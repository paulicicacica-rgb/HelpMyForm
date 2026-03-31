import os
import subprocess
from pathlib import Path

PUBLIC_DIR = "public"

# العلاقات بين الصفحات (عدلها حسب موقعك)
RELATED_LINKS = {
    "hap.html": ["pps.html", "medical-card.html", "irp.html"],
    "pps.html": ["hap.html", "medical-card.html", "irp.html"],
    "medical-card.html": ["hap.html", "pps.html", "irp.html"],
    "irp.html": ["hap.html", "pps.html", "medical-card.html"],
    "jobseeker.html": ["hap.html", "pps.html", "medical-card.html"],
}

def generate_related_links(current_page, related_pages):
    html = '\n<div class="related-guides">\n'
    html += '<h3>Related Guides</h3>\n<ul>\n'

    for page in related_pages:
        name = page.replace(".html", "").replace("-", " ").title()
        html += f'<li><a href="/{page}">{name}</a></li>\n'

    html += '</ul>\n</div>\n'
    return html


def inject_related_links(file_path):
    file_name = Path(file_path).name

    if file_name not in RELATED_LINKS:
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    related_html = generate_related_links(file_name, RELATED_LINKS[file_name])

    if related_html in content:
        return  # already injected

    if "</body>" in content:
        content = content.replace("</body>", related_html + "\n</body>")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated: {file_path}")


def process_files():
    for root, dirs, files in os.walk(PUBLIC_DIR):
        for file in files:
            if file.endswith(".html"):
                inject_related_links(os.path.join(root, file))


def git_push():
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Auto update related guides"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Changes pushed to GitHub")
    except subprocess.CalledProcessError as e:
        print("❌ Git error:", e)


if __name__ == "__main__":
    process_files()
    git_push()
