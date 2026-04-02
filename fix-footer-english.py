import re

old_footers = [
    '''<div class="footer-links">
<a href="https://helpmyform.com">Home</a>
<a href="https://helpmyform.com/pps">PPS Number</a>
<a href="https://helpmyform.com/hap">HAP Form</a>
<a href="https://helpmyform.com/medical-card">Medical Card</a>
</div>''',
    '''<div class="footer-links">
<a href="https://helpmyform.com">Home</a>
<a href="https://helpmyform.com/pps">PPS Number</a>
<a href="https://helpmyform.com/hap">HAP Form</a>
<a href="https://helpmyform.com/medical-card">Medical Card</a>
<a href="https://helpmyform.com/irp">IRP Renewal</a>
</div>''',
    '''<div class="footer-links">
<a href="https://helpmyform.com">Home</a>
<a href="https://helpmyform.com/pps">PPS Number</a>
<a href="https://helpmyform.com/hap">HAP Form</a>
<a href="https://helpmyform.com/medical-card">Medical Card</a>
<a href="https://helpmyform.com/irp">IRP Renewal</a>
<a href="https://helpmyform.com/jobseeker">Jobseeker</a>
</div>'''
]

new_footer = '''<div class="footer-links">
<a href="https://www.helpmyform.com">Home</a>
<a href="https://www.helpmyform.com/pps">PPS Number</a>
<a href="https://www.helpmyform.com/hap">HAP Form</a>
<a href="https://www.helpmyform.com/medical-card">Medical Card</a>
<a href="https://www.helpmyform.com/jobseeker">Jobseeker</a>
</div>'''

files = ['public/hap.html', 'public/pps.html', 'public/medical-card.html', 'public/irp.html', 'public/jobseeker.html']

updated = 0

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        matched = False
        for old in old_footers:
            if old in content:
                content = content.replace(old, new_footer)
                matched = True

        # Fix duplicate footer
        content = re.sub(r'(</footer>)\s*<footer>[\s\S]*?</footer>', r'\1', content)

        if matched:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'✅ Updated: {filepath}')
            updated += 1
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'⚠️ Footer already updated, fixed duplicates: {filepath}')
    except FileNotFoundError:
        print(f'❌ Not found: {filepath}')

print(f'\nDone. {updated} files updated.')
