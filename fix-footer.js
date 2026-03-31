const fs = require('fs');
const path = require('path');
const { glob } = require('glob');

const newFooter = `<footer>
<div class="footer-brand">Help<span>My</span>Form</div>
<p class="footer-note">Free help filling in Irish forms · 27 languages · No account needed</p>
<div class="footer-links">
<a href="https://www.helpmyform.com">Home</a>
<a href="https://www.helpmyform.com/pps">PPS Number</a>
<a href="https://www.helpmyform.com/hap">HAP Form</a>
<a href="https://www.helpmyform.com/medical-card">Medical Card</a>
<a href="https://www.helpmyform.com/irp">IRP</a>
<a href="https://www.helpmyform.com/jobseeker">Jobseeker</a>
</div>
<div class="footer-links" style="margin-top:8px;font-size:12px">
<a href="https://www.helpmyform.com/ro">Română</a>
<a href="https://www.helpmyform.com/pt">Português</a>
<a href="https://www.helpmyform.com/uk">Українська</a>
<a href="https://www.helpmyform.com/pl">Polski</a>
<a href="https://www.helpmyform.com/so">Somali</a>
</div>
</footer>`;

async function run() {
  const files = await glob('**/*.html', { ignore: 'node_modules/**' });
  
  let updated = 0;
  
  for (const file of files) {
    let content = fs.readFileSync(file, 'utf8');
    
    const footerRegex = /<footer>[\s\S]*?<\/footer>/;
    
    if (footerRegex.test(content)) {
      content = content.replace(footerRegex, newFooter);
      fs.writeFileSync(file, content, 'utf8');
      console.log(`✅ Updated: ${file}`);
      updated++;
    } else {
      console.log(`⚠️ No footer found: ${file}`);
    }
  }
  
  console.log(`\nDone. ${updated} files updated.`);
}

run();
