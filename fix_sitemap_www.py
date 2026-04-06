#!/usr/bin/env python3
"""
fix_sitemap_www.py
Replaces all non-www URLs in sitemap.xml with www versions.
"""

import os

SITEMAP = "sitemap.xml"
OLD = "https://helpmyform.com/"
NEW = "https://www.helpmyform.com/"

if not os.path.exists(SITEMAP):
    print("sitemap.xml not found in current directory.")
    exit(1)

with open(SITEMAP, "r", encoding="utf-8") as f:
    original = f.read()

updated = original.replace(OLD, NEW)
count = original.count(OLD)

if updated != original:
    with open(SITEMAP, "w", encoding="utf-8") as f:
        f.write(updated)
    print(f"Done. Fixed {count} URL(s) in sitemap.xml.")
else:
    print("No changes needed — sitemap already uses www.")
