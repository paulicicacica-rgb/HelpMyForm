#!/usr/bin/env python3
"""
fix_canonical_www.py
Replaces all instances of https://helpmyform.com/ with https://www.helpmyform.com/
in every .html file in the repo, fixing canonical/og:url mismatches.
"""

import os
import sys

OLD = "https://helpmyform.com"
NEW = "https://www.helpmyform.com"

def fix_file(path):
    with open(path, "r", encoding="utf-8") as f:
        original = f.read()

    updated = original.replace(OLD, NEW)

    if updated != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
        count = original.count(OLD)
        print(f"  Fixed {count} occurrence(s): {path}")
        return True
    return False

def main():
    root = os.getcwd()
    fixed_files = 0
    total_files = 0

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden folders and node_modules
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "node_modules"]

        for filename in filenames:
            if filename.endswith(".html"):
                total_files += 1
                filepath = os.path.join(dirpath, filename)
                if fix_file(filepath):
                    fixed_files += 1

    print(f"\nDone. Fixed {fixed_files} file(s) out of {total_files} HTML file(s) scanned.")
    if fixed_files == 0:
        print("No changes needed — all files already use www.")

if __name__ == "__main__":
    main()
