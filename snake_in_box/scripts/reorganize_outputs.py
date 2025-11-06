#!/usr/bin/env python3
"""Reorganize all outputs into unified output/ directory structure.

Moves all generated files into organized subdirectories:
- output/reports/
- output/visualizations/
- output/graphical_abstracts/
- output/test_outputs/
- output/data/
"""

import os
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


def reorganize_outputs():
    """Reorganize all outputs into output/ directory."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    output_dir = os.path.join(base_dir, 'output')
    
    # Create directory structure
    dirs = [
        'reports',
        'visualizations',
        'graphical_abstracts',
        'test_outputs',
        'data',
    ]
    
    for d in dirs:
        os.makedirs(os.path.join(output_dir, d), exist_ok=True)
    
    # Move reports
    reports = [
        'analysis_report.md',
        'analysis_report.html',
        'validation_report.md',
        'performance_report.md',
    ]
    
    for report in reports:
        src = os.path.join(base_dir, report)
        if os.path.exists(src):
            dst = os.path.join(output_dir, 'reports', report)
            shutil.move(src, dst)
            print(f"Moved: {report} -> output/reports/")
    
    # Move visualizations
    viz_dir = os.path.join(base_dir, 'visualizations')
    if os.path.exists(viz_dir):
        for f in os.listdir(viz_dir):
            src = os.path.join(viz_dir, f)
            if os.path.isfile(src):
                dst = os.path.join(output_dir, 'visualizations', f)
                shutil.move(src, dst)
                print(f"Moved: {f} -> output/visualizations/")
        try:
            os.rmdir(viz_dir)
        except:
            pass
    
    # Move graphical abstracts
    for f in os.listdir(base_dir):
        if f.startswith('graphical_abstract') and f.endswith('.png'):
            src = os.path.join(base_dir, f)
            dst = os.path.join(output_dir, 'graphical_abstracts', f)
            shutil.move(src, dst)
            print(f"Moved: {f} -> output/graphical_abstracts/")
    
    # Move test outputs if they exist
    test_output_dir = os.path.join(base_dir, 'test_outputs')
    if os.path.exists(test_output_dir):
        for f in os.listdir(test_output_dir):
            src = os.path.join(test_output_dir, f)
            if os.path.isfile(src):
                dst = os.path.join(output_dir, 'test_outputs', f)
                shutil.move(src, dst)
                print(f"Moved: {f} -> output/test_outputs/")
    
    print(f"\nAll outputs reorganized into: {output_dir}/")


if __name__ == "__main__":
    reorganize_outputs()

