"""
Convert Stanford SNAP web-Google dataset to NetworkX DiGraph pickle format
for use with SPMiner.

Usage:
    python convert_google_web.py --input web-Google.txt --output web-google.pkl
"""

import argparse
import networkx as nx
import pickle
import gzip
import os
from tqdm import tqdm

def convert_snap_to_networkx(input_file, output_file, use_gzip=False):
    """
    Convert SNAP format edge list to NetworkX DiGraph pickle file.
    
    Args:
        input_file: Path to SNAP format file (web-Google.txt)
        output_file: Output path for pickle file
        use_gzip: Whether input file is gzipped
    """
    print(f"Reading graph from {input_file}...")
    
    graph = nx.DiGraph()
    
    # Open file (handle gzip if needed)
    opener = gzip.open if use_gzip or input_file.endswith('.gz') else open
    mode = 'rt' if use_gzip or input_file.endswith('.gz') else 'r'
    
    with opener(input_file, mode) as f:
        # First pass: count edges for progress bar
        lines = f.readlines()
        total_lines = len([l for l in lines if not l.strip().startswith('#')])
        
        # Reset file pointer
        f.seek(0)
        
        # Second pass: build graph
        edge_count = 0
        for line in tqdm(f, total=total_lines, desc="Processing edges"):
            # Skip comments
            if line.strip().startswith('#'):
                continue
            
            # Parse edge
            parts = line.strip().split('\t')
            if len(parts) < 2:
                parts = line.strip().split()
                if len(parts) < 2:
                    continue
            
            try:
                source = int(parts[0])
                target = int(parts[1])
                
                # Add edge (NetworkX handles duplicate edges automatically)
                graph.add_edge(source, target)
                
                # Add node attributes (required by SPMiner)
                if 'id' not in graph.nodes[source]:
                    graph.nodes[source]['id'] = str(source)
                    graph.nodes[source]['label'] = str(source)
                if 'id' not in graph.nodes[target]:
                    graph.nodes[target]['id'] = str(target)
                    graph.nodes[target]['label'] = str(target)
                
                edge_count += 1
                
            except (ValueError, IndexError) as e:
                print(f"Warning: Skipping malformed line: {line.strip()} ({e})")
                continue
    
    print(f"\nGraph created:")
    print(f"  Nodes: {graph.number_of_nodes():,}")
    print(f"  Edges: {graph.number_of_edges():,}")
    
    # Compute basic statistics
    if graph.number_of_nodes() > 0:
        in_degrees = [d for n, d in graph.in_degree()]
        out_degrees = [d for n, d in graph.out_degree()]
        
        print(f"  Average in-degree: {sum(in_degrees) / len(in_degrees):.2f}")
        print(f"  Average out-degree: {sum(out_degrees) / len(out_degrees):.2f}")
        print(f"  Max in-degree: {max(in_degrees)}")
        print(f"  Max out-degree: {max(out_degrees)}")
        
        # Check connectivity (sample-based for large graphs)
        if graph.number_of_nodes() < 100000:
            wcc = list(nx.weakly_connected_components(graph))
            scc = list(nx.strongly_connected_components(graph))
            largest_wcc = max(wcc, key=len)
            largest_scc = max(scc, key=len)
            
            print(f"  Weakly connected components: {len(wcc)}")
            print(f"  Largest WCC size: {len(largest_wcc):,} ({100*len(largest_wcc)/graph.number_of_nodes():.1f}%)")
            print(f"  Strongly connected components: {len(scc)}")
            print(f"  Largest SCC size: {len(largest_scc):,} ({100*len(largest_scc)/graph.number_of_nodes():.1f}%)")
        else:
            print("  (Skipping connectivity analysis for large graph)")
    
    # Save graph
    print(f"\nSaving graph to {output_file}...")
    with open(output_file, 'wb') as f:
        pickle.dump(graph, f)
    
    print(f"✓ Graph saved successfully!")
    print(f"  File size: {os.path.getsize(output_file) / (1024**2):.2f} MB")
    
    return graph

def main():
    parser = argparse.ArgumentParser(
        description='Convert SNAP web-Google dataset to NetworkX pickle format'
    )
    parser.add_argument(
        '--input',
        type=str,
        default='web-Google.txt',
        help='Input SNAP format file (default: web-Google.txt)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='web-google.pkl',
        help='Output pickle file (default: web-google.pkl)'
    )
    parser.add_argument(
        '--gzip',
        action='store_true',
        help='Input file is gzipped'
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found!")
        print("\nPlease download the dataset from:")
        print("https://snap.stanford.edu/data/web-Google.html")
        return
    
    try:
        graph = convert_snap_to_networkx(args.input, args.output, args.gzip)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == '__main__':
    main()

