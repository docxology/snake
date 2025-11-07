#!/usr/bin/env python3
"""Comprehensive exhaustive search for dimensions 11-16.

This script performs exhaustive, validated searches for dimensions 11-16 using
multiple aggressive search strategies with comprehensive logging and progress saving.

Strategies:
1. Priming from known lower dimensions (N-1, N-2, N-3)
2. Direct pruned BFS search from empty snake
3. Multiple seed starting points (truncated snakes, various prefixes)

All results are validated and compared against known records.
Progress is saved periodically to allow resuming.
"""

import sys
import os
import json
import logging
import time
import traceback
from typing import Dict, List, Optional, Tuple
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from snake_in_box.core.snake_node import SnakeNode
from snake_in_box.core.validation import validate_transition_sequence
from snake_in_box.search.bfs_pruned import pruned_bfs_search
from snake_in_box.search.priming import prime_search, pruned_bfs_search_from_seed
from snake_in_box.benchmarks.known_snakes import (
    get_known_snake,
    get_known_record,
    KNOWN_RECORDS
)


# Configuration
TARGET_DIMENSIONS = [11, 12, 13, 14, 15, 16]
MEMORY_LIMIT_GB = 50.0
MAX_LEVELS = 200000
OUTPUT_BASE = "output"
CRACK_RESULTS_DIR = f"{OUTPUT_BASE}/crack_results"
CRACK_LOGS_DIR = f"{OUTPUT_BASE}/crack_logs"


