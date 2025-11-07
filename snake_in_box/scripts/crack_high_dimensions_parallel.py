#!/usr/bin/env python3
"""Parallel comprehensive exhaustive search for dimensions 11-16.

This script performs exhaustive, validated searches for dimensions 11-16 using
multiple aggressive search strategies with comprehensive logging and progress saving.
Runs one independent process per dimension for parallel execution.

Strategies (per dimension):
1. Priming from known lower dimensions (N-1, N-2, N-3)
2. Direct pruned BFS search from empty snake
3. Multiple seed starting points (truncated snakes, various prefixes)

All results are validated and compared against known records.
Progress is saved periodically to allow resuming.
Comprehensive visualizations are generated after all processes complete.
"""

import sys
import os
import json
import logging
import time
import traceback
import multiprocessing as mp
from typing import Dict, List, Optional, Tuple
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Import all functions from the original script
from snake_in_box.scripts.crack_high_dimensions import (
    setup_logging,
    validate_and_log_snake,
    save_progress,
    load_progress,
    strategy_priming_from_lower_dimensions,
    strategy_direct_bfs_search,
    strategy_multiple_seeds,
    search_dimension,
    MEMORY_LIMIT_GB,
    MAX_LEVELS,
    OUTPUT_BASE,
    CRACK_RESULTS_DIR,
    CRACK_LOGS_DIR,
    TARGET_DIMENSIONS
)
from snake_in_box.core.snake_node import SnakeNode
from snake_in_box.benchmarks.known_snakes import get_known_record
from snake_in_box.utils.visualize_advanced import (
    visualize_snake_auto,
    visualize_snake_heatmap,
    visualize_snake_3d_projection,
    visualize_snake_transition_matrix,
)
from snake_in_box.utils.graphical_abstract import generate_16d_panel
from snake_in_box.utils.performance_plots import (
    plot_computation_time_vs_dimension,
)


# Configuration
CRACK_VISUALIZATIONS_DIR = f"{OUTPUT_BASE}/crack_visualizations"


def worker_search_dimension(
    dimension: int,
    memory_limit_gb: float,
    result_queue: mp.Queue,
    status_queue: mp.Queue
) -> None:
    """Worker function to run search for a single dimension in a separate process.
    
    Parameters
    ----------
    dimension : int
        Dimension to search
    memory_limit_gb : float
        Memory limit for searches
    result_queue : mp.Queue
        Queue to put results when complete
    status_queue : mp.Queue
        Queue to put status updates
    """
    process_id = mp.current_process().pid
    status_queue.put({
        'dimension': dimension,
        'process_id': process_id,
        'status': 'started',
        'timestamp': time.time()
    })
    
    try:
        # Run the search (this handles its own logging)
        result = search_dimension(dimension, memory_limit_gb)
        
        status_queue.put({
            'dimension': dimension,
            'process_id': process_id,
            'status': 'completed',
            'timestamp': time.time(),
            'length': result.get('best_length', 0)
        })
        
        # Put result in queue
        result_queue.put({
            'dimension': dimension,
            'result': result,
            'process_id': process_id
        })
        
    except Exception as e:
        error_msg = f"Error in process for dimension {dimension}: {e}"
        status_queue.put({
            'dimension': dimension,
            'process_id': process_id,
            'status': 'error',
            'timestamp': time.time(),
            'error': str(e)
        })
        
        # Log error
        logger = setup_logging(dimension)
        logger.error(error_msg)
        logger.debug(traceback.format_exc())
        
        # Put error result
        result_queue.put({
            'dimension': dimension,
            'result': {
                'dimension': dimension,
                'best_snake': None,
                'best_length': 0,
                'best_metadata': {},
                'best_strategy': None,
                'known_record': get_known_record(dimension),
                'is_new_record': False,
                'error': str(e)
            },
            'process_id': process_id,
            'error': True
        })


