from pathlib import Path
import re

ROOT = Path("news/posts")

CANONICAL = {
    "elemental imaging": "Elemental imaging",
    "libs": "Elemental imaging",
    "multi-elemental imaging": "Elemental imaging",
    "metals & health": "Elemental imaging",
    "cancer": "Cancer & nanomedicine",
    "oncology": "Cancer & nanomedicine",
    "nanoparticles": "Cancer & nanomedicine",
    "nanoscience": "Cancer & nanomedicine",
    "nanomedicine": "Cancer & nanomedicine",
    "clinical": "Clinical research",
    "clinical research": "Clinical research",
    "clinical study": "Clinical research",
    "trial": "Clinical research",
    "biolibs": "BioLIBS",
    "platform": "BioLIBS",
    "article": "Publications",
    "review": "Publications",
    "publication": "Publications",
    "paper": "Publications",
    "book": "Publications",
    "book chapter": "Publications",
    "chapter": "Publications",
    "conference": "Events",
    "congress": "Events",
    "scientific events": "Events",
    "event": "Events",
    "seminar": "Events",
    "talk": "Events",
    "lecture": "Events",
    "award": "Career & awards",
    "awards": "Career & awards",
    "iuf": "Career & awards",
    "academic": "Career & awards",
    "career": "Career & awards",
    "phd": "Career & awards",
    "outreach": "Outreach",
    "media": "Outreach",
    "public engagement": "Outreach",
}

PRIORITY = [
    "BioLIBS",
    "Career & awards",
    "Clinical research",
    "Cancer & nanomedicine",
    "Elemental imaging",
    "Publications",
    "Events",
    "Outreach",
]


def parse_categories(raw: str):
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1]
    parts = [p.strip().strip('"\'') for p in raw.split(",") if p.strip()]
    return parts


def canonicalize(categories, text):
    out = []
    haystack = text.lower()
    for cat in categories:
        mapped = CANONICAL.get(cat.lower())
        if mapped and mapped not in out:
            out.append(mapped)

    # Add one useful thematic category when legacy metadata was too generic.
    if "libs" in haystack or "elemental" in haystack:
        if "Elemental imaging" not in out:
            out.append("Elemental imaging")
    if any(k in haystack for k in ["cancer", "nanoparticle", "nanocluster", "nanomedicine"]):
        if "Cancer & nanomedicine" not in out:
            out.append("Cancer & nanomedicine")
    if "biolibs" in haystack and "BioLIBS" not in out:
        out.append("BioLIBS")
    if any(k in haystack for k in ["conference", "congress", "seminar", "talk @", "lecture @", "meeting"]):
        if "Events" not in out:
            out.append("Events")
    if any(k in haystack for k in ["published", "review", "article", "chapter", "doi"]):
        if "Publications" not in out:
            out.append("Publications")

    # Keep at most two categories, ordered consistently.
    out = sorted(set(out), key=lambda x: PRIORITY.index(x) if x in PRIORITY else 999)
    return out[:2] or ["Outreach"]


def normalize_file(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.search(r"(?m)^categories:\s*(.+)$", text)
    if not m:
        return False
    categories = parse_categories(m.group(1))
    new_categories = canonicalize(categories, text)
    replacement = "categories: [" + ", ".join(new_categories) + "]"
    new_text = text[:m.start()] + replacement + text[m.end():]
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"Normalized {path}: {new_categories}")
        return True
    return False


if __name__ == "__main__":
    changed = 0
    for path in sorted(ROOT.glob("*/index.qmd")):
        changed += normalize_file(path)
    print(f"Normalized {changed} News file(s).")
