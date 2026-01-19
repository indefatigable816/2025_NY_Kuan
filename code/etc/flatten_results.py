import os
import shutil
from pathlib import Path
from collections import defaultdict

def flatten_directory(source_dir, target_dir=None):
    """
    Flatten a nested directory structure by moving all files to a single flat directory.
    If filename conflicts exist, appends parent directory names to make them unique.
    
    Args:
        source_dir: Source directory to flatten
        target_dir: Target directory (defaults to source_dir + '_flattened')
    """
    
    source_path = Path(source_dir)
    
    if target_dir is None:
        target_path = source_path.parent / f"{source_path.name}_flattened"
    else:
        target_path = Path(target_dir)
    
    # Create target directory
    target_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Flattening: {source_path}")
    print(f"Target: {target_path}")
    print()
    
    # Collect all files with their paths
    file_map = defaultdict(list)
    all_files = list(source_path.rglob('*'))
    total_files = sum(1 for f in all_files if f.is_file())
    
    print(f"Total files found: {total_files}")
    print()
    
    for file_path in all_files:
        if file_path.is_file():
            file_map[file_path.name].append(file_path)
    
    # Move files
    moved = 0
    skipped = 0
    
    for filename, file_paths in sorted(file_map.items()):
        if len(file_paths) == 1:
            # No conflict, just move
            src = file_paths[0]
            dst = target_path / filename
            
            try:
                shutil.copy2(src, dst)
                moved += 1
                print(f"✓ {filename}")
            except Exception as e:
                print(f"✗ {filename}: {str(e)}")
                skipped += 1
        else:
            # Conflict: add parent directory info to make unique
            for src in file_paths:
                # Get relative path from source
                rel_path = src.relative_to(source_path)
                parent_dirs = '_'.join(rel_path.parts[:-1])
                
                # Create new filename
                stem = src.stem
                suffix = src.suffix
                new_name = f"{stem}_{parent_dirs}{suffix}"
                dst = target_path / new_name
                
                try:
                    shutil.copy2(src, dst)
                    moved += 1
                    print(f"✓ {new_name}")
                except Exception as e:
                    print(f"✗ {new_name}: {str(e)}")
                    skipped += 1
    
    print()
    print("=" * 80)
    print(f"Flattening Complete!")
    print(f"  Files moved: {moved}")
    print(f"  Files skipped: {skipped}")
    print(f"  Target directory: {target_path}")
    print("=" * 80)
    
    return target_path


if __name__ == "__main__":
    results_dir = r"c:\Users\indef\Documents\NY\project\snakemake2\results"
    flatten_directory(results_dir)