def monitor_processes(
    processes: List[mp.Process],
    status_queue: mp.Queue,
    num_dimensions: int
) -> None:
    """Monitor process status and print updates.
    
    Parameters
    ----------
    processes : List[mp.Process]
        List of running processes
    status_queue : mp.Queue
        Queue receiving status updates
    num_dimensions : int
        Total number of dimensions being processed
    """
    completed = set()
    started = set()
    
    print("\nMonitoring processes...")
    print("=" * 70)
    
    while len(completed) < num_dimensions:
        try:
            # Check for status updates (non-blocking)
            if not status_queue.empty():
                status = status_queue.get(timeout=0.1)
                dim = status['dimension']
                
                if status['status'] == 'started' and dim not in started:
                    started.add(dim)
                    print(f"[{time.strftime('%H:%M:%S')}] Dimension {dim}: Process started (PID: {status['process_id']})")
                
                elif status['status'] == 'completed' and dim not in completed:
                    completed.add(dim)
                    length = status.get('length', 0)
                    print(f"[{time.strftime('%H:%M:%S')}] Dimension {dim}: ✓ Completed (Length: {length})")
                
                elif status['status'] == 'error' and dim not in completed:
                    completed.add(dim)
                    error = status.get('error', 'Unknown error')
                    print(f"[{time.strftime('%H:%M:%S')}] Dimension {dim}: ✗ Error - {error}")
            
            # Check if processes are still alive
            for i, proc in enumerate(processes):
                if not proc.is_alive() and proc not in [p for p in processes if hasattr(p, '_completed')]:
                    # Process finished but we might not have gotten status yet
                    time.sleep(0.5)
            
            time.sleep(1)  # Check every second
            
        except Exception:
            # Queue might be empty, continue monitoring
            time.sleep(1)
    
    print("=" * 70)
    print("All processes completed\n")


