# Step-by-Step Execution Guide: Google Web Graph Analysis

Based on the workflow file (`.github/workflows/run.yml`), here's the practical execution guide.

## Prerequisites

1. **Python environment** with required packages (or Docker)
2. **Dataset**: web-Google.txt from Stanford SNAP
3. **Checkpoint file**: Should exist at `ckpt/model.pt` (pre-trained model)

---

## Step 1: Prepare the Dataset

### 1.1 Download the Dataset

```bash
# Download from SNAP
wget https://snap.stanford.edu/data/web-Google.txt.gz

# Extract
gunzip web-Google.txt.gz
```

### 1.2 Convert to Pickle Format

Use the provided conversion script:

```bash
python convert_google_web.py --input web-Google.txt --output web-google.pkl
```

This will create `web-google.pkl` in the current directory.

**Verify the conversion:**
- Check that the file was created
- You should see output showing ~875K nodes and ~5.1M edges

---

## Step 2: Prepare Directory Structure

Create the necessary output directories (as shown in the workflow):

```bash
mkdir -p plots/cluster
mkdir -p results
```

**Note**: The workflow uses `chmod -R 777` but this is optional for local execution.

---

## Step 3: Run SPMiner Decoder

### Option A: Direct Python Execution (Recommended for Local)

Based on the workflow pattern, but adapted for your dataset:

```bash
python -m subgraph_mining.decoder \
    --dataset=web-google.pkl \
    --n_trials=200 \
    --node_anchored \
    --out_path=results/web-google-patterns.pkl \
    --graph_type=directed
```

**Key Parameters (from workflow):**
- `--dataset=web-google.pkl`: Your prepared dataset
- `--n_trials=200`: Number of search trials (workflow uses 200, you may want more for better results)
- `--node_anchored`: Node-anchored patterns (required)
- `--out_path=results/web-google-patterns.pkl`: Output location
- `--graph_type=directed`: Directed graph type

**Additional Parameters (for Google web graph - larger dataset):**

For the Google web graph (875K nodes), you may want to add:

```bash
python -m subgraph_mining.decoder \
    --dataset=web-google.pkl \
    --n_trials=1000 \
    --n_neighborhoods=10000 \
    --min_pattern_size=3 \
    --max_pattern_size=7 \
    --min_neighborhood_size=20 \
    --max_neighborhood_size=29 \
    --search_strategy=greedy \
    --out_batch_size=3 \
    --node_anchored \
    --out_path=results/web-google-patterns.pkl \
    --graph_type=directed
```

**What happens:**
- The decoder loads the graph
- Analyzes graph characteristics (may enable streaming mode for large graphs)
- Mines frequent subgraph patterns
- Saves patterns to `results/web-google-patterns.pkl`
- Creates visualizations in `plots/cluster/`
- Prints runtime at the end

**Runtime Tracking:**
- The decoder automatically prints runtime: `X TOTAL TIME` and `Y mins Z secs`
- Note this value for your report

**Memory Monitoring:**
- Monitor memory usage in another terminal: `htop` or `top`
- Or use: `watch -n 1 free -h` (Linux) or Task Manager (Windows)

---

### Option B: Docker Execution (Optional)

If you prefer using Docker (as in the workflow):

```bash
# Pull the Docker image
docker pull samribahta/decoder-image:latest

# Run decoder in Docker
docker run --rm \
    -v $(pwd):/app \
    -e PYTHONUNBUFFERED=1 \
    samribahta/decoder-image:latest \
    bash -c "
        python -m subgraph_mining.decoder \
            --dataset=/app/web-google.pkl \
            --n_trials=200 \
            --node_anchored \
            --out_path=/app/results/web-google-patterns.pkl \
            --graph_type=directed
    "
```

---

## Step 4: Count Pattern Instances

After the decoder finishes, count how many times each pattern appears in the graph.

Based on the commented workflow code, here's the command:

```bash
python -m analyze.count_patterns \
    --dataset=web-google.pkl \
    --queries_path=results/web-google-patterns.pkl \
    --out_path=results/web-google-counts.json \
    --node_anchored \
    --graph_type=directed \
    --n_workers=4 \
    --count_method=bin
```

**Parameters:**
- `--dataset=web-google.pkl`: Your graph dataset
- `--queries_path=results/web-google-patterns.pkl`: Patterns from Step 3
- `--out_path=results/web-google-counts.json`: Count results
- `--node_anchored`: Match workflow settings
- `--graph_type=directed`: Directed graph
- `--n_workers=4`: Parallel workers (adjust based on CPU)
- `--count_method=bin`: Binary matching (faster)

**Note**: This step may take a long time for large graphs. You can use:
- `--timeout=600` to limit time per query
- `--max_query_size=10` to limit pattern sizes
- `--sample_anchors=1000` for large graphs

---

## Step 5: Analyze Results

### 5.1 Analyze Pattern Counts

```bash
python -m analyze.analyze_pattern_counts \
    --counts_path=results/ \
    --out_path=results/web-google-analysis.csv
```

