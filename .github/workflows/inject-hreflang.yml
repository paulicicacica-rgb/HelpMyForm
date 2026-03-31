from bs4 import BeautifulSoup
import os

BASE = "https://www.helpmyform.com"
ROOT = "public"  # all HTML files live inside /public

# ─── PAGE GROUPS ───────────────────────────────────────────────
GROUPS = {
    "index": {
        "en": "index.html",
    },
    "hap": {
        "en": "hap.html",
        "pt": "pt/hap.html",
        "ro": "ro/hap.html",
        "pl": "pl/hap.html",
        "uk": "uk/hap.html",
        "so": "so/hap.html",
    },
    "pps": {
        "en": "pps.html",
        "pt": "pt/pps.html",
        "ro": "ro/pps.html",
        "pl": "pl/pps.html",
        "uk": "uk/pps.html",
        "so": "so/pps.html",
    },
    "medical-card": {
        "en": "medical-card.html",
        "pt": "pt/medical-card.html",
        "ro": "ro/medical-card.html",
        "pl": "pl/medical-card.html",
        "uk": "uk/medical-card.html",
    },
    "irp": {
        "en": "irp.html",
        "pt": "pt/irp.html",
        "so": "so/irp.html",
    },
    "jobseeker": {
        "en": "jobseeker.html",
        "pt": "pt/jobseeker.html",
        "ro": "ro/jobseeker.html",
        "pl": "pl/jobseeker.html",
        "uk": "uk/jobseeker.html",
        "so": "so/jobseeker.html",
    },
    "temporary-protection": {
        "en": "temporary-protection.html",
    },
    "child-benefit": {
        "uk": "uk/child-benefit.html",
    },
    "education": {
        "uk": "uk/education.html",
    },
}

def to_url(path):
    clean = path.replace("\\", "/")
    if clean == "index.html":
        return BASE + "/"
    clean = clean.replace(".html", "")
    return BASE + "/" + clean

def inject(rel_path, group_langs, self_path):
    filepath = os.path.join(ROOT, rel_path)
    if not os.path.exists(filepath):
        print(f"  SKIP (missing): {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    head = soup.find("head")
    if not head:
        print(f"  SKIP (no <head>): {filepath}")
        return

    for tag in soup.find_all("link"):
        rel = tag.get("rel", [])
        if "alternate" in rel or "canonical" in rel:
            tag.decompose()

    for lang, path in group_langs.items():
        tag = soup.new_tag("link", rel="alternate", hreflang=lang, href=to_url(path))
        head.append("\n  ")
        head.append(tag)

    default_path = group_langs.get("en", list(group_langs.values())[0])
    head.append("\n  ")
    head.append(soup.new_tag("link", rel="alternate", hreflang="x-default", href=to_url(default_path)))
    head.append("\n  ")
    head.append(soup.new_tag("link", rel="canonical", href=to_url(self_path)))
    head.append("\n")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"  ✓  {filepath}")

print("=== Injecting hreflang + canonical tags ===\n")
for slug, langs in GROUPS.items():
    print(f"Group: {slug}")
    for lang, path in langs.items():
        inject(path, langs, path)
    print()
print("=== Done ===")
