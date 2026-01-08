# Understanding GitHub Actions Workflow Execution

## What Your Mentor Meant

When your mentor said **"the code will run when you push code to the repository"**, they're referring to **GitHub Actions** - an automated CI/CD (Continuous Integration/Continuous Deployment) system.

## How It Works

Looking at `.github/workflows/run.yml`, the workflow file defines **when** and **how** the code runs automatically:

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
```

This means the workflow **automatically triggers** in three scenarios:

### 1. **Push to Main Branch** (Automatic)
When you push code to the `main` branch:
```bash
git add .
git commit -m "Add dataset"
git push origin main
```
→ GitHub Actions **automatically** starts running the decoder

### 2. **Pull Request to Main** (Automatic)
When someone creates a pull request targeting `main`
→ Workflow runs to test the changes

### 3. **Manual Trigger** (`workflow_dispatch`)
You can manually trigger it from GitHub's web interface:
- Go to the "Actions" tab in your repository
- Select the "Run Decoder" workflow
- Click "Run workflow" button

## What Happens When Workflow Runs

The workflow (lines 38-57) will:
1. Pull a Docker image with the required environment
2. Create output directories (`plots/cluster`, `results`)
3. Run the decoder in a Docker container:
   ```bash
   python -m subgraph_mining.decoder \
       --dataset=directed.pkl \
       --n_trials=200 \
       --node_anchored \
       --out_path=/app/results/patterns.pkl \
       --graph_type=directed
   ```
4. Upload results as artifacts (downloadable from GitHub Actions UI)

## Important Considerations for Your Task

### Current Workflow Issue

The workflow currently uses:
```yaml
--dataset=directed.pkl
```

This is a **hardcoded dataset name**. For your Google web graph task, you have a few options:

### Option 1: Modify the Workflow File (Recommended for GitHub Actions)

Edit `.github/workflows/run.yml` to use your dataset:

```yaml
python -m subgraph_mining.decoder \
    --dataset=web-google.pkl \
    --n_trials=1000 \
    --n_neighborhoods=10000 \
    --min_pattern_size=3 \
    --max_pattern_size=7 \
    --search_strategy=greedy \
    --out_batch_size=3 \
    --node_anchored \
    --out_path=/app/results/web-google-patterns.pkl \
    --graph_type=directed
```

**Then:**
1. Add your `web-google.pkl` file to the repository
2. Commit and push:
   ```bash
   git add web-google.pkl .github/workflows/run.yml
   git commit -m "Add Google web graph dataset and update workflow"
   git push origin main
   ```
3. The workflow will automatically run

**⚠️ Warning**: The Google web graph pickle file will be **large** (~100-200MB+). Consider using Git LFS (Large File Storage) or running locally instead.

### Option 2: Run Locally (Recommended for Large Datasets)

Instead of pushing to GitHub, run it on your local machine:

1. **Prepare your dataset locally**:
   ```bash
   python convert_google_web.py --input web-Google.txt --output web-google.pkl
   ```

2. **Run the decoder locally**:
   ```bash
   python -m subgraph_mining.decoder \
       --dataset=web-google.pkl \
       --n_trials=1000 \
       --node_anchored \
       --out_path=results/web-google-patterns.pkl \
       --graph_type=directed
   ```

3. **No need to push** - work with results locally

**Advantages:**
- No large file uploads
- Faster (no network overhead)
- More control over parameters
- Can monitor progress in real-time

### Option 3: Use Manual Trigger with Input Parameters

You could modify the workflow to accept dataset name as an input parameter, then manually trigger it with your dataset name.

## Where to See Workflow Results

When the workflow runs (either automatically or manually):

1. Go to your repository on GitHub
2. Click the **"Actions"** tab
3. You'll see a list of workflow runs
4. Click on a specific run to see:
   - Logs of the execution
   - Success/failure status
   - Downloadable artifacts (results, plots)

## For Your Google Web Graph Task

### Recommended Approach

Given the large size of the Google web graph dataset:

1. **Run locally** for development and testing
2. **Use GitHub Actions** only if:
   - You want to share results with your mentor automatically
   - You need to run it on GitHub's infrastructure
   - You're comfortable with Git LFS for large files

### Step-by-Step for Local Execution

```bash
# 1. Download dataset
wget https://snap.stanford.edu/data/web-Google.txt.gz
gunzip web-Google.txt.gz

# 2. Convert to pickle
python convert_google_web.py --input web-Google.txt --output web-google.pkl

# 3. Create directories
mkdir -p plots/cluster results

# 4. Run decoder (locally, no push needed)
python -m subgraph_mining.decoder \
    --dataset=web-google.pkl \
    --n_trials=1000 \
    --n_neighborhoods=10000 \
    --min_pattern_size=3 \
    --max_pattern_size=7 \
    --search_strategy=greedy \
    --out_batch_size=3 \
    --node_anchored \
    --out_path=results/web-google-patterns.pkl \
    --graph_type=directed
```

## Summary

- **"Push to run"** = GitHub Actions automatically executes when you push code
- **You have options**: Run locally OR push to trigger GitHub Actions
- **For large datasets**: Local execution is usually more practical
- **Workflow file** = Defines what runs automatically
- **Results**: Available as artifacts in GitHub Actions UI (if using GitHub) or locally in `results/` folder

## Questions to Ask Your Mentor

1. Should I commit the large `.pkl` file, or run locally?
2. Do you want to see results via GitHub Actions artifacts, or can I share them another way?
3. Should I modify the workflow file for the Google web graph, or run it separately?



