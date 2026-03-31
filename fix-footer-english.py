import glob

old_footer = '''<div class="footer-links">
<a href="https://helpmyform.com">Home</a>
<a href="https://helpmyform.com/pps">PPS Number</a>
<a href="https://helpmyform.com/hap">HAP Form</a>
<a href="https://helpmyform.com/medical-card">Medical Card</a>
</div>'''

new_footer = '''<div class="footer-links">
<a href="https://www.helpmyform.com">Home</a>
<a href="https://www.helpmyform.com/pps">PPS Number</a>
<a href="https://www.helpmyform.com/hap">HAP Form</a>
<a href="https://www.helpmyform.com/medical-card">Medical Card</a>
<a href="https://www.helpmyform.com/irp">IRP</a>
<a href="https://www.helpmyform.com/jobseeker">Jobseeker</a>
</div>'''

updated = 0

for filepath in ['hap.html', 'pps.html', 'medical-card.html', 'irp.html', 'jobseeker.html']:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if old_footer in content:
            content = content.replace(old_footer, new_footer)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'✅ Updated: {filepath}')
            updated += 1
        else:
            print(f'⚠️ No match: {filepath}')
    except FileNotFoundError:
        print(f'❌ Not found: {filepath}')

print(f'\nDone. {updated} files updated.')
