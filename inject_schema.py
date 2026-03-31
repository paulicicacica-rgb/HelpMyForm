import os
import json
from bs4 import BeautifulSoup
from schemas import get_webpage_schema, get_software_app_schema

BASE_URL = "https://helpmyform.com"

PAGES = {
    "index.html": {
        "type": "app"
    },
    "hap.html": {
        "title": "How to Fill in the HAP Form in Ireland",
        "url": f"{BASE_URL}/hap",
        "description": "Step-by-step guide to the HAP form in Ireland.",
        "lang": "en"
    },
    "pps.html": {
        "title": "How to Apply for a PPS Number in Ireland",
        "url": f"{BASE_URL}/pps",
        "description": "Guide to applying for a PPS number in Ireland.",
        "lang": "en"
    }
    # add more pages here
}

def inject_schema(file_path, schema_obj):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    script_tag = soup.new_tag("script", type="application/ld+json")
    script_tag.string = json.dumps(schema_obj, indent=2)

    soup.head.append(script_tag)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))


def main():
    for file_name, config in PAGES.items():
        if not os.path.exists(file_name):
            continue

        if config.get("type") == "app":
            schema = get_software_app_schema()
        else:
            schema = get_webpage_schema(
                config["title"],
                config["url"],
                config["description"],
                config["lang"]
            )

        inject_schema(file_name, schema)


if __name__ == "__main__":
    main()
