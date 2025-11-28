#!/usr/bin/env python3
from pathlib import Path
import sys

def process_file(path: Path) -> int:
    """
    Read file, keep only lines that are inside braces (including lines that contain { or }).
    Returns number of lines written (kept).
    """
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"Failed to read {path}: {e}", file=sys.stderr)
        return 0

    lines = text.splitlines(keepends=True)
    new_lines = []
    brace_level = 0

    for line in lines:
        # Determine whether this line contains any brace characters
        has_brace = ("{" in line) or ("}" in line)

        # Keep the line if we are already inside a block, or if it contains a brace
        if brace_level > 0 or has_brace:
            new_lines.append(line)

        # Update brace_level left-to-right so nesting works correctly on the same line
        for ch in line:
            if ch == "{":
                brace_level += 1
            elif ch == "}":
                brace_level -= 1
                # prevent negative nesting depth from persisting
                if brace_level < 0:
                    brace_level = 0

    # Write results back (overwrite) using same tolerant encoding
    try:
        path.write_text("".join(new_lines), encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"Failed to write {path}: {e}", file=sys.stderr)
        return 0

    return len(new_lines)


def main():
    # directory where this script file lives (works when __file__ exists)
    try:
        script_dir = Path(__file__).resolve().parent
    except NameError:
        # fallback for interactive environments where __file__ isn't defined
        script_dir = Path.cwd()

    txt_files = list(script_dir.glob("*.txt"))
    if not txt_files:
        print(f"No .txt files found in {script_dir}")
        return

    for p in txt_files:
        kept = process_file(p)
        print(f"Processed {p.name}: kept {kept} lines")


if __name__ == "__main__":
    main()
