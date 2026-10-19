"""Reproduce every table and figure of the paper from the released processed features.

    python reproduce.py

Expects the Zenodo files in data/ (see data/README.md). Runs the analysis, the baselines,
the gyroscope ablation, the cross-session study, the tables, the figures and the energy
estimate, then checks the headline numbers against analysis/expected_results.json.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STEPS = [['analysis/results/make_results.py'], ['analysis/results/make_baselines.py'], ['analysis/results/make_gyro.py'],
         ['analysis/session2.py'], ['analysis/tables/make_tables.py'], ['analysis/figures/make_figures.py'],
         ['hardware/esp32_benchmark/energy_estimate.py']]


def main():
    if not (ROOT / 'data' / 'session1_episodes.csv').is_file() and not (ROOT / 'dataset').is_dir():
        sys.exit('Put the Zenodo files in data/ first (see data/README.md).')
    for step in STEPS:
        print(f'>>> {" ".join(step)}', flush=True)
        subprocess.run([sys.executable, '-W', 'ignore', *step], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

    out = ROOT / 'analysis' / 'results' / 'out'
    res = json.loads((out / 'results.json').read_text())
    s2 = json.loads((out / 'session2' / 'results_session2.json').read_text())
    static = lambda block, name: next(r for r in block['static'] if r['method'].startswith(name))
    got = {
        'P0 online FRR (%)': res['P0']['pooled']['frr'], 'P0 online FAR (%)': res['P0']['pooled']['far'],
        'P1 online FRR (%)': res['P1']['pooled']['frr'], 'P1 online FAR (%)': res['P1']['pooled']['far'],
        'P0 static EER (%)': static(res['P0'], 'Full')['eer'], 'P1 static EER (%)': static(res['P1'], 'Full')['eer'],
        'P1 FNMR@FMR1% (%)': static(res['P1'], 'Full')['fnmr_at_fmr1'],
        'Session 2 static EER (%)': s2['P1']['static_s2']['table']['Full decision score m']['eer'],
        'Session 2 online FRR, FIFO carried (%)': s2['P1']['online_s2_carried']['frr'],
    }
    expected = json.loads((ROOT / 'analysis' / 'expected_results.json').read_text())
    ok = True
    print(f'\n{"metric":<42}{"paper":>10}{"reproduced":>13}')
    for k, v in expected.items():
        same = abs(got[k] - v) < 1e-6
        ok &= same
        print(f'{k:<42}{v:>10.3f}{got[k]:>13.3f}  {"OK" if same else "MISMATCH"}')
    print('\nAll headline numbers reproduced.' if ok else '\nSome numbers differ; see above.')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
