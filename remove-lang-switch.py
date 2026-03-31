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
