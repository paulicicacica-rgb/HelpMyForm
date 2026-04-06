import os
import re

# Run this from the root of your repo
# It will fix all scan-box-btn links in /public to point to /app

PUBLIC_DIR = "public"
OLD = 'class="scan-box-btn" href="https://helpmyform.com"'
NEW = 'class="scan-box-btn" href="https://helpmyform.com/app"'

fixed = 0
for root, dirs, files in os.walk(PUBLIC_DIR):
    for fname in files:
        if not fname.endswith(".html"):
            continue
        path = os.path.join(root, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if OLD in content:
            new_content = content.replace(OLD, NEW)
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            count = content.count(OLD)
            print(f"✓ {path} — {count} CTA(s) fixed")
            fixed += count

if fixed == 0:
    print("No matches found. Check that your HTML uses exactly:")
    print(f'  {OLD}')
else:
    print(f"\nDone. {fixed} CTA(s) updated to /app")
