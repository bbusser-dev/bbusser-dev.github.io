#!/usr/bin/env python3
"""Generate the publication list for the website from OpenAlex.

The script uses Benoit Busser's ORCID as the stable author identifier. It
keeps a machine-readable snapshot of all OpenAlex records, while the public
page displays conventional academic publications rather than supplementary
files, datasets, peer-review records and similar objects.
"""

from __future__ import annotations

import html
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ORCID = os.environ.get("OPENALEX_ORCID", "0000-0002-9425-1577")
API_KEY = os.environ.get("OPENALEX_API_KEY", "").strip()
BASE_URL = "https://api.openalex.org/works"
OUT_MD = Path("generated/publications.md")
OUT_JSON = Path("data/openalex_publications.json")

DISPLAY_TYPES = {"article", "review", "book-chapter", "editorial", "letter"}

SELECT = ",".join(
    [
        "id",
        "doi",
        "title",
        "display_name",
        "publication_year",
        "publication_date",
        "type",
        "cited_by_count",
        "authorships",
        "primary_location",
        "biblio",
        "open_access",
        "ids",
        "is_retracted",
    ]
)


def api_get(params: dict[str, str], attempts: int = 4) -> dict:
    query = dict(params)
    if API_KEY:
        query["api_key"] = API_KEY
    url = BASE_URL + "?" + urllib.parse.urlencode(query)
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "bbusser-academic-site/1.0 (GitHub Actions)",
        },
    )

    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            print(f"OpenAlex HTTP {exc.code}: {body}")
            if exc.code not in (429, 500, 502, 503, 504) or attempt == attempts - 1:
                raise
        except urllib.error.URLError as exc:
            print(f"OpenAlex network error: {exc}")
            if attempt == attempts - 1:
                raise
        time.sleep(2**attempt)
    raise RuntimeError("OpenAlex request failed")


def fetch_works() -> list[dict]:
    works: list[dict] = []
    cursor = "*"
    while cursor:
        payload = api_get(
            {
                "filter": f"authorships.author.orcid:{ORCID},type:!paratext",
                "select": SELECT,
                "per_page": "100",
                "cursor": cursor,
                "sort": "publication_date:desc",
            }
        )
        works.extend(payload.get("results", []))
        cursor = payload.get("meta", {}).get("next_cursor")

    unique: dict[str, dict] = {}
    for work in works:
        work_id = work.get("id")
        if work_id:
            unique[work_id] = work

    return sorted(
        unique.values(),
        key=lambda w: (w.get("publication_date") or "0000-00-00", w.get("title") or ""),
        reverse=True,
    )


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def display_type(value: str | None) -> str:
    if not value:
        return "Publication"
    return value.replace("-", " ").title()


def source_name(work: dict) -> str:
    location = work.get("primary_location") or {}
    source = location.get("source") or {}
    return source.get("display_name") or ""


def is_display_publication(work: dict) -> bool:
    """Keep conventional academic publications for the public page."""
    if work.get("type") not in DISPLAY_TYPES:
        return False

    doi = (work.get("doi") or "").lower()
    source = source_name(work).lower()
    title = (work.get("title") or work.get("display_name") or "").lower()

    # ACS and some publishers assign DOIs to supporting-information files that
    # OpenAlex may classify as articles. These should not appear as papers.
    if re.search(r"\.s\d+$", doi):
        return False
    if source in {"figshare", "the cambridge structural database"}:
        return False
    if title.startswith("author response for "):
        return False
    return True


def author_html(work: dict) -> str:
    authors = []
    for authorship in work.get("authorships") or []:
        author = authorship.get("author") or {}
        name = author.get("display_name") or ""
        author_orcid = (author.get("orcid") or "").replace("https://orcid.org/", "")
        if not name:
            continue
        rendered = esc(name)
        if author_orcid == ORCID or name.lower().replace("î", "i") == "benoit busser":
            rendered = f"<strong>{rendered}</strong>"
        authors.append(rendered)

    if len(authors) > 12:
        authors = authors[:11] + ["et al."]
    return ", ".join(authors)