This generates analysis CSV file with pattern statistics.

### 5.2 Manual Inspection

**Check the output files:**

1. **Patterns file**: `results/web-google-patterns.pkl`
   - Contains NetworkX graph objects for each discovered pattern
   - Load with: `pickle.load(open('results/web-google-patterns.pkl', 'rb'))`

2. **Counts file**: `results/web-google-counts.json`
   - Contains pattern frequencies
   - Format: `[pattern_sizes, instance_counts, baseline_counts]`

3. **Visualizations**: `plots/cluster/`
   - HTML files showing pattern graphs
   - Files named like: `dir_3_rank_1_*.html`, `dir_4_rank_1_*.html`, etc.
   - Open in a web browser to view patterns

### 5.3 Extract Metrics

**From decoder output:**
- **Runtime**: Look for "TOTAL TIME" in console output
- **Number of patterns**: Count patterns in pickle file or check `plots/cluster/` directory

**From counts file:**
```python
import json

with open('results/web-google-counts.json', 'r') as f:
    sizes, counts, _ = json.load(f)

# Calculate metrics
total_instances = sum(counts)
patterns_by_size = {}
for size, count in zip(sizes, counts):
    if size not in patterns_by_size:
        patterns_by_size[size] = []
    patterns_by_size[size].append(count)

print(f"Total instances: {total_instances}")
for size in sorted(patterns_by_size.keys()):
    print(f"Size {size}: {sum(patterns_by_size[size])} instances across {len(patterns_by_size[size])} patterns")
```

**Pattern Diversity:**
- Count unique topologies by examining HTML files
- Categorize: triangles, stars, chains, cycles, etc.
- Note duplication rate (check if patterns are unique)

---

## Step 6: Document Results

Create your evaluation report following this structure:

### 6.1 Introduction to Dataset
- Google web graph description
- Dataset statistics (nodes, edges, connectivity)
- Domain context (web pages and hyperlinks)

### 6.2 Running SPMiner and Metrics
- Configuration parameters used
- Runtime (from decoder output)
- Memory usage (if monitored)
- Number of patterns discovered
- Pattern breakdown by size and rank
- Instance counts (from counts.json)

### 6.3 Motif Interpretability
- Visual inspection of HTML files
- Topology analysis
- Pattern structures found

### 6.4 Domain-Specific Insights
- Web graph interpretations
- Hub pages (star patterns)
- Link structures (triangles, chains)
- Navigation pathways

### 6.5 Findings
- Usefulness for web graph analysis
- Strengths and limitations
- Potential applications (SEO, navigation design, etc.)

---

## Quick Reference: Complete Command Sequence

```bash
# 1. Download and convert dataset
wget https://snap.stanford.edu/data/web-Google.txt.gz
gunzip web-Google.txt.gz
python convert_google_web.py --input web-Google.txt --output web-google.pkl

# 2. Create directories
mkdir -p plots/cluster results

# 3. Run decoder
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

# 4. Count patterns
python -m analyze.count_patterns \
    --dataset=web-google.pkl \
    --queries_path=results/web-google-patterns.pkl \
    --out_path=results/web-google-counts.json \
    --node_anchored \
    --graph_type=directed \
    --n_workers=4 \
    --count_method=bin

# 5. Analyze results
python -m analyze.analyze_pattern_counts \
    --counts_path=results/ \
    --out_path=results/web-google-analysis.csv
```

---

## Troubleshooting

### Issue: "File not found" errors
**Solution**: Ensure you're in the correct directory and files exist. Use absolute paths if needed.

### Issue: Memory errors
**Solution**: 
- Reduce `--max_pattern_size` (try 5-6 instead of 7-8)
- Reduce `--n_trials` (try 500 instead of 1000)
- Use `--memory_efficient` flag if available
- The decoder will auto-detect and use streaming mode for large graphs

### Issue: Very long runtime
**Solution**:
- Start with smaller parameters (`--n_trials=200`, `--max_pattern_size=5`)
- Use greedy search (already default)
- Run overnight or on a server
- Monitor progress - the decoder prints status messages

### Issue: Pattern counting takes too long
**Solution**:
- Use `--count_method=bin` (binary, faster)
- Reduce `--max_query_size` (e.g., `--max_query_size=8`)
- Use `--timeout=300` to skip slow queries
- For very large graphs, use `--sample_anchors=1000`

---

## Expected Timeline

For Google web graph (875K nodes):
- **Dataset conversion**: 2-5 minutes
- **SPMiner decoder**: 30 minutes - 2 hours (depends on parameters)
- **Pattern counting**: 1-4 hours (depends on pattern complexity)
- **Analysis**: 30 minutes - 1 hour

**Total**: ~2-7 hours depending on hardware and parameters

---

## Key Differences from Workflow

The workflow uses simpler parameters:
- `--n_trials=200` (workflow) vs `--n_trials=1000` (recommended for large graph)
- Fewer explicit parameters (uses defaults from config.py)

For the Google web graph, you'll likely need more parameters to get good results, but you can start with the workflow's simpler command and add parameters as needed.



