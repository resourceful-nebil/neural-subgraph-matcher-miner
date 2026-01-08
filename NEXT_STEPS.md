# Next Steps: Commit and Push to GitHub

## ✅ Completed
- [x] Downloaded dataset (web-Google.txt)
- [x] Converted to pickle format (web-google.pkl - 120.83 MB)
- [x] Modified workflow file (.github/workflows/run.yml)

## 🔄 Next Steps: Git Setup and Push

### Step 1: Set Up Git LFS (Required - file is 120.83 MB)

Since your file is over 100MB, you MUST use Git LFS:

```powershell
# Initialize Git LFS in your repository
git lfs install

# Track .pkl files with Git LFS
git lfs track "*.pkl"

# Add the .gitattributes file (created by git lfs track)
git add .gitattributes
```

### Step 2: Add Files to Git

```powershell
# Add your dataset file (will use Git LFS)
git add web-google.pkl

# Add the modified workflow file
git add .github/workflows/run.yml
```

### Step 3: Commit

```powershell
git commit -m "Add Google web graph dataset and update workflow for SPMiner"
```

### Step 4: Push (This Triggers GitHub Actions!)

```powershell
git push origin main
```

**This push will automatically trigger the GitHub Actions workflow!**

### Step 5: Monitor on GitHub

1. Go to your GitHub repository in a web browser
2. Click the **"Actions"** tab (top menu)
3. You'll see a new workflow run starting
4. Click on it to watch the progress
5. Wait for it to complete (may take 30 minutes - 2 hours)

### Step 6: Download Results

After the workflow completes:
1. In the workflow run page, scroll to "Artifacts"
2. Download "decoder-plots"
3. Extract to see your results in `plots/cluster/` and `results/`

---

## 📋 Summary of Changes Made

### File Modified:
- **`.github/workflows/run.yml`** (Line 49 & 52)
  - Changed: `--dataset=directed.pkl` → `--dataset=web-google.pkl`
  - Changed: `--out_path=/app/results/patterns.pkl` → `--out_path=/app/results/web-google-patterns.pkl`

### File Added:
- **`web-google.pkl`** (120.83 MB - will use Git LFS)
- **`.gitattributes`** (created by `git lfs track`)

---

## ⚠️ Important Notes

1. **Git LFS is required** - File is 120.83 MB (> 100MB GitHub limit)
2. **Make sure to run `git lfs track "*.pkl"` before adding the file**
3. **Workflow will run automatically** after you push
4. **Check Actions tab** immediately after pushing to see it start

---

## 🆘 If Something Goes Wrong

**If push fails with "file too large":**
- Make sure you ran `git lfs install` and `git lfs track "*.pkl"` first
- Check that `.gitattributes` was added

**If workflow fails:**
- Check the Actions tab logs for error messages
- Common issue: File not found - make sure `web-google.pkl` was committed

Good luck! 🚀



