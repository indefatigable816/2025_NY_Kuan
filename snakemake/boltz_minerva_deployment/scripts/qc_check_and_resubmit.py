#!/usr/bin/env python3
"""
qc_check_and_resubmit.py

Scan Boltz prediction output `confidence_*.json` files and report how many
predictions meet the QC criteria (ptm > 0.5 and iptm > 0.3 by default).

If fewer than the requested number of passing predictions are found, the
script writes a small `resubmit_instructions.txt` file with suggested
resubmission commands the user can run on Minerva.

Usage (on Minerva):
  python3 scripts/qc_check_and_resubmit.py \
      --results-dir /sc/arion/work/cheny69/1216/results \
      --job-name WT_trastuzumab \
      --min-pass 10

This is intentionally conservative: it reports results and suggests actions
for the user to review rather than automatically resubmitting jobs.
"""
import argparse
import json
from pathlib import Path
import sys


def find_confidence_files(results_dir: Path, job_name: str | None):
    files = list(results_dir.rglob('confidence_*.json'))
    if job_name:
        files = [p for p in files if job_name in p.parts or job_name in p.as_posix()]
    return sorted(files)


def read_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception as e:
        print(f"Warning: failed to read {path}: {e}")
        return {}


def extract_scores(data: dict):
    # Robustly pick up ptm/iptm keys used in existing outputs
    ptm_keys = ('ptm', 'pTM', 'ptm_score')
    iptm_keys = ('iptm', 'iPTM', 'iptm_score')
    ptm = None
    iptm = None
    for k in ptm_keys:
        if k in data:
            ptm = data[k]
            break
    for k in iptm_keys:
        if k in data:
            iptm = data[k]
            break
    # Fallbacks for differently-named keys
    if ptm is None:
        ptm = data.get('complex_ptm') or data.get('complex_ptm_score')
    if iptm is None:
        iptm = data.get('complex_iptm') or data.get('complex_iplddt')
    return ptm, iptm


def main():
    p = argparse.ArgumentParser(description='QC check for Boltz predictions')
    p.add_argument('--results-dir', required=True, type=Path, help='Root results directory')
    p.add_argument('--job-name', required=False, help='Optional job name to filter (e.g. WT_trastuzumab)')
    p.add_argument('--min-pass', type=int, default=10, help='Minimum number of passing predictions to accept')
    p.add_argument('--ptm-thresh', type=float, default=0.5, help='pTM threshold (default 0.5)')
    p.add_argument('--iptm-thresh', type=float, default=0.3, help='iPTM threshold (default 0.3)')
    p.add_argument('--out', type=Path, default=Path('qc_report.txt'), help='Output report path')
    args = p.parse_args()

    results_dir: Path = args.results_dir
    if not results_dir.exists():
        print(f"Error: results-dir {results_dir} does not exist", file=sys.stderr)
        sys.exit(2)

    files = find_confidence_files(results_dir, args.job_name)
    if not files:
        print("No confidence_*.json files found (check --results-dir and --job-name)")
        sys.exit(2)

    passing = []
    failing = []
    for f in files:
        data = read_json(f)
        ptm, iptm = extract_scores(data)
        ok = False
        try:
            if ptm is not None and iptm is not None:
                ok = (float(ptm) > args.ptm_thresh) and (float(iptm) > args.iptm_thresh)
        except Exception:
            ok = False
        rec = (f, ptm, iptm)
        if ok:
            passing.append(rec)
        else:
            failing.append(rec)

    report_lines = []
    report_lines.append(f"QC summary for: {results_dir} (job filter: {args.job_name})")
    report_lines.append(f"Found {len(files)} confidence files; passing: {len(passing)}; failing: {len(failing)}")
    report_lines.append(f"Criteria: ptm > {args.ptm_thresh}, iptm > {args.iptm_thresh}; required passing: {args.min_pass}\n")

    if passing:
        report_lines.append("Passing predictions (sample):")
        for path, ptm, iptm in passing[:50]:
            report_lines.append(f"  {path}  ptm={ptm}  iptm={iptm}")
    if failing:
        report_lines.append("\nFailing predictions (sample):")
        for path, ptm, iptm in failing[:50]:
            report_lines.append(f"  {path}  ptm={ptm}  iptm={iptm}")

    args.out.write_text('\n'.join(report_lines))
    print(f"Wrote report to {args.out}")

    if len(passing) >= args.min_pass:
        print(f"QC OK: {len(passing)} >= {args.min_pass}")
        sys.exit(0)

    # Not enough passing predictions: write resubmission suggestions
    resub = Path('resubmit_instructions.txt')
    suggestions = []
    suggestions.append("# QC resubmission suggestions")
    suggestions.append(f"# Found {len(passing)} passing predictions; need {args.min_pass - len(passing)} more.")
    suggestions.append("")
    suggestions.append("# Suggested actions (review before running):")
    suggestions.append("# 1) Re-run the same .lsf file for this job to generate additional seeds: e.g.")
    suggestions.append("#    cd /sc/arion/work/cheny69/1216")
    suggestions.append("#    bsub < <JOB>.lsf")
    suggestions.append("")
    suggestions.append("# 2) Create a modified .lsf with a larger array or extra seeds and submit it.")
    suggestions.append("# 3) If issues persist, consider adjusting MSA settings or increasing recycling.")
    suggestions.append("")
    suggestions.append("# Example: to re-run WT_trastuzumab (10 more seeds):")
    suggestions.append("#    cp WT_trastuzumab.lsf WT_trastuzumab_resubmit.lsf")
    suggestions.append("#    # Edit the new .lsf to set a different job name and submit: bsub < WT_trastuzumab_resubmit.lsf")

    resub.write_text('\n'.join(suggestions))
    print(f"Wrote resubmission suggestions to {resub}")
    sys.exit(1)


if __name__ == '__main__':
    main()
