import os
import re

ROOT = "public"

# The full style block extracted from a known-good file (ro/pps.html)
# This is the shared stylesheet used across all language subpages
FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,300;1,9..144,400&family=Instrument+Sans:wght@400;500;600&display=swap" onload="this.onload=null;this.rel='stylesheet'"><noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,300;1,9..144,400&family=Instrument+Sans:wght@400;500;600&display=swap"></noscript>'''

STYLE = '''<style>
:root{--bg:#f5f0eb;--surface:#fff;--border:#e0d8cf;--ink:#1a1612;--ink2:#6b5f54;--ink3:#a89d94;--accent:#2d6a4f;--accent-light:#e8f4ef;--accent-mid:#52b788;--gold:#b5832a;--gold-light:#fdf6e7;--warm:#c9562a;--warm-light:#fdf0eb;--radius:18px;--shadow:0 2px 12px rgba(26,22,18,0.08);--shadow-lg:0 8px 32px rgba(26,22,18,0.12)}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}body{background:var(--bg);color:var(--ink);font-family:'Instrument Sans',sans-serif;font-size:16px;line-height:1.6}
.top-bar{height:4px;background:linear-gradient(90deg,var(--accent) 0%,var(--accent-mid) 50%,var(--gold) 100%)}
nav{background:var(--surface);border-bottom:1px solid var(--border);padding:16px 24px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100}
.nav-brand{font-family:'Fraunces',serif;font-size:22px;font-weight:500;color:var(--ink);text-decoration:none}.nav-brand span{color:var(--accent)}
.nav-cta{background:var(--accent);color:white;border-radius:100px;padding:10px 20px;font-size:14px;font-weight:600;text-decoration:none;display:inline-block}
.hero{padding:52px 24px 40px;max-width:760px;margin:0 auto}
.breadcrumb{font-size:12px;color:var(--ink3);margin-bottom:20px}.breadcrumb a{color:var(--accent);text-decoration:none}
.hero-badge{display:inline-flex;align-items:center;gap:6px;background:var(--accent-light);border:1px solid rgba(45,106,79,0.2);border-radius:100px;padding:5px 14px;font-size:12px;font-weight:600;color:var(--accent);text-transform:uppercase;margin-bottom:20px}
h1{font-family:'Fraunces',serif;font-size:clamp(28px,6vw,44px);font-weight:500;color:var(--ink);line-height:1.2;letter-spacing:-0.5px;margin-bottom:16px}h1 em{font-style:italic;color:var(--accent)}
.hero-sub{font-size:17px;color:var(--ink2);line-height:1.7;margin-bottom:12px;max-width:600px}
.hero-meta{font-size:13px;color:var(--ink3);font-weight:500;margin-top:16px}
.content{max-width:760px;margin:0 auto;padding:0 24px 80px}
.toc{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px 24px;margin-bottom:40px}
.toc-title{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;color:var(--ink3);margin-bottom:12px}
.toc-list{list-style:none;display:flex;flex-direction:column;gap:6px}
.toc-list a{font-size:14px;color:var(--accent);text-decoration:none;font-weight:500}
.section{margin-bottom:48px}
h2{font-family:'Fraunces',serif;font-size:26px;font-weight:500;color:var(--ink);margin-bottom:16px;border-top:2px solid var(--accent-light);padding-top:20px;margin-top:8px}
h3{font-family:'Fraunces',serif;font-size:20px;font-weight:500;color:var(--ink);margin-bottom:12px;margin-top:24px}
p{color:var(--ink2);margin-bottom:16px;font-size:15px;line-height:1.8}
ul.body-list{color:var(--ink2);font-size:15px;margin:12px 0 16px 20px;line-height:1.9}
.info-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px 22px;margin:20px 0}
.info-card h4{font-size:15px;font-weight:700;color:var(--ink);margin-bottom:10px}
.info-card p{font-size:14px;margin-bottom:8px;line-height:1.7}
.info-card ul{margin:6px 0 0 16px;color:var(--ink2);font-size:14px;line-height:1.8}
.compare-table{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;margin:20px 0}
.compare-header{display:grid;grid-template-columns:1.4fr 1fr 1fr;background:var(--accent);padding:12px 18px}
.compare-header div{font-size:12px;font-weight:700;color:white;text-transform:uppercase;letter-spacing:0.4px}
.compare-row{display:grid;grid-template-columns:1.4fr 1fr 1fr;padding:12px 18px;border-bottom:1px solid var(--border)}.compare-row:last-child{border-bottom:none}.compare-row:nth-child(even){background:rgba(45,106,79,0.025)}
.compare-cell{font-size:14px;color:var(--ink2);line-height:1.5}.compare-cell.label{font-weight:600;color:var(--ink)}.compare-cell.yes{color:var(--accent);font-weight:600}.compare-cell.no{color:var(--warm)}
.note-box{background:var(--gold-light);border:1px solid rgba(181,131,42,0.25);border-radius:var(--radius);padding:16px 20px;margin:20px 0;font-size:14px;color:var(--gold);line-height:1.7}.note-box strong{display:block;margin-bottom:4px;font-size:15px}
.warn-box{background:var(--warm-light);border:1px solid rgba(201,86,42,0.25);border-radius:var(--radius);padding:16px 20px;margin:20px 0;font-size:14px;color:var(--warm);line-height:1.7}.warn-box strong{display:block;margin-bottom:4px;font-size:15px}
.steps{list-style:none;display:flex;flex-direction:column;gap:16px;margin:20px 0}
.step-item{display:flex;gap:16px;align-items:flex-start}
.step-num{width:32px;height:32px;background:var(--accent);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:white;flex-shrink:0;margin-top:2px}
.step-content h3{margin-top:0;font-size:17px}.step-content p{margin-bottom:0}
.related{display:flex;flex-direction:column;gap:10px;margin-top:16px}
.related-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;text-decoration:none;display:flex;align-items:center;justify-content:space-between}
.related-card-left h3{font-size:15px;font-weight:600;color:var(--ink);margin-bottom:3px;font-family:'Instrument Sans',sans-serif}
.related-card-left p{font-size:13px;color:var(--ink2);margin:0}
.related-card-arrow{color:var(--accent);font-size:18px;flex-shrink:0}
.bottom-cta{background:var(--accent);border-radius:var(--radius);padding:32px 24px;text-align:center;margin-top:40px;color:white}
.bottom-cta h3{font-family:'Fraunces',serif;font-size:22px;font-weight:500;margin-bottom:8px}
.bottom-cta p{font-size:14px;color:rgba(255,255,255,0.85);margin-bottom:20px;line-height:1.6}
.bottom-cta-btn{display:inline-block;background:white;color:var(--accent);border-radius:100px;padding:14px 32px;font-size:15px;font-weight:700;text-decoration:none;width:100%;text-align:center}
.bottom-cta-note{margin-top:10px;font-size:12px;opacity:0.6}
footer{background:var(--surface);border-top:1px solid var(--border);padding:32px 24px;text-align:center}
.footer-brand{font-family:'Fraunces',serif;font-size:18px;font-weight:500;color:var(--ink);margin-bottom:6px}.footer-brand span{color:var(--accent)}
.footer-links{display:flex;justify-content:center;gap:20px;margin-top:12px;flex-wrap:wrap}.footer-links a{font-size:13px;color:var(--ink3);text-decoration:none}
.footer-note{font-size:12px;color:var(--ink3);margin-top:8px}
</style>'''

INJECTION = FONTS + "\n" + STYLE + "\n"

fixed = 0
skipped = 0

for dirpath, dirnames, filenames in os.walk(ROOT):
    # Skip the main English hub pages — they have their own heavier stylesheet
    # Only process language subfolders: ro/, pl/, uk/, pt/, so/, ar/, it/, de/, lt/, es/
    parts = dirpath.replace("\\", "/").split("/")
    if len(parts) < 2:
        skipped_file = True
    
    for filename in filenames:
        if not filename.endswith(".html"):
            continue

        filepath = os.path.join(dirpath, filename)
        rel = filepath.replace("\\", "/")

        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()

        # Only fix files that are missing a <style> block
        if "<style>" in html:
            continue

        # Only fix files that have a <head> 
        if "</head>" not in html:
            print(f"  SKIP (no </head>): {rel}")
            continue

        # Inject fonts + style before </head>
        html = html.replace("</head>", INJECTION + "</head>", 1)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"  ✓ fixed: {rel}")
        fixed += 1

print(f"\n=== Done: {fixed} files fixed ===")
