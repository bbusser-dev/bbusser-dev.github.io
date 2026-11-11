from pathlib import Path
import html
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "projects.yaml"
OUT = ROOT / "generated"

with DATA.open(encoding="utf-8") as fh:
    projects = yaml.safe_load(fh)["projects"]

projects = sorted(projects, key=lambda x: x.get("order", 999))

def card(p):
    acronym = html.escape(str(p["acronym"]))
    title = html.escape(str(p["title"]))
    period = html.escape(str(p.get("period", "")))
    role = html.escape(str(p.get("role", "")))
    kind = html.escape(str(p.get("kind", "")))
    theme = html.escape(str(p.get("theme", "")))
    description = html.escape(str(p.get("description", "")))
    href = p.get("internal_url") or p.get("external_url") or ""
    link = ""
    if href:
        label = "Explore project" if p.get("internal_url") else "External record"
        link = f'<a class="project-link" href="{html.escape(href, quote=True)}">{label} →</a>'
    return f"""<article class="project-card">
  <div class="project-visual" aria-hidden="true">
    <span></span><span></span><span></span><span></span><span></span><span></span>
  </div>
  <div class="project-card-body">
    <div class="project-meta">{kind} · {period}</div>
    <h3>{acronym}</h3>
    <div class="project-title">{title}</div>
    <p>{description}</p>
    <div class="project-footer"><span>{role}</span><span>{theme}</span></div>
    {link}
  </div>
</article>"""

def grid(items):
    return '<div class="project-grid">\n' + "\n".join(card(p) for p in items) + "\n</div>\n"

OUT.mkdir(exist_ok=True)
(OUT / "projects-home.md").write_text(grid([p for p in projects if p.get("featured_home")]), encoding="utf-8")
(OUT / "projects-clinical.md").write_text(grid([p for p in projects if p.get("clinical")]), encoding="utf-8")
(OUT / "projects-all.md").write_text(grid(projects), encoding="utf-8")

print(f"Rendered {len(projects)} structured project entries.")
