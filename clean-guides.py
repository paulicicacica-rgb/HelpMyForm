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
