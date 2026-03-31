def get_webpage_schema(title, url, description, lang="en"):
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "url": url,
        "description": description,
        "inLanguage": lang,
        "isPartOf": {
            "@type": "WebSite",
            "name": "HelpMyForm",
            "url": "https://helpmyform.com"
        }
    }


def get_software_app_schema():
    return {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "HelpMyForm",
        "applicationCategory": "WebApplication",
        "operatingSystem": "All",
        "url": "https://helpmyform.com",
        "description": "Upload a photo of any form and get AI guidance to fill it step-by-step."
    }
