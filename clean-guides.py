import glob
import re

updated = 0

for pattern in ['*.html', '*/*.html']:
    for filepath in glob.glob(pattern, recursive=True):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = re.sub(
            r'\n?<div class="related-guides">[\s\S]*?</div>\s*\n?(?=</body>)',
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
And .github/workflows/clean-guides.yml:
name: Clean Related Guides

on:
  workflow_dispatch:

jobs:
  clean:
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
        run: python clean-guides.py

      - name: Commit and push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git diff --staged --quiet || git commit -m "Remove related guides from all pages"
          git push
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Deploy to Vercel
        run: curl -X POST "https://api.vercel.com/v1/integrations/deploy/prj_kkhosX2cx6IA8XzwOVEQrAbYGsUh/cBtdlk4XmO"