def setup_logging(dimension: int) -> logging.Logger:
    """Set up logging for a specific dimension.
    
    Creates both file and console handlers with comprehensive formatting.
    
    Parameters
    ----------
    dimension : int
        Dimension being searched
    
    Returns
    -------
    logging.Logger
        Configured logger instance
    """
    logger = logging.getLogger(f"crack_dim_{dimension}")
    logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers
    logger.handlers = []
    
    # File handler
    os.makedirs(CRACK_LOGS_DIR, exist_ok=True)
    file_handler = logging.FileHandler(
        f"{CRACK_LOGS_DIR}/dimension_{dimension}.log",
        mode='a'
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger


def validate_and_log_snake(
    transition_sequence: List[int],
    dimension: int,
    logger: logging.Logger,
    method: str = "unknown"
) -> Tuple[bool, Optional[SnakeNode], Dict]:
    """Validate a snake and log the results.
    
    Parameters
    ----------
    transition_sequence : List[int]
        Transition sequence to validate
    dimension : int
        Dimension of hypercube
    logger : logging.Logger
        Logger instance
    method : str
        Method used to find this snake
    
    Returns
    -------
    Tuple[bool, Optional[SnakeNode], Dict]
        (is_valid, snake_node, metadata)
    """
    if not transition_sequence:
        logger.warning(f"Empty transition sequence from {method}")
        return False, None, {'error': 'Empty sequence'}
    
    # Validate
    is_valid, validation_msg = validate_transition_sequence(
        transition_sequence,
        dimension
    )
    
    if not is_valid:
        logger.error(
            f"Invalid snake from {method}: {validation_msg}\n"
            f"  Length: {len(transition_sequence)}\n"
            f"  First 20 transitions: {transition_sequence[:20]}"
        )
        return False, None, {'error': validation_msg, 'method': method}
    
    # Create SnakeNode
    try:
        snake_node = SnakeNode(transition_sequence, dimension)
        length = snake_node.get_length()
        
        # Compare with known record
        known_record = get_known_record(dimension)
        is_new_record = False
        if known_record:
            if length > known_record:
                is_new_record = True
                logger.critical(
                    f"*** NEW RECORD FOUND ***\n"
                    f"  Dimension: {dimension}\n"
                    f"  Length: {length} (previous record: {known_record})\n"
                    f"  Method: {method}\n"
                    f"  Improvement: +{length - known_record}"
                )
            elif length == known_record:
                logger.info(
                    f"Matched known record: {length} (method: {method})"
                )
            else:
                logger.info(
                    f"Found snake length {length} (record: {known_record}, "
                    f"method: {method})"
                )
        else:
            logger.info(
                f"Found snake length {length} (no known record, method: {method})"
            )
        
        metadata = {
            'is_valid': True,
            'length': length,
            'method': method,
            'known_record': known_record,
            'is_new_record': is_new_record,
            'validation_msg': validation_msg
        }
        
        return True, snake_node, metadata
        
    except Exception as e:
        logger.error(f"Error creating SnakeNode from {method}: {e}")
        logger.debug(traceback.format_exc())
        return False, None, {'error': str(e), 'method': method}


def save_progress(
    dimension: int,
    best_snake: Optional[SnakeNode],
    metadata: Dict,
    strategy: str
) -> None:
    """Save progress to JSON file.
    
    Parameters
    ----------
    dimension : int
        Dimension being searched
    best_snake : Optional[SnakeNode]
        Best snake found so far
    metadata : Dict
        Metadata about the search
    strategy : str
        Strategy that found this snake
    """
    os.makedirs(CRACK_RESULTS_DIR, exist_ok=True)
    
    result = {
        'dimension': dimension,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'strategy': strategy,
        'length': best_snake.get_length() if best_snake else 0,
        'transition_sequence': (
            best_snake.transition_sequence if best_snake else []
        ),
        'metadata': metadata,
        'known_record': get_known_record(dimension),
        'is_new_record': metadata.get('is_new_record', False)
    }
    
    filename = f"{CRACK_RESULTS_DIR}/dimension_{dimension}_best.json"
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2)
    
    # Also save a backup with timestamp
    backup_filename = (
        f"{CRACK_RESULTS_DIR}/dimension_{dimension}_"
        f"{time.strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(backup_filename, 'w') as f:
        json.dump(result, f, indent=2)


def load_progress(dimension: int) -> Optional[Dict]:
    """Load saved progress for a dimension.
    
    Parameters
    ----------
    dimension : int
        Dimension to load progress for
    
    Returns
    -------
    Optional[Dict]
        Saved progress data, or None if not found
    """
    filename = f"{CRACK_RESULTS_DIR}/dimension_{dimension}_best.json"
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except Exception:
            return None
    return None


def strategy_priming_from_lower_dimensions(
    dimension: int,
    logger: logging.Logger,
    memory_limit_gb: float
) -> Tuple[Optional[SnakeNode], Dict]:
    """Strategy 1: Priming from known lower dimensions.
    
    Tries extending from dimensions N-1, N-2, N-3 (if available).
    
    Parameters
    ----------
    dimension : int
        Target dimension
    logger : logging.Logger
        Logger instance
    memory_limit_gb : float
        Memory limit for search
    
    Returns
    -------
    Tuple[Optional[SnakeNode], Dict]
        (best_snake, metadata)
    """
    logger.info("=" * 70)
    logger.info(f"STRATEGY 1: Priming from lower dimensions (target: {dimension})")
    logger.info("=" * 70)
    
    best_snake = None
    best_length = 0
    best_metadata = {}
    
    # Try extending from N-1, N-2, N-3
    seed_dimensions = []
    for offset in [1, 2, 3]:
        seed_dim = dimension - offset
        if seed_dim >= 9 and seed_dim in KNOWN_RECORDS:
            seed_dimensions.append(seed_dim)
    
    if not seed_dimensions:
        logger.warning("No known lower dimensions available for priming")
        return None, {'error': 'No seed dimensions available'}
    
    for seed_dim in seed_dimensions:
        logger.info(f"\nAttempting to extend from dimension {seed_dim} to {dimension}")
        
        seed_seq = get_known_snake(seed_dim)
        if not seed_seq:
            logger.warning(f"Could not retrieve known snake for dimension {seed_dim}")
            continue
        
        logger.info(
            f"  Seed snake length: {len(seed_seq)}\n"
            f"  Known record for {seed_dim}: {get_known_record(seed_dim)}"
        )
        
        start_time = time.time()
        try:
            # Use aggressive parameters for high dimensions
            extended_seq = prime_search(
                lower_dimension_snake=seed_seq,
                target_dimension=dimension,
                memory_limit_gb=memory_limit_gb,
                verbose=True
            )
            
            elapsed = time.time() - start_time
            
            if extended_seq and len(extended_seq) >= len(seed_seq):
                # Validate the result
                is_valid, snake_node, metadata = validate_and_log_snake(
                    extended_seq,
                    dimension,
                    logger,
                    f"priming_from_{seed_dim}"
                )
                
                if is_valid and snake_node:
                    length = snake_node.get_length()
                    extension = length - len(seed_seq)
                    
                    logger.info(
                        f"  ✓ Extended from {seed_dim}D: "
                        f"{len(seed_seq)} → {length} (+{extension})\n"
                        f"  Time: {elapsed:.2f}s"
                    )
                    
                    if length > best_length:
                        best_length = length
                        best_snake = snake_node
                        best_metadata = {
                            **metadata,
                            'seed_dimension': seed_dim,
                            'seed_length': len(seed_seq),
                            'extension': extension,
                            'elapsed_seconds': elapsed
                        }
                else:
                    logger.warning(
                        f"  ✗ Extension from {seed_dim}D produced invalid snake"
                    )
            else:
                logger.warning(
                    f"  ✗ Failed to extend from {seed_dim}D "
                    f"(elapsed: {elapsed:.2f}s)"
                )
                
        except Exception as e:
            logger.error(f"  ✗ Error extending from {seed_dim}D: {e}")
            logger.debug(traceback.format_exc())
    
    if best_snake:
        logger.info(
            f"\nStrategy 1 best result: length {best_length} "
            f"(from dimension {best_metadata.get('seed_dimension', 'unknown')})"
        )
    else:
        logger.warning("\nStrategy 1: No valid snakes found")
    
    return best_snake, best_metadata


def strategy_direct_bfs_search(
    dimension: int,
    logger: logging.Logger,
    memory_limit_gb: float
) -> Tuple[Optional[SnakeNode], Dict]:
    """Strategy 2: Direct pruned BFS search from empty snake.
    
    Parameters
    ----------
    dimension : int
        Target dimension
    logger : logging.Logger
        Logger instance
    memory_limit_gb : float
        Memory limit for search
    
    Returns
    -------
    Tuple[Optional[SnakeNode], Dict]
        (best_snake, metadata)
    """
    logger.info("=" * 70)
    logger.info(f"STRATEGY 2: Direct pruned BFS search (dimension {dimension})")
    logger.info("=" * 70)
    
    logger.info("Starting search from empty snake...")
    start_time = time.time()
    
    try:
        snake_node = pruned_bfs_search(
            dimension=dimension,
            memory_limit_gb=memory_limit_gb,
            verbose=True
        )
        
        elapsed = time.time() - start_time
        
        if snake_node:
            length = snake_node.get_length()
            
            # Validate
            is_valid, validation_msg = validate_transition_sequence(
                snake_node.transition_sequence,
                dimension
            )
            
            if is_valid:
                logger.info(
                    f"  ✓ Direct search found snake of length {length}\n"
                    f"  Time: {elapsed:.2f}s"
                )
                
                metadata = {
                    'is_valid': True,
                    'length': length,
                    'method': 'direct_bfs',
                    'elapsed_seconds': elapsed,
                    'known_record': get_known_record(dimension),
                    'is_new_record': (
                        get_known_record(dimension) is not None and
                        length > get_known_record(dimension)
                    )
                }
                
                return snake_node, metadata
            else:
                logger.error(
                    f"  ✗ Direct search produced invalid snake: {validation_msg}"
                )
                return None, {'error': validation_msg}
        else:
            logger.warning(f"  ✗ Direct search failed (elapsed: {elapsed:.2f}s)")
            return None, {'error': 'Search returned None'}
            
    except Exception as e:
        logger.error(f"  ✗ Error in direct search: {e}")
        logger.debug(traceback.format_exc())
        return None, {'error': str(e)}


def strategy_multiple_seeds(
    dimension: int,
    logger: logging.Logger,
    memory_limit_gb: float
) -> Tuple[Optional[SnakeNode], Dict]:
    """Strategy 3: Multiple seed starting points.
    
    Tries truncating known snakes at various points and searching from there.
    
    Parameters
    ----------
    dimension : int
        Target dimension
    logger : logging.Logger
        Logger instance
    memory_limit_gb : float
        Memory limit for search
    
    Returns
    -------
    Tuple[Optional[SnakeNode], Dict]
        (best_snake, metadata)
    """
    logger.info("=" * 70)
    logger.info(f"STRATEGY 3: Multiple seed starting points (dimension {dimension})")
    logger.info("=" * 70)
    
    best_snake = None
    best_length = 0
    best_metadata = {}
    
    # Get known snakes from lower dimensions to use as seeds
    seed_dimensions = []
    for offset in [1, 2, 3]:
        seed_dim = dimension - offset
        if seed_dim >= 9 and seed_dim in KNOWN_RECORDS:
            seed_dimensions.append(seed_dim)
    
    if not seed_dimensions:
        logger.warning("No known lower dimensions available for seed strategy")
        return None, {'error': 'No seed dimensions available'}
    
    # Try various truncation points
    truncation_ratios = [0.99, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
    fixed_lengths = [1000, 500, 200, 100, 50, 20, 10]
    
    for seed_dim in seed_dimensions:
        logger.info(f"\nTrying seeds from dimension {seed_dim}")
        
        seed_seq = get_known_snake(seed_dim)
        if not seed_seq:
            continue
        
        seed_length = len(seed_seq)
        logger.info(f"  Full seed length: {seed_length}")
        
        # Try ratio-based truncations
        for ratio in truncation_ratios:
            prefix_len = max(1, int(seed_length * ratio))
            if prefix_len >= seed_length:
                continue
            
            logger.info(f"  Trying prefix of length {prefix_len} ({ratio:.0%} of seed)")
            
            try:
                prefix_seq = seed_seq[:prefix_len]
                seed_node = SnakeNode(prefix_seq, dimension)
                
                # Check if this seed can extend
                from snake_in_box.utils.canonical import get_legal_next_dimensions
                legal_dims = get_legal_next_dimensions(prefix_seq)
                new_dim = dimension - 1
                if new_dim not in legal_dims and new_dim < dimension:
                    legal_dims = list(legal_dims) + [new_dim]
                
                can_extend = any(
                    seed_node.can_extend(d) for d in legal_dims if d < dimension
                )
                
                if not can_extend:
                    logger.debug(f"    Prefix {prefix_len} cannot extend, skipping")
                    continue
                
                # Search from this seed
                start_time = time.time()
                extended_node = pruned_bfs_search_from_seed(
                    seed_node=seed_node,
                    dimension=dimension,
                    memory_limit_gb=memory_limit_gb,
                    max_levels=MAX_LEVELS,
                    min_extension=1,
                    verbose=False
                )
                elapsed = time.time() - start_time
                
                if extended_node:
                    ext_length = extended_node.get_length()
                    extension = ext_length - prefix_len
                    
                    # Validate
                    is_valid, snake_node, metadata = validate_and_log_snake(
                        extended_node.transition_sequence,
                        dimension,
                        logger,
                        f"seed_{seed_dim}_prefix_{prefix_len}"
                    )
                    
                    if is_valid and snake_node:
                        logger.info(
                            f"    ✓ Extended from prefix {prefix_len}: "
                            f"{prefix_len} → {ext_length} (+{extension})\n"
                            f"    Time: {elapsed:.2f}s"
                        )
                        
                        if ext_length > best_length:
                            best_length = ext_length
                            best_snake = snake_node
                            best_metadata = {
                                **metadata,
                                'seed_dimension': seed_dim,
                                'prefix_length': prefix_len,
                                'prefix_ratio': ratio,
                                'extension': extension,
                                'elapsed_seconds': elapsed
                            }
                
            except Exception as e:
                logger.debug(f"    Error with prefix {prefix_len}: {e}")
                continue
        
        # Try fixed-length prefixes
        for fixed_len in fixed_lengths:
            if fixed_len >= seed_length:
                continue
            
            if fixed_len in [int(seed_length * r) for r in truncation_ratios]:
                continue  # Already tried
            
            logger.info(f"  Trying fixed prefix of length {fixed_len}")
            
            try:
                prefix_seq = seed_seq[:fixed_len]
                seed_node = SnakeNode(prefix_seq, dimension)
                
                from snake_in_box.utils.canonical import get_legal_next_dimensions
                legal_dims = get_legal_next_dimensions(prefix_seq)
                new_dim = dimension - 1
                if new_dim not in legal_dims and new_dim < dimension:
                    legal_dims = list(legal_dims) + [new_dim]
                
                can_extend = any(
                    seed_node.can_extend(d) for d in legal_dims if d < dimension
                )
                
                if not can_extend:
                    continue
                
                start_time = time.time()
                extended_node = pruned_bfs_search_from_seed(
                    seed_node=seed_node,
                    dimension=dimension,
                    memory_limit_gb=memory_limit_gb,
                    max_levels=MAX_LEVELS,
                    min_extension=1,
                    verbose=False
                )
                elapsed = time.time() - start_time
                
                if extended_node:
                    ext_length = extended_node.get_length()
                    extension = ext_length - fixed_len
                    
                    is_valid, snake_node, metadata = validate_and_log_snake(
                        extended_node.transition_sequence,
                        dimension,
                        logger,
                        f"seed_{seed_dim}_fixed_{fixed_len}"
                    )
                    
                    if is_valid and snake_node:
                        logger.info(
                            f"    ✓ Extended from fixed prefix {fixed_len}: "
                            f"{fixed_len} → {ext_length} (+{extension})\n"
                            f"    Time: {elapsed:.2f}s"
                        )
                        
                        if ext_length > best_length:
                            best_length = ext_length
                            best_snake = snake_node
                            best_metadata = {
                                **metadata,
                                'seed_dimension': seed_dim,
                                'prefix_length': fixed_len,
                                'prefix_ratio': fixed_len / seed_length,
                                'extension': extension,
                                'elapsed_seconds': elapsed
                            }
                
            except Exception as e:
                logger.debug(f"    Error with fixed prefix {fixed_len}: {e}")
                continue
    
    if best_snake:
        logger.info(
            f"\nStrategy 3 best result: length {best_length} "
            f"(from dimension {best_metadata.get('seed_dimension', 'unknown')}, "
            f"prefix length {best_metadata.get('prefix_length', 'unknown')})"
        )
    else:
        logger.warning("\nStrategy 3: No valid snakes found")
    
    return best_snake, best_metadata


def search_dimension(
    dimension: int,
    memory_limit_gb: float = MEMORY_LIMIT_GB
) -> Dict:
    """Run all search strategies for a single dimension.
    
    Parameters
    ----------
    dimension : int
        Dimension to search
    memory_limit_gb : float
        Memory limit for searches
    
    Returns
    -------
    Dict
        Results dictionary with best snake and metadata
    """
    logger = setup_logging(dimension)
    
    logger.info("=" * 70)
    logger.info(f"COMPREHENSIVE SEARCH FOR DIMENSION {dimension}")
    logger.info("=" * 70)
    logger.info(f"Memory limit: {memory_limit_gb} GB")
    logger.info(f"Max levels: {MAX_LEVELS}")
    logger.info(f"Known record: {get_known_record(dimension)}")
    logger.info("")
    
    # Load existing progress
    saved_progress = load_progress(dimension)
    best_snake = None
    best_length = 0
    best_metadata = {}
    best_strategy = None
    
    if saved_progress:
        logger.info(f"Found saved progress: length {saved_progress.get('length', 0)}")
        try:
            saved_seq = saved_progress.get('transition_sequence', [])
            if saved_seq:
                is_valid, snake_node, metadata = validate_and_log_snake(
                    saved_seq,
                    dimension,
                    logger,
                    "saved_progress"
                )
                if is_valid and snake_node:
                    best_snake = snake_node
                    best_length = snake_node.get_length()
                    best_metadata = saved_progress.get('metadata', {})
                    best_strategy = saved_progress.get('strategy', 'saved')
                    logger.info(f"Loaded saved snake: length {best_length}")
        except Exception as e:
            logger.warning(f"Could not load saved progress: {e}")
    
    # Strategy 1: Priming from lower dimensions
    logger.info("\n" + "=" * 70)
    logger.info("STARTING STRATEGY 1")
    logger.info("=" * 70)
    snake1, metadata1 = strategy_priming_from_lower_dimensions(
        dimension,
        logger,
        memory_limit_gb
    )
    if snake1 and snake1.get_length() > best_length:
        best_snake = snake1
        best_length = snake1.get_length()
        best_metadata = metadata1
        best_strategy = "priming_from_lower_dimensions"
        save_progress(dimension, best_snake, best_metadata, best_strategy)
        logger.info(f"New best: {best_length} (Strategy 1)")
    
    # Strategy 2: Direct BFS search
    logger.info("\n" + "=" * 70)
    logger.info("STARTING STRATEGY 2")
    logger.info("=" * 70)
    snake2, metadata2 = strategy_direct_bfs_search(
        dimension,
        logger,
        memory_limit_gb
    )
    if snake2 and snake2.get_length() > best_length:
        best_snake = snake2
        best_length = snake2.get_length()
        best_metadata = metadata2
        best_strategy = "direct_bfs_search"
        save_progress(dimension, best_snake, best_metadata, best_strategy)
        logger.info(f"New best: {best_length} (Strategy 2)")
    
    # Strategy 3: Multiple seeds
    logger.info("\n" + "=" * 70)
    logger.info("STARTING STRATEGY 3")
    logger.info("=" * 70)
    snake3, metadata3 = strategy_multiple_seeds(
        dimension,
        logger,
        memory_limit_gb
    )
    if snake3 and snake3.get_length() > best_length:
        best_snake = snake3
        best_length = snake3.get_length()
        best_metadata = metadata3
        best_strategy = "multiple_seeds"
        save_progress(dimension, best_snake, best_metadata, best_strategy)
        logger.info(f"New best: {best_length} (Strategy 3)")
    
    # Final summary
    logger.info("\n" + "=" * 70)
    logger.info("SEARCH COMPLETE")
    logger.info("=" * 70)
    
    if best_snake:
        known_record = get_known_record(dimension)
        logger.info(f"Best snake found: length {best_length}")
        logger.info(f"Known record: {known_record}")
        logger.info(f"Strategy: {best_strategy}")
        
        if known_record:
            if best_length > known_record:
                logger.critical(
                    f"*** NEW RECORD: {best_length} (previous: {known_record}, "
                    f"+{best_length - known_record}) ***"
                )
            elif best_length == known_record:
                logger.info("Matched known record")
            else:
                logger.info(
                    f"Below known record (difference: {known_record - best_length})"
                )
        else:
            logger.info("No known record for comparison")
    else:
        logger.error("No valid snake found")
    
    return {
        'dimension': dimension,
        'best_snake': best_snake,
        'best_length': best_length,
        'best_metadata': best_metadata,
        'best_strategy': best_strategy,
        'known_record': get_known_record(dimension),
        'is_new_record': (
            get_known_record(dimension) is not None and
            best_length > get_known_record(dimension)
        )
    }


def generate_summary_report(results: Dict[int, Dict]) -> None:
    """Generate summary report of all searches.
    
    Parameters
    ----------
    results : Dict[int, Dict]
        Results dictionary keyed by dimension
    """
    os.makedirs(CRACK_RESULTS_DIR, exist_ok=True)
    
    report_lines = [
        "# Comprehensive Search Results for Dimensions 11-14",
        "",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
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
        
        report_lines.append(f"### Dimension {dim}")
        report_lines.append("")
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
    
    report_file = f"{CRACK_RESULTS_DIR}/summary_report.md"
    with open(report_file, 'w') as f:
        f.write(report_content)
    
    print(f"\nSummary report saved to: {report_file}")


def main():
    """Main function to orchestrate searches for all target dimensions."""
    print("=" * 70)
    print("COMPREHENSIVE SEARCH FOR DIMENSIONS 11-14")
    print("=" * 70)
    print(f"Target dimensions: {TARGET_DIMENSIONS}")
    print(f"Memory limit: {MEMORY_LIMIT_GB} GB")
    print(f"Max levels: {MAX_LEVELS}")
    print(f"Output directory: {OUTPUT_BASE}/")
    print("")
    
    # Create output directories
    os.makedirs(CRACK_RESULTS_DIR, exist_ok=True)
    os.makedirs(CRACK_LOGS_DIR, exist_ok=True)
    
    results = {}
    
    for dimension in TARGET_DIMENSIONS:
        print(f"\n{'=' * 70}")
        print(f"Processing dimension {dimension}")
        print(f"{'=' * 70}\n")
        
        try:
            result = search_dimension(dimension, MEMORY_LIMIT_GB)
            results[dimension] = result
            
            # Brief summary
            best_length = result.get('best_length', 0)
            known_record = result.get('known_record')
            is_new_record = result.get('is_new_record', False)
            
            print(f"\nDimension {dimension} complete:")
            print(f"  Best length: {best_length}")
            print(f"  Known record: {known_record}")
            if is_new_record:
                print(f"  *** NEW RECORD FOUND ***")
            
        except KeyboardInterrupt:
            print(f"\n\nInterrupted by user. Saving progress...")
            break
        except Exception as e:
            print(f"\n\nError processing dimension {dimension}: {e}")
            traceback.print_exc()
            continue
    
    # Generate summary report
    if results:
        print("\n" + "=" * 70)
        print("Generating summary report...")
        print("=" * 70)
        generate_summary_report(results)
    
    print("\n" + "=" * 70)
    print("ALL SEARCHES COMPLETE")
    print("=" * 70)
    print(f"\nResults saved to: {CRACK_RESULTS_DIR}/")
    print(f"Logs saved to: {CRACK_LOGS_DIR}/")


if __name__ == "__main__":
    main()

