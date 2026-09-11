# Updating the website

This file is a private maintenance note for the GitHub repository. It is **not rendered as a public website page**.

The site is built with Quarto. In normal use, you only need to edit `.qmd` files or upload images. GitHub Actions rebuilds and publishes the site automatically after each commit.

## 1. Add an image

Upload image files to the `images/` folder:

1. Open the repository on GitHub.
2. Open `images/`.
3. Click **Add file → Upload files**.
4. Drag the image into the browser.
5. Click **Commit changes**.

Recommended file names:

- lowercase only
- no spaces
- no accents
- short and descriptive

Examples:

`biolibs-inauguration-2025.jpg`

`metals-health-team.jpg`

`libs-microscope.jpg`

To display an image from a root-level `.qmd` page:

```markdown
![BioLIBS platform](images/libs-microscope.jpg)
```

To control its width:

```markdown
![BioLIBS platform](images/libs-microscope.jpg){width=70%}
```

## 2. Add a News item

Create a new folder inside `news/posts/`, for example:

`news/posts/new-paper-libs-2026/`

Then create an `index.qmd` file inside it:

```yaml
---
title: "New LIBS publication"
date: 2026-09-15
description: "A short one-line description shown on the News page."
categories: [Publication, LIBS]
---

A short text explaining the news.

[Read the paper](https://doi.org/...)
```

Quarto automatically sorts News by date.

## 3. Add an image to a News item

The easiest approach is to put the image in the same News folder as the `index.qmd` file.

Example:

`news/posts/new-paper-libs-2026/image.jpg`

Then add this to the YAML header:

```yaml
image: image.jpg
```

This allows Quarto to use the image as the News thumbnail.

## 4. Edit normal text

Open the relevant `.qmd` file, click the pencil icon, edit the text and click **Commit changes**.

Main files:

- `index.qmd` — homepage
- `about.qmd` — biography
- `research.qmd` — research overview
- `biolibs.qmd` — BioLIBS
- `clinical-research.qmd` — clinical and translational projects
- `publications.qmd` — publication page shell (publication entries are automatic)
- `contact.qmd` — contact page
- `news/index.qmd` — News listing configuration

## 5. Add a link

Markdown link:

```markdown
[Université Grenoble Alpes](https://www.univ-grenoble-alpes.fr/)
```

Button:

```markdown
[Learn more](https://example.org){.btn .btn-primary}
```

## 6. Publications

Do **not** manually edit `generated/publications.md` or `data/openalex_publications.json`.

They are generated automatically from OpenAlex using ORCID every week by GitHub Actions.

Google Scholar remains available as an external profile link.

## 7. Dark mode and visual design

The light/dark theme configuration is in `_quarto.yml`.

The custom visual appearance is in `styles.css`.

Routine content updates should normally **not** require editing `styles.css`.

## 8. If something goes wrong

Do not panic: every GitHub commit is reversible.

The simplest workflow is to send ChatGPT the change you want in plain language, for example:

> Add this image to the BioLIBS page after the technology paragraph.

or

> Create a News item announcing this paper using this DOI.

The repository can then be updated directly without local software or terminal commands.