def generate_comprehensive_visualizations(results: Dict[int, Dict]) -> None:
    """Generate comprehensive visualizations for all dimensions.
    
    Parameters
    ----------
    results : Dict[int, Dict]
        Results dictionary keyed by dimension
    """
    os.makedirs(CRACK_VISUALIZATIONS_DIR, exist_ok=True)
    
    print("\n" + "=" * 70)
    print("Generating comprehensive visualizations...")
    print("=" * 70)
    
    snake_nodes = {}
    visualization_stats = {
        'auto': 0,
        'heatmap': 0,
        '3d': 0,
        'transitions': 0,
        'errors': 0
    }
    
    # Generate individual visualizations for each dimension
    for dim in sorted(results.keys()):
        result = results[dim]
        best_snake = result.get('best_snake')
        
        if not best_snake:
            print(f"  Dimension {dim}: No snake to visualize")
            continue
        
        print(f"\n  Dimension {dim} (Length: {best_snake.get_length()})...")
        snake_nodes[dim] = best_snake
        
        # Auto visualization
        try:
            fig = visualize_snake_auto(best_snake, show_plot=False)
            if fig:
                fig.savefig(
                    f"{CRACK_VISUALIZATIONS_DIR}/dimension_{dim:02d}_auto.png",
                    dpi=300,
                    bbox_inches='tight'
                )
                import matplotlib.pyplot as plt
                plt.close(fig)
                visualization_stats['auto'] += 1
                print(f"    ✓ Auto visualization")
        except Exception as e:
            print(f"    ✗ Auto visualization failed: {e}")
            visualization_stats['errors'] += 1
        
        # Heatmap (for dimensions >= 4)
        if dim >= 4:
            try:
                fig = visualize_snake_heatmap(best_snake, show_plot=False)
                if fig:
                    fig.savefig(
                        f"{CRACK_VISUALIZATIONS_DIR}/dimension_{dim:02d}_heatmap.png",
                        dpi=300,
                        bbox_inches='tight'
                    )
                    import matplotlib.pyplot as plt
                    plt.close(fig)
                    visualization_stats['heatmap'] += 1
                    print(f"    ✓ Heatmap")
            except Exception as e:
                print(f"    ✗ Heatmap failed: {e}")
                visualization_stats['errors'] += 1
        
        # 3D projection (for dimensions >= 4)
        if dim >= 4:
            try:
                fig = visualize_snake_3d_projection(best_snake, show_plot=False)
                if fig:
                    fig.savefig(
                        f"{CRACK_VISUALIZATIONS_DIR}/dimension_{dim:02d}_3d.png",
                        dpi=300,
                        bbox_inches='tight'
                    )
                    import matplotlib.pyplot as plt
                    plt.close(fig)
                    visualization_stats['3d'] += 1
                    print(f"    ✓ 3D projection")
            except Exception as e:
                print(f"    ✗ 3D projection failed: {e}")
                visualization_stats['errors'] += 1
        
        # Transition matrix (for all dimensions)
        try:
            fig = visualize_snake_transition_matrix(best_snake, show_plot=False)
            if fig:
                fig.savefig(
                    f"{CRACK_VISUALIZATIONS_DIR}/dimension_{dim:02d}_transitions.png",
                    dpi=300,
                    bbox_inches='tight'
                )
                import matplotlib.pyplot as plt
                plt.close(fig)
                visualization_stats['transitions'] += 1
                print(f"    ✓ Transition matrix")
        except Exception as e:
            print(f"    ✗ Transition matrix failed: {e}")
            visualization_stats['errors'] += 1
    
    # Generate combined panel if we have multiple dimensions
    if len(snake_nodes) >= 2:
        print(f"\n  Generating combined panel for {len(snake_nodes)} dimensions...")
        try:
            fig = generate_16d_panel(
                snake_nodes,
                output_file=f"{CRACK_VISUALIZATIONS_DIR}/combined_panel.png",
                figsize=(20, 20),
                dpi=300
            )
            if fig:
                import matplotlib.pyplot as plt
                plt.close(fig)
                print(f"    ✓ Combined panel")
        except Exception as e:
            print(f"    ✗ Combined panel failed: {e}")
            visualization_stats['errors'] += 1
    
    # Generate performance comparison plot
    print(f"\n  Generating performance comparison...")
    try:
        # Extract computation times from metadata
        times_dict = {}
        for dim, result in results.items():
            metadata = result.get('best_metadata', {})
            elapsed = metadata.get('elapsed_seconds', 0)
            if elapsed > 0:
                times_dict[dim] = elapsed
        
        if times_dict:
            plot_computation_time_vs_dimension(
                times_dict,
                f"{CRACK_VISUALIZATIONS_DIR}/performance_comparison.png"
            )
            print(f"    ✓ Performance comparison")
    except Exception as e:
        print(f"    ✗ Performance comparison failed: {e}")
        visualization_stats['errors'] += 1
    
    print("\n" + "=" * 70)
    print("Visualization Summary:")
    print(f"  Auto visualizations: {visualization_stats['auto']}")
    print(f"  Heatmaps: {visualization_stats['heatmap']}")
    print(f"  3D projections: {visualization_stats['3d']}")
    print(f"  Transition matrices: {visualization_stats['transitions']}")
    print(f"  Errors: {visualization_stats['errors']}")
    print(f"\nVisualizations saved to: {CRACK_VISUALIZATIONS_DIR}/")
    print("=" * 70)


