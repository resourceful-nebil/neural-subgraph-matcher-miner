# GitHub Actions Setup Guide: Google Web Graph Analysis

## Files You Need to Modify/Touch

1. **`.github/workflows/run.yml`** - Modify this workflow file
2. **Download and add `web-google.pkl`** - New file to add to repository
3. **`convert_google_web.py`** - Already created, just use it locally

## Complete Step-by-Step Process

---

## Step 1: Download the Dataset

### 1.1 Download from SNAP

**On Windows (PowerShell):**
```powershell
# Download the file
Invoke-WebRequest -Uri "https://snap.stanford.edu/data/web-Google.txt.gz" -OutFile "web-Google.txt.gz"

# Extract using 7-Zip or WinRAR, OR use PowerShell:
# (If you have 7-Zip installed)
& "C:\Program Files\7-Zip\7z.exe" x web-Google.txt.gz
```

**On Linux/Mac:**
```bash
wget https://snap.stanford.edu/data/web-Google.txt.gz
gunzip web-Google.txt.gz
```

**Or download manually:**
1. Go to: https://snap.stanford.edu/data/web-Google.html
2. Click "web-Google.txt.gz" to download
3. Extract the `.gz` file using 7-Zip, WinRAR, or similar

**Expected file:** `web-Google.txt` (should be around 68-70 MB uncompressed)

---

## Step 2: Convert Dataset to Pickle Format (LOCALLY)

**Run this on your local machine:**

```bash
python convert_google_web.py --input web-Google.txt --output web-google.pkl
```

**What this does:**
- Reads the SNAP format file
- Converts it to NetworkX DiGraph
- Saves as `web-google.pkl`

**Expected output:**
- File: `web-google.pkl` (will be large, ~100-200MB)
- Console output showing: "Graph created: Nodes: 875,713, Edges: 5,105,039"

**⚠️ Important:** Do this conversion **locally first** to verify it works, then add the `.pkl` file to your repository.

---

## Step 3: Modify the Workflow File

**File to modify:** `.github/workflows/run.yml`

### 3.1 What to Change

You need to update **line 49** in the workflow file. 

**Current line 49:**
```yaml
--dataset=directed.pkl \
```

**Change it to:**
```yaml
--dataset=web-google.pkl \
```

### 3.2 Complete Updated Workflow Section

Here's the complete section to replace (lines 48-53):

**OLD:**
```yaml
python -m subgraph_mining.decoder \
    --dataset=directed.pkl \
    --n_trials=200 \
    --node_anchored \
    --out_path=/app/results/patterns.pkl \
    --graph_type=directed
```

**NEW (Option 1 - Simple, like current workflow):**
```yaml
python -m subgraph_mining.decoder \
    --dataset=web-google.pkl \
    --n_trials=200 \
    --node_anchored \
    --out_path=/app/results/web-google-patterns.pkl \
    --graph_type=directed
```

**NEW (Option 2 - Better parameters for large graph):**
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

**Recommendation:** Start with **Option 1** (simple, like current workflow). If it works, you can later try Option 2 with more parameters.

---

## Step 4: Add Files to Git Repository

### 4.1 Add the Dataset File

**⚠️ Important Note About Large Files:**
- The `web-google.pkl` file will be large (~100-200MB)
- GitHub has a 100MB file size limit for regular Git
- Files over 100MB need Git LFS (Large File Storage)

**Check file size first:**
```bash
# Windows PowerShell
(Get-Item web-google.pkl).Length / 1MB

# Linux/Mac
ls -lh web-google.pkl
```

**If file is > 100MB, you have two options:**

#### Option A: Use Git LFS (Recommended for large files)

```bash
# Install Git LFS (if not installed)
# Windows: Download from https://git-lfs.github.com/
# Linux: sudo apt-get install git-lfs
# Mac: brew install git-lfs

# Initialize Git LFS in your repo
git lfs install

# Track .pkl files with Git LFS
git lfs track "*.pkl"

# Add the .gitattributes file
git add .gitattributes

# Add your dataset
git add web-google.pkl
```

#### Option B: If file is < 100MB, add normally

```bash
git add web-google.pkl
```

### 4.2 Add the Modified Workflow File

