"""Output directory reorganization.

Moves generated analysis artifacts from the repository root into the unified
``output/`` directory layout. Moved verbatim from
``snake_in_box/scripts/reorganize_outputs.py`` (thin-orchestrator contract,
2026-09 scripts audit); the script now only computes the repo root and
delegates here.
"""

import os
import shutil


def reorganize_outputs(base_dir: str) -> None:
    """Reorganize all outputs into ``<base_dir>/output/``.

    Parameters
    ----------
    base_dir : str
        Repository root containing stray generated files and the ``output/``
        target directory.
    """
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