def generate_summary_report(results: Dict[int, Dict]) -> None:
    """Generate summary report of all searches.
    
    Parameters
    ----------
    results : Dict[int, Dict]
        Results dictionary keyed by dimension
    """
    os.makedirs(CRACK_RESULTS_DIR, exist_ok=True)
    
    report_lines = [
        "# Parallel Comprehensive Search Results for Dimensions 11-16",
        "",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Execution Mode: Parallel (one process per dimension)",
        "",
        "## Summary",
        ""
    ]
    
    for dim in sorted(results.keys()):
        result = results[dim]
        best_length = result.get('best_length', 0)
        known_record = result.get('known_record')
        is_new_record = result.get('is_new_record', False)
        strategy = result.get('best_strategy', 'none')
        has_error = result.get('error') is not None
        
        report_lines.append(f"### Dimension {dim}")
        report_lines.append("")
        
        if has_error:
            report_lines.append(f"- **Status**: ✗ Error - {result.get('error', 'Unknown error')}")
        else:
            report_lines.append(f"- **Best length found**: {best_length}")
            report_lines.append(f"- **Known record**: {known_record if known_record else 'None'}")
            
            if known_record:
                if is_new_record:
                    improvement = best_length - known_record
                    report_lines.append(
                        f"- **Status**: ⭐ **NEW RECORD** (+{improvement})"
                    )
                elif best_length == known_record:
                    report_lines.append("- **Status**: ✓ Matched record")
                else:
                    diff = known_record - best_length
                    report_lines.append(f"- **Status**: Below record (difference: {diff})")
            else:
                report_lines.append("- **Status**: No known record for comparison")
            
            report_lines.append(f"- **Strategy**: {strategy}")
        
        report_lines.append("")
    
    report_lines.extend([
        "## Details",
        ""
    ])
    
    for dim in sorted(results.keys()):
        result = results[dim]
        report_lines.append(f"### Dimension {dim}")
        report_lines.append("")
        report_lines.append("```json")
        report_lines.append(json.dumps(result.get('best_metadata', {}), indent=2))
        report_lines.append("```")
        report_lines.append("")
    
    report_content = "\n".join(report_lines)
    
    report_file = f"{CRACK_RESULTS_DIR}/summary_report_parallel.md"
    try:
        with open(report_file, 'w') as f:
            f.write(report_content)
        print(f"\n✓ Summary report saved to: {report_file}")
        
        # Verify file was created
        if os.path.exists(report_file):
            file_size = os.path.getsize(report_file)
            print(f"  Report file size: {file_size} bytes")
        else:
            print(f"  ⚠ WARNING: Report file was not created!")
    except Exception as e:
        print(f"\n✗ ERROR: Failed to save summary report: {e}")
        traceback.print_exc()


