#!/usr/bin/env python3
from pathlib import Path
import shutil

# CONFIG: choose 'ignore' or 'replace'
DECODE_ERRORS = "ignore"  # or "replace"

def process_txt_files(folder: Path, make_backup: bool = True):
    for path in folder.glob("*.txt"):
        try:
            # Read while ignoring/replacing undecodable bytes
            text = path.read_text(encoding="utf-8", errors=DECODE_ERRORS)
        except Exception as e:
            print(f"Skipping {path.name}: failed to read ({e})")
            continue

        # Split keeping line endings so we preserve original newlines
        lines = text.splitlines(keepends=True)

        # Keep only lines that start with "capital"
        kept = [ln for ln in lines if ln.startswith("capital")]

        # Create a backup before overwriting
        if make_backup:
            backup_path = path.with_suffix(path.suffix + ".bak")
            try:
                shutil.copy2(path, backup_path)
            except Exception as e:
                print(f"Warning: could not create backup for {path.name}: {e}")

        try:
            # Write back the kept lines (will be encoded as utf-8)
            path.write_text("".join(kept), encoding="utf-8", errors=DECODE_ERRORS)
            print(f"Processed: {path.name}  (kept {len(kept)} lines)")
        except Exception as e:
            print(f"Failed to write {path.name}: {e}")

if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    process_txt_files(folder)
