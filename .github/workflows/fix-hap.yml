import re

files = ['hap.html', 'pps.html', 'medical-card.html', 'irp.html', 'jobseeker.html']

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()

        # Fix 1: Remove official link from CSS block if it's there
        content = content.replace(
            '\n  <a class="scan-box-official" href="https://www.hap.ie/apply/" target="_blank" rel="noopener">⬇ Apply for HAP Online →</a>\n  .scan-box-langs',
            '\n  .scan-box-langs'
        )

        # Fix 2: Remove broken related guides
        content = re.sub(
            r'<div class="related-guides">[\s\S]*?</div>\s*(?=</body>)',
            '',
            content
        )

        # Fix 3: Fix footer
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

        content = content.replace(old_footer, new_footer)

        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'✅ Fixed: {f}')
    except FileNotFoundError:
        print(f'⚠ Not found: {f}')

print('Done.')
