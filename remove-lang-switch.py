import glob
import re

HTML_BLOCK = '''  <div class="lang-switch">
    <p>Citești în română. Vrei în engleză?</p>
    <a href="https://helpmyform.com">Switch to English →</a>
  </div>'''

updated = 0

for filepath in glob.glob('public/**/*.html', recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove any lang-switch div regardless of content
    new_content = re.sub(
        r'\s*<div class="lang-switch">[\s\S]*?</div>\s*</div>',
        '',
        content
    )

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'✅ Cleaned: {filepath}')
        updated += 1
    else:
        print(f'⏭ Skipped: {filepath}')

print(f'\nDone. {updated} files cleaned.')
And .github/workflows/remove-lang-switch.yml:
name: Remove Lang Switch

on:
  workflow_dispatch:

jobs:
  remove:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Run script
        run: python remove-lang-switch.py

      - name: Commit and push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git diff --staged --quiet || git commit -m "Remove lang switch from language pages"
          git push
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Deploy to Vercel
        run: curl -X POST "https://api.vercel.com/v1/integrations/deploy/prj_kkhosX2cx6IA8XzwOVEQrAbYGsUh/xxdtD48jhk"
