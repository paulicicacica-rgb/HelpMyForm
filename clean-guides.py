import glob 
import re

updated = 0

# Include all HTML files in all subdirectories
for filepath in glob.glob('**/*.html', recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = re.sub(
        r'\s*<div class="related-guides">[\s\S]*?</ul>\s*</div>',
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
