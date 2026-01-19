import os
import shutil
from pathlib import Path
from collections import defaultdict

SOURCE = Path(r"c:\Users\indef\Documents\NY\project\snakemake2\results\multimer")
TARGET = Path(r"c:\Users\indef\Documents\NY\project\snakemake2\results\multimer_flattened")

TARGET.mkdir(parents=True, exist_ok=True)

file_map = defaultdict(list)
all_files = list(SOURCE.rglob('*.json'))
print(f'Found {len(all_files)} json files under {SOURCE}')

for f in all_files:
    file_map[f.name].append(f)

moved = 0
skipped = 0

for name, paths in file_map.items():
    if len(paths) == 1:
        src = paths[0]
        dst = TARGET / name
        try:
            shutil.copy2(src, dst)
            moved += 1
        except Exception as e:
            print(f'Error copying {src}: {e}')
            skipped += 1
    else:
        # disambiguate by parent dirs
        for p in paths:
            rel = p.relative_to(SOURCE)
            parent = '_'.join(rel.parts[:-1])
            new_name = f"{Path(name).stem}_{parent}{Path(name).suffix}"
            dst = TARGET / new_name
            try:
                shutil.copy2(p, dst)
                moved += 1
            except Exception as e:
                print(f'Error copying {p}: {e}')
                skipped += 1

print('\nDone')
print(f'Files moved: {moved}, skipped: {skipped}')
print(f'Target dir: {TARGET}')