def publication_link(work: dict) -> tuple[str, str]:
    doi = work.get("doi") or ""
    if doi:
        return doi, "DOI"
    pmid = (work.get("ids") or {}).get("pmid") or ""
    if pmid:
        return pmid, "PubMed"
    return work.get("id") or "https://openalex.org", "OpenAlex"


def make_json(works: list[dict]) -> str:
    compact = []
    for work in works:
        compact.append(
            {
                "id": work.get("id"),
                "doi": work.get("doi"),
                "title": work.get("title") or work.get("display_name"),
                "publication_year": work.get("publication_year"),
                "publication_date": work.get("publication_date"),
                "type": work.get("type"),
                "cited_by_count": work.get("cited_by_count", 0),
                "source": source_name(work),
                "authors": [
                    (a.get("author") or {}).get("display_name")
                    for a in (work.get("authorships") or [])
                    if (a.get("author") or {}).get("display_name")
                ],
                "is_open_access": (work.get("open_access") or {}).get("is_oa"),
                "is_retracted": work.get("is_retracted", False),
                "display_on_site": is_display_publication(work),
            }
        )
    return json.dumps(compact, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def make_markdown(works: list[dict], raw_count: int) -> str:
    lines = [
        "<!-- AUTO-GENERATED by scripts/update_publications.py. Do not edit manually. -->",
        "",
        f'<div class="publication-count"><strong>{len(works)} academic publications</strong> displayed from {raw_count} OpenAlex records linked to ORCID {esc(ORCID)}.</div>',
        "",
    ]

    current_year = None
    for work in works:
        year = work.get("publication_year") or "Undated"
        if year != current_year:
            current_year = year
            lines.extend([f"## {year}", ""])

        title = work.get("title") or work.get("display_name") or "Untitled work"
        href, link_label = publication_link(work)
        journal = source_name(work)
        pub_type = display_type(work.get("type"))
        citations = int(work.get("cited_by_count") or 0)
        authors = author_html(work)
        oa = (work.get("open_access") or {}).get("is_oa")
        retracted = bool(work.get("is_retracted"))

        meta = []
        if journal:
            meta.append(f"<em>{esc(journal)}</em>")
        meta.append(esc(pub_type))
        meta.append(f"{citations} citation" + ("" if citations == 1 else "s"))
        if oa:
            meta.append("Open access")
        if retracted:
            meta.append("<strong>Retracted</strong>")

        lines.extend(
            [
                '<div class="publication-item">',
                f'<div class="publication-title"><a href="{esc(href)}">{esc(title)}</a></div>',
                f'<div class="publication-authors">{authors}</div>' if authors else "",
                f'<div class="publication-meta">{" · ".join(meta)} · <a href="{esc(href)}">{link_label}</a></div>',
                "</div>",
                "",
            ]
        )

    return "\n".join(line for line in lines if line is not None).rstrip() + "\n"


def write_if_changed(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    previous = path.read_text(encoding="utf-8") if path.exists() else None
    if previous != content:
        path.write_text(content, encoding="utf-8")
        print(f"updated {path}")
    else:
        print(f"unchanged {path}")


def main() -> None:
    works = fetch_works()
    if not works:
        raise RuntimeError(f"OpenAlex returned no works for ORCID {ORCID}; refusing to overwrite publication data")
    display_works = [work for work in works if is_display_publication(work)]
    if not display_works:
        raise RuntimeError("OpenAlex returned records but none passed the publication display filter")

    write_if_changed(OUT_JSON, make_json(works))
    write_if_changed(OUT_MD, make_markdown(display_works, len(works)))
    print(f"OpenAlex sync complete: {len(works)} records; {len(display_works)} displayed publications")


if __name__ == "__main__":
    main()
