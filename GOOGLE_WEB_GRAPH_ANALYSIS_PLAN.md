# Google Web Graph Dataset Analysis Plan

## Codebase Analysis Summary

### SPMiner Architecture Overview

**SPMiner (Neural Subgraph Matcher Miner)** is a graph neural network-based framework for extracting frequent subgraph patterns. The workflow consists of:

1. **Pre-trained GNN Encoder**: Uses a pre-trained model (checkpoint at `ckpt/model.pt` or `ckpt/model_new.pt`) based on NeuroMatch
2. **Pattern Discovery**: The decoder (`subgraph_mining/decoder.py`) mines frequent subgraphs
3. **Pattern Visualization**: Results are saved as HTML files in `plots/cluster/`
4. **Pattern Counting**: The `analyze/count_patterns.py` script counts real-world instances

### Key Components

- **Main Script**: `subgraph_mining/decoder.py` - Runs SPMiner
- **Configuration**: `subgraph_mining/config.py` - Contains default parameters
- **Pattern Counting**: `analyze/count_patterns.py` - Counts pattern frequencies
- **Analysis**: `analyze/analyze_pattern_counts.py` - Analyzes count results
- **Visualization**: `visualizer/visualizer.py` - Creates HTML visualizations

### Dataset Format

SPMiner accepts:

- `.pkl` files containing NetworkX graphs (Graph or DiGraph)
- Or predefined datasets (enzymes, cox2, etc.)

The Google web graph needs to be:

- Downloaded from SNAP (web-Google.txt.gz)
- Converted to NetworkX DiGraph format
- Saved as a `.pkl` file

---

## Step-by-Step Execution Plan

### Step 1: Download and Prepare the Dataset

**1.1 Download the Dataset**

- Download `web-Google.txt.gz` from Stanford SNAP datasets
- URL: https://snap.stanford.edu/data/web-Google.html
- Extract the `.txt` file

**1.2 Convert to NetworkX Format**
Create a script to convert the SNAP format to a NetworkX DiGraph pickle file:

```python
# convert_google_web.py
import networkx as nx
import pickle
import gzip

# Read the SNAP format file
graph = nx.DiGraph()

with open('web-Google.txt', 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        parts = line.strip().split('\t')
        if len(parts) == 2:
            source, target = int(parts[0]), int(parts[1])
            graph.add_edge(source, target)

            # Add node attributes (required by SPMiner)
            if source not in graph.nodes():
                graph.nodes[source]['id'] = str(source)
                graph.nodes[source]['label'] = str(source)
            if target not in graph.nodes():
                graph.nodes[target]['id'] = str(target)
                graph.nodes[target]['label'] = str(target)

# Save as pickle
with open('web-google.pkl', 'wb') as f:
    pickle.dump(graph, f)

print(f"Created graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
```

**1.3 Verify Graph Statistics**
The dataset should have:

- Nodes: 875,713
- Edges: 5,105,039
- Type: Directed
- Largest WCC: 855,802 nodes (97.7%)
- Largest SCC: 434,818 nodes (49.7%)
- Average clustering: 0.5143

---

### Step 2: Run SPMiner

**2.1 Basic Command Structure**

```bash
python3 -m subgraph_mining.decoder \
    --dataset=web-google.pkl \
    --graph_type=directed \
    --node_anchored \
    --out_path=results/web-google-patterns.pkl \
    --n_trials=1000 \
    --n_neighborhoods=10000 \
    --min_pattern_size=3 \
    --max_pattern_size=8 \
    --min_neighborhood_size=20 \
    --max_neighborhood_size=29 \
    --search_strategy=greedy \
    --out_batch_size=3
```

**2.2 Key Parameters Explained**

- `--dataset=web-google.pkl`: Path to your prepared dataset
- `--graph_type=directed`: Google web graph is directed
- `--node_anchored`: Uses node-anchored patterns (recommended)
- `--n_trials=1000`: Number of search trials (adjust based on time/compute)
- `--n_neighborhoods=10000`: Number of neighborhoods to sample
- `--min_pattern_size=3`: Minimum motif size
- `--max_pattern_size=8`: Maximum motif size (adjust based on dataset size)
- `--search_strategy=greedy`: Use greedy search (faster) or "mcts" (more thorough)
- `--out_batch_size=3`: Top 3 patterns per size

**2.3 For Large Graphs (Memory Considerations)**

The Google web graph is large (875K nodes). The decoder automatically analyzes graph characteristics and may use streaming mode. You can also force streaming:

```bash
--use_streaming \
--streaming_workers=4 \
--chunk_size=10000
```

**2.4 Track Runtime and Memory**

Runtime is automatically printed at the end. To track memory, you can:

1. Use system monitoring: `htop` or `top` in another terminal
2. Use Python's `psutil` library to log memory usage
3. Check if the code already logs memory (check `common/utils.py`)

The output will show:

- Total runtime in seconds
- Number of patterns discovered
- Patterns saved to `results/web-google-patterns.pkl`
- Visualizations in `plots/cluster/`

---

### Step 3: Count Pattern Instances

**3.1 Run Pattern Counting**

```bash
python3 -m analyze.count_patterns \
    --dataset=web-google.pkl \
    --queries_path=results/web-google-patterns.pkl \
    --out_path=results/web-google-counts.json \
    --node_anchored \
    --graph_type=directed \
    --n_workers=4 \
    --count_method=bin \
    --max_query_size=20 \
    --timeout=600
```

**3.2 Parameters**

- `--count_method=bin`: Binary matching (faster) or "freq" for exact frequency
- `--n_workers=4`: Number of parallel workers
- `--timeout=600`: Maximum time per query (10 minutes)
- `--max_query_size=20`: Maximum pattern size to count

This generates `results/web-google-counts.json` with pattern frequencies.