def main():
    """Main function to orchestrate parallel searches for all target dimensions."""
    print("=" * 70)
    print("PARALLEL COMPREHENSIVE SEARCH FOR DIMENSIONS 11-16")
    print("=" * 70)
    print(f"Target dimensions: {TARGET_DIMENSIONS}")
    print(f"Number of processes: {len(TARGET_DIMENSIONS)}")
    print(f"Memory limit per process: {MEMORY_LIMIT_GB} GB")
    print(f"Max levels: {MAX_LEVELS}")
    print(f"Output directory: {OUTPUT_BASE}/")
    print("")
    
    # Create output directories
    os.makedirs(CRACK_RESULTS_DIR, exist_ok=True)
    os.makedirs(CRACK_LOGS_DIR, exist_ok=True)
    os.makedirs(CRACK_VISUALIZATIONS_DIR, exist_ok=True)
    
    # Set up multiprocessing
    mp.set_start_method('spawn', force=True)  # Use spawn for better isolation
    
    # Create queues for communication
    result_queue = mp.Queue()
    status_queue = mp.Queue()
    
    # Create and start processes
    processes = []
    start_time = time.time()
    
    print("Starting processes...")
    for dimension in TARGET_DIMENSIONS:
        proc = mp.Process(
            target=worker_search_dimension,
            args=(dimension, MEMORY_LIMIT_GB, result_queue, status_queue)
        )
        proc.start()
        processes.append(proc)
        print(f"  Started process for dimension {dimension} (PID: {proc.pid})")
    
    print(f"\nAll {len(processes)} processes started")
    print("=" * 70)
    
    # Monitor processes
    try:
        monitor_processes(processes, status_queue, len(TARGET_DIMENSIONS))
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Terminating all processes...")
        for proc in processes:
            proc.terminate()
            proc.join(timeout=5)
            if proc.is_alive():
                proc.kill()
        print("All processes terminated.")
        return
    
    # Wait for all processes to complete
    for proc in processes:
        proc.join()
    
    elapsed_time = time.time() - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds ({elapsed_time/3600:.2f} hours)")
    
    # Collect results
    print("\n" + "=" * 70)
    print("Collecting results...")
    print("=" * 70)
    
    results = {}
    collected_count = 0
    max_wait_time = 300  # 5 minutes max wait per result
    start_collect_time = time.time()
    
    for i in range(len(TARGET_DIMENSIONS)):
        try:
            # Wait longer for results, with timeout
            item = result_queue.get(timeout=max_wait_time)
            dimension = item['dimension']
            result = item['result']
            results[dimension] = result
            collected_count += 1
            
            best_length = result.get('best_length', 0)
            known_record = result.get('known_record')
            is_new_record = result.get('is_new_record', False)
            has_error = result.get('error') is not None
            
            print(f"\nDimension {dimension}:")
            if has_error:
                print(f"  ✗ Error: {result.get('error')}")
            else:
                print(f"  Best length: {best_length}")
                print(f"  Known record: {known_record}")
                if is_new_record:
                    print(f"  *** NEW RECORD FOUND ***")
                print(f"  Strategy: {result.get('best_strategy', 'none')}")
        except Exception as e:
            print(f"  ⚠ Timeout or error collecting result for dimension {TARGET_DIMENSIONS[i]}: {e}")
            # Try to get any remaining results without timeout
            while not result_queue.empty():
                try:
                    item = result_queue.get_nowait()
                    dimension = item['dimension']
                    result = item['result']
                    results[dimension] = result
                    collected_count += 1
                    print(f"  ✓ Collected late result for dimension {dimension}")
                except:
                    break
    
    print(f"\nCollected {collected_count} out of {len(TARGET_DIMENSIONS)} results")
    if collected_count < len(TARGET_DIMENSIONS):
        missing = set(TARGET_DIMENSIONS) - set(results.keys())
        print(f"  ⚠ Missing results for dimensions: {sorted(missing)}")
    
    # Generate summary report (always attempt, even if results is empty)
    print("\n" + "=" * 70)
    print("Generating summary report...")
    print("=" * 70)
    try:
        if results:
            generate_summary_report(results)
        else:
            print("⚠ WARNING: No results to report. Creating empty report.")
            # Create a minimal report indicating no results
            report_file = f"{CRACK_RESULTS_DIR}/summary_report_parallel.md"
            with open(report_file, 'w') as f:
                f.write(f"# Parallel Comprehensive Search Results for Dimensions 11-16\n\n")
                f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("## Status\n\n")
                f.write("⚠ No results were collected from the parallel search.\n")
                f.write("This may indicate all processes failed or results were not properly collected.\n")
            print(f"  Created empty report at: {report_file}")
    except Exception as e:
        print(f"✗ ERROR: Failed to generate summary report: {e}")
        traceback.print_exc()
    
    # Generate comprehensive visualizations (always attempt)
    print("\n" + "=" * 70)
    print("Generating comprehensive visualizations...")
    print("=" * 70)
    try:
        if results:
            generate_comprehensive_visualizations(results)
        else:
            print("⚠ WARNING: No results available for visualization generation.")
    except Exception as e:
        print(f"✗ ERROR: Failed to generate visualizations: {e}")
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("ALL SEARCHES COMPLETE")
    print("=" * 70)
    print(f"\nResults saved to: {CRACK_RESULTS_DIR}/")
    print(f"Logs saved to: {CRACK_LOGS_DIR}/")
    print(f"Visualizations saved to: {CRACK_VISUALIZATIONS_DIR}/")
    print(f"\nTotal time: {elapsed_time:.2f} seconds ({elapsed_time/3600:.2f} hours)")


if __name__ == "__main__":
    main()