```bash
git add .github/workflows/run.yml
```

### 4.3 Commit the Changes

```bash
git commit -m "Add Google web graph dataset and update workflow for SPMiner"
```

### 4.4 Push to Repository

```bash
git push origin main
```

**This will automatically trigger the GitHub Actions workflow!**

---

## Step 5: Monitor the Workflow Execution

### 5.1 View Workflow Progress

1. Go to your GitHub repository in a web browser
2. Click on the **"Actions"** tab (top menu)
3. You'll see a new workflow run starting (it will show "Run Decoder" with a yellow dot)
4. Click on the workflow run to see detailed logs

### 5.2 What to Look For

**Success indicators:**
- Green checkmark ✅ when complete
- Logs showing "Starting decoder run..."
- Final logs showing file listings in `/app/plots/cluster` and `/app/results`
- "Upload plots as artifact" step completes

**If it fails:**
- Red X ❌ indicates failure
- Click on the failed step to see error messages
- Common issues:
  - File not found (dataset file not committed properly)
  - Out of memory (graph too large, need to adjust parameters)
  - Timeout (workflow runs too long, GitHub has time limits)

### 5.3 Download Results

After the workflow completes successfully:

1. In the workflow run page, scroll down to "Artifacts"
2. You'll see "decoder-plots" artifact
3. Click to download (contains `plots/` and `results/` folders)
4. Extract the zip file to see your results

---

## Complete Command Sequence (Summary)

```bash
# 1. Download dataset (do this locally)
# Windows: Use browser or Invoke-WebRequest
# Extract web-Google.txt.gz to web-Google.txt

# 2. Convert to pickle (locally)
python convert_google_web.py --input web-Google.txt --output web-google.pkl

# 3. Check file size
# If > 100MB, use Git LFS:
git lfs install
git lfs track "*.pkl"
git add .gitattributes

# 4. Add files to git
git add web-google.pkl
git add .github/workflows/run.yml

# 5. Commit
git commit -m "Add Google web graph dataset and update workflow"

# 6. Push (this triggers GitHub Actions!)
git push origin main

# 7. Go to GitHub -> Actions tab to watch it run
```

---

## Files Summary: What You're Touching

| File | Action | Why |
|------|--------|-----|
| `.github/workflows/run.yml` | **MODIFY** | Change dataset name from `directed.pkl` to `web-google.pkl` |
| `web-google.pkl` | **ADD** | Your converted Google web graph dataset |
| `web-Google.txt` | **DOWNLOAD** (don't commit) | Original dataset (keep local, don't add to repo) |
| `convert_google_web.py` | **USE** (already exists) | Script to convert dataset (no changes needed) |

---

## Troubleshooting

### Issue: "File too large" error when pushing

**Solution:** Use Git LFS (see Step 4.1, Option A)

### Issue: Workflow fails with "FileNotFoundError: web-google.pkl"

**Solution:** 
- Make sure you committed and pushed `web-google.pkl`
- Check that the file path in workflow matches exactly: `web-google.pkl`
- Verify the file is in the repository root (not in a subdirectory)

### Issue: Workflow times out

**Solution:**
- GitHub Actions has a 6-hour limit for free accounts
- For very large graphs, the workflow might timeout
- Try reducing `--n_trials` (e.g., use 500 instead of 1000)
- Reduce `--max_pattern_size` (e.g., use 5 instead of 7)

### Issue: Out of memory errors

**Solution:**
- The decoder should auto-detect and use streaming mode
- If it still fails, reduce parameters:
  - Lower `--n_trials`
  - Lower `--max_pattern_size`
  - Lower `--n_neighborhoods`

---

## Next Steps After Workflow Runs

1. Download the artifacts from GitHub Actions
2. Extract and examine the results in `plots/cluster/` (HTML visualizations)
3. Check `results/` folder for pattern files
4. Use the results to create your evaluation report

---

## Quick Reference: Exact Changes to Workflow File

**File:** `.github/workflows/run.yml`

**Line 49:** Change `directed.pkl` to `web-google.pkl`

**Line 52 (optional):** Change output path from `patterns.pkl` to `web-google-patterns.pkl` for clarity

That's it! Just these minimal changes to get it working.



