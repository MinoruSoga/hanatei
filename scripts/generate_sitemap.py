"""Regenerate the static sitemap: python3 scripts/generate_sitemap.py."""
import datetime
from pathlib import Path
from html.parser import HTMLParser
from xml.etree.ElementTree import Element, SubElement, ElementTree, register_namespace
ROOT = Path(__file__).resolve().parent.parent
class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(); self.canonical = None; self.noindex = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and a.get("rel") == "canonical": self.canonical = a.get("href")
        if tag == "meta" and a.get("name") == "robots" and "noindex" in a.get("content", ""): self.noindex = True
ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
register_namespace("", ns)
urls = Element(f"{{{ns}}}urlset")
for page in sorted(ROOT.glob("*.html")):
    meta = Metadata(); meta.feed(page.read_text())
    if meta.noindex: continue
    if not meta.canonical or not meta.canonical.startswith("https://hanatei.jp/"): raise ValueError(f"Invalid canonical: {page.name}")
    url = SubElement(urls, f"{{{ns}}}url")
    SubElement(url, f"{{{ns}}}loc").text = meta.canonical
    SubElement(url, f"{{{ns}}}lastmod").text = datetime.date.fromtimestamp(page.stat().st_mtime).isoformat()
ElementTree(urls).write(ROOT / "sitemap.xml", encoding="utf-8", xml_declaration=True)