---

### Step 4: Analyze Results

**4.1 Analyze Pattern Counts**

```bash
python3 -m analyze.analyze_pattern_counts \
    --counts_path=results/ \
    --out_path=results/web-google-analysis.csv
```

**4.2 Manual Analysis**

Examine the output files:

- `results/web-google-patterns.pkl`: Discovered patterns (NetworkX graphs)
- `results/web-google-counts.json`: Pattern frequencies
- `plots/cluster/`: HTML visualizations of each pattern

**4.3 Extract Metrics**

From the count JSON file, extract:

- Pattern sizes and ranks
- Instance counts per pattern
- Total instances across all patterns
- Pattern diversity (topological types)

---

### Step 5: Interpret Motifs for Web Graph Domain

**5.1 Web Graph-Specific Insights**

The Google web graph represents hyperlink relationships. Patterns might indicate:

1. **Triangles (Size-3)**: Mutual linking between pages (A→B, B→C, C→A)

   - Could indicate topic clusters
   - Related content pages linking to each other

2. **Stars (Size-4+)**: Hub pages with many outbound links

   - Popular entry points (homepages, portals)
   - Navigation structures

3. **Chains (Size-5+)**: Sequential linking patterns

   - Content hierarchies
   - Navigation paths
   - Topic progressions

4. **Cycles**: Circular link structures
   - Content loops
   - Related topic groups

**5.2 Domain Applications**

- **SEO Analysis**: Identify important hub pages
- **Link Structure Analysis**: Understand web topology
- **Navigation Design**: Optimize user pathways
- **Content Discovery**: Find related page clusters

---

## Expected Output Structure

### Files Generated

```
results/
├── web-google-patterns.pkl          # Discovered patterns
├── web-google-counts.json           # Pattern frequencies
└── web-google-analysis.csv          # Analysis results

plots/cluster/
├── dir_3_rank_1_*.html              # Size-3, Rank-1 pattern visualization
├── dir_3_rank_2_*.html              # Size-3, Rank-2 pattern visualization
├── dir_4_rank_1_*.html              # Size-4, Rank-1 pattern visualization
└── ... (more patterns)
```

### Metrics to Collect

1. **Runtime**: Total execution time from decoder output
2. **Memory Usage**: Peak memory during execution (need to monitor)
3. **Motif Diversity**:
   - Number of unique topologies
   - Distribution across sizes
   - Topological types (triangles, stars, chains, cycles)
4. **Instance Counts**: Total occurrences of each pattern

---

## Documentation Template (Based on Amazon Example)

### Structure for Your Report

1. **Introduction to the Dataset**

   - Dataset description
   - Graph structure characteristics
   - Domain context (web graph, hyperlinks)

2. **Explanation of Output**

   - SPMiner methodology
   - Configuration used
   - Runtime and memory metrics
   - Pattern breakdown by size and rank

3. **Assessment of Motif Interpretability**

   - Visual inspection of patterns
   - Topology analysis
   - Label/attribute analysis (if any)

4. **Domain-Specific Insights**

   - Web graph interpretations
   - Hub page identification
   - Link structure patterns
   - Navigation pathways

5. **Findings: Usefulness, Strengths, Limitations**
   - Usefulness for web graph analysis
   - Strengths of SPMiner on this dataset
   - Limitations observed
   - Potential applications

---

## Potential Challenges & Solutions

### Challenge 1: Large Dataset Size

**Solution**:

- Use streaming mode (`--use_streaming`)
- Reduce `--max_pattern_size` initially (try 5-6)
- Reduce `--n_trials` if needed (start with 500)
- Use `--memory_efficient` flag

### Challenge 2: Memory Issues

**Solution**:

- Monitor memory usage: `watch -n 1 free -h`
- Reduce `--n_neighborhoods` (try 5000)
- Use smaller chunk sizes in streaming mode
- Process in multiple runs with different size ranges

### Challenge 3: Long Runtime

**Solution**:

- Start with smaller parameters (fewer trials, smaller max size)
- Use greedy search (faster than MCTS)
- Parallelize counting with `--n_workers`
- Run overnight or on a server

### Challenge 4: Pattern Interpretability

**Solution**:

- Examine HTML visualizations in `plots/cluster/`
- Look for common web graph structures (hubs, chains, triangles)
- Compare patterns to known web topology patterns
- Analyze node degrees in patterns

---

## Next Steps

1. **Download the dataset** from SNAP
2. **Create conversion script** to generate `web-google.pkl`
3. **Run SPMiner** with initial parameters
4. **Monitor runtime and memory** during execution
5. **Count pattern instances** using count_patterns.py
6. **Analyze results** and extract metrics
7. **Document findings** following the template structure

---

## Reference Commands Summary

```bash
# 1. Convert dataset (create convert_google_web.py first)
python convert_google_web.py

# 2. Run SPMiner
python3 -m subgraph_mining.decoder \
    --dataset=web-google.pkl \
    --graph_type=directed \
    --node_anchored \
    --out_path=results/web-google-patterns.pkl \
    --n_trials=1000 \
    --n_neighborhoods=10000 \
    --min_pattern_size=3 \
    --max_pattern_size=8 \
    --min_neighborhood_size=20 \
    --max_neighborhood_size=29 \
    --search_strategy=greedy \
    --out_batch_size=3

# 3. Count patterns
python3 -m analyze.count_patterns \
    --dataset=web-google.pkl \
    --queries_path=results/web-google-patterns.pkl \
    --out_path=results/web-google-counts.json \
    --node_anchored \
    --graph_type=directed \
    --n_workers=4 \
    --count_method=bin

# 4. Analyze counts
python3 -m analyze.analyze_pattern_counts \
    --counts_path=results/ \
    --out_path=results/web-google-analysis.csv
```


