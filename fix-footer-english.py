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
</div>'''
]

new_footer = '''<div class="footer-links">
<a href="https://www.helpmyform.com">Home</a>
<a href="https://www.helpmyform.com/pps">PPS Number</a>
<a href="https://www.helpmyform.com/hap">HAP Form</a>
<a href="https://www.helpmyform.com/medical-card">Medical Card</a>
<a href="https://www.helpmyform.com/irp">IRP</a>
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
                break

        if matched:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'✅ Updated: {filepath}')
            updated += 1
        else:
            print(f'⚠️ No match: {filepath}')
    except FileNotFoundError:
        print(f'❌ Not found: {filepath}')

print(f'\nDone. {updated} files updated.')
