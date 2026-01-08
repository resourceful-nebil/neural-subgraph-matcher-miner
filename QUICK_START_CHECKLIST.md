# Quick Start Checklist: Google Web Graph with GitHub Actions

## ✅ Step-by-Step Checklist

### Phase 1: Prepare Dataset Locally

- [ ] **Download dataset**
  - Go to: https://snap.stanford.edu/data/web-Google.html
  - Download `web-Google.txt.gz`
  - Extract to get `web-Google.txt`

- [ ] **Convert to pickle format**
  ```bash
  python convert_google_web.py --input web-Google.txt --output web-google.pkl
  ```
  - Verify output shows: ~875K nodes, ~5.1M edges
  - File `web-google.pkl` is created

- [ ] **Check file size**
  - If > 100MB → Need Git LFS
  - If < 100MB → Can add normally

### Phase 2: Modify Workflow File

- [ ] **Open file:** `.github/workflows/run.yml`

- [ ] **Find line 49** (should say `--dataset=directed.pkl \`)

- [ ] **Change to:** `--dataset=web-google.pkl \`

- [ ] **(Optional) Change line 52** from `patterns.pkl` to `web-google-patterns.pkl`

### Phase 3: Set Up Git LFS (Only if file > 100MB)

- [ ] Install Git LFS (if not installed)
  - Windows: https://git-lfs.github.com/
  - Linux: `sudo apt-get install git-lfs`
  - Mac: `brew install git-lfs`

- [ ] Initialize Git LFS:
  ```bash
  git lfs install
  git lfs track "*.pkl"
  git add .gitattributes
  ```

### Phase 4: Commit and Push

- [ ] **Add files to git:**
  ```bash
  git add web-google.pkl
  git add .github/workflows/run.yml
  git add .gitattributes  # (only if using Git LFS)
  ```

- [ ] **Commit:**
  ```bash
  git commit -m "Add Google web graph dataset and update workflow"
  ```

- [ ] **Push (triggers GitHub Actions!):**
  ```bash
  git push origin main
  ```

### Phase 5: Monitor Execution

- [ ] Go to GitHub repository
- [ ] Click "Actions" tab
- [ ] Watch workflow run
- [ ] Wait for completion (may take 30 min - 2 hours)

### Phase 6: Download Results

- [ ] In Actions tab, click on completed workflow run
- [ ] Scroll down to "Artifacts"
- [ ] Download "decoder-plots"
- [ ] Extract zip file
- [ ] Check `plots/cluster/` for HTML visualizations
- [ ] Check `results/` for pattern files

---

## 📝 Files You're Modifying/Adding

| File | Action | Line/Details |
|------|--------|--------------|
| `.github/workflows/run.yml` | **MODIFY** | Line 49: Change `directed.pkl` → `web-google.pkl` |
| `web-google.pkl` | **ADD** | New file (your dataset) |
| `.gitattributes` | **ADD** (if using Git LFS) | New file (auto-created by `git lfs track`) |

---

## 🔍 Exact Change in Workflow File

**File:** `.github/workflows/run.yml`

**BEFORE (Line 49):**
```yaml
                --dataset=directed.pkl \
```

**AFTER (Line 49):**
```yaml
                --dataset=web-google.pkl \
```

That's the only required change!

---

## ⚠️ Important Notes

1. **Large File Warning:** `web-google.pkl` will be 100-200MB. Use Git LFS if > 100MB.
2. **Workflow Time:** May take 30 minutes to 2+ hours depending on parameters
3. **Check Actions Tab:** After pushing, immediately check GitHub Actions tab to see it start
4. **Results Location:** Download artifacts from Actions tab, not from repository files

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "File too large" when pushing | Use Git LFS (see Phase 3) |
| Workflow fails: "FileNotFoundError" | Make sure `web-google.pkl` was committed |
| Workflow times out | Reduce `--n_trials` to 500 or less |
| Don't see workflow running | Check you pushed to `main` branch |

---

## 📞 What to Do Next

After workflow completes:
1. Download artifacts
2. Analyze results
3. Create your evaluation report
4. Document findings

Good luck! 🚀



