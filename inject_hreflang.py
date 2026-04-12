from bs4 import BeautifulSoup
import os

BASE = "https://www.helpmyform.com"
ROOT = "public"

GROUPS = {
    "index": {
        "en": "index.html",
    },
    "hap": {
        "en": "hap/index.html",
        "ro": "ro/hap.html",
        "pl": "pl/hap.html",
        "pt": "pt/hap.html",
        "uk": "uk/hap.html",
        "so": "so/hap.html",
        "ar": "ar/hap.html",
        "it": "it/hap.html",
        "de": "de/hap.html",
        "lt": "lt/hap.html",
    },
    "pps": {
        "en": "pps/index.html",
        "ro": "ro/pps.html",
        "pl": "pl/pps.html",
        "pt": "pt/pps.html",
        "uk": "uk/pps.html",
        "so": "so/pps.html",
        "ar": "ar/pps.html",
        "it": "it/pps.html",
        "de": "de/pps.html",
        "lt": "lt/pps.html",
    },
    "medical-card": {
        "en": "medical-card/index.html",
        "ro": "ro/medical-card.html",
        "pl": "pl/medical-card.html",
        "pt": "pt/medical-card.html",
        "uk": "uk/medical-card.html",
        "so": "so/medical-card.html",
        "ar": "ar/medical-card.html",
        "it": "it/medical-card.html",
        "de": "de/medical-card.html",
        "lt": "lt/medical-card.html",
    },
    "jobseeker": {
        "en": "jobseeker/index.html",
        "ro": "ro/jobseeker.html",
        "pl": "pl/jobseeker.html",
        "pt": "pt/jobseeker.html",
        "uk": "uk/jobseeker.html",
        "so": "so/jobseeker.html",
        "ar": "ar/jobseeker.html",
        "it": "it/jobseeker.html",
        "de": "de/jobseeker.html",
        "lt": "lt/jobseeker.html",
    },
    "driving-licence": {
        "en": "driving-licence/index.html",
        "ro": "ro/driving-licence.html",
        "pl": "pl/driving-licence.html",
        "pt": "pt/driving-licence.html",
        "uk": "uk/driving-licence.html",
        "so": "so/driving-licence.html",
        "ar": "ar/driving-licence.html",
        "it": "it/driving-licence.html",
        "de": "de/driving-licence.html",
        "lt": "lt/driving-licence.html",
    },
    "rent-supplement": {
        "en": "rent-supplement/index.html",
        "ro": "ro/rent-supplement.html",
        "pl": "pl/rent-supplement.html",
        "pt": "pt/rent-supplement.html",
        "uk": "uk/rent-supplement.html",
        "so": "so/rent-supplement.html",
        "ar": "ar/rent-supplement.html",
        "it": "it/rent-supplement.html",
        "de": "de/rent-supplement.html",
        "lt": "lt/rent-supplement.html",
    },
    # IRP — non-EU only (no pl, pt, it, de, lt)
    "irp": {
        "en": "irp/index.html",
        "ro": "ro/irp.html",
        "uk": "uk/irp.html",
        "so": "so/irp.html",
        "ar": "ar/irp.html",
    },
    # Bank account — all 10 languages
    "bank-account": {
        "en": "bank-account/index.html",
        "ro": "ro/bank-account.html",
        "uk": "uk/bank-account.html",
        "pl": "pl/bank-account.html",
        "pt": "pt/bank-account.html",
        "lt": "lt/bank-account.html",
        "it": "it/bank-account.html",
        "de": "de/bank-account.html",
        "es": "es/bank-account.html",
        "so": "so/bank-account.html",
        "ar": "ar/bank-account.html",
    },
    # Language homepages
    "lang-ro": {"en": "index.html", "ro": "ro/index.html"},
    "lang-pl": {"en": "index.html", "pl": "pl/index.html"},
    "lang-pt": {"en": "index.html", "pt": "pt/index.html"},
    "lang-uk": {"en": "index.html", "uk": "uk/index.html"},
    "lang-so": {"en": "index.html", "so": "so/index.html"},
    "lang-ar": {"en": "index.html", "ar": "ar/index.html"},
    "lang-it": {"en": "index.html", "it": "it/index.html"},
    "lang-de": {"en": "index.html", "de": "de/index.html"},
    "lang-lt": {"en": "index.html", "lt": "lt/index.html"},
    "lang-es": {"en": "index.html", "es": "es/index.html"},
    # English-only pages
    "temporary-protection": {"en": "temporary-protection/index.html"},
    "child-benefit":        {"uk": "uk/child-benefit.html"},
    "education":            {"uk": "uk/education.html"},
}

def to_url(path):
    clean = path.replace("\\", "/")
    if clean == "index.html":
        return BASE + "/"
    clean = clean.replace(".html", "")
    # folder/index → /folder  (e.g. hap/index → /hap, ro/index → /ro)
    if clean.endswith("/index"):
        clean = clean[:-6]
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

    # Remove existing alternate and canonical tags
    for tag in soup.find_all("link"):
        if not tag.attrs:
            continue
        rel = tag.get("rel", [])
        if "alternate" in rel or "canonical" in rel:
            tag.decompose()

    # Inject hreflang alternates
    for lang, path in group_langs.items():
        tag = soup.new_tag("link", rel="alternate", hreflang=lang, href=to_url(path))
        head.append("\n  ")
        head.append(tag)

    # x-default → English, fallback to first entry
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
