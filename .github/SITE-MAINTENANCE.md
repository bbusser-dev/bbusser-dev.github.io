# Mémo — mettre à jour le site web professionnel

Ce fichier est un **mode d'emploi privé** du dépôt GitHub. Il n'est pas publié sur le site.

## Le principe à retenir

Le site est construit avec **Quarto + GitHub Pages**.

Dans la plupart des cas :

1. modifier un fichier ou déposer une image dans GitHub ;
2. cliquer sur **Commit changes** ;
3. GitHub Actions reconstruit automatiquement le site ;
4. vérifier le résultat sur **https://bbusser-dev.github.io**.

---

# 1. Voir le site comme un visiteur

Ouvrir :

**https://bbusser-dev.github.io**

C'est la version réellement publiée.

Après une modification, attendre que le workflow GitHub soit terminé :

1. ouvrir le dépôt GitHub ;
2. cliquer sur l'onglet **Actions** ;
3. ouvrir le workflow **Publish Quarto website** le plus récent ;
4. attendre le statut vert **Success** ;
5. recharger **https://bbusser-dev.github.io** avec Ctrl+F5 si nécessaire.

Si le workflow est rouge, ne pas multiplier les corrections au hasard : regarder l'étape en erreur ou demander à ChatGPT de la diagnostiquer.

---

# 2. Ajouter une image

Toutes les images générales du site doivent être déposées dans :

`images/`

Dans GitHub :

1. ouvrir le dossier **images** ;
2. cliquer sur **Add file → Upload files** ;
3. glisser-déposer l'image ;
4. choisir un nom simple ;
5. cliquer sur **Commit changes**.

Nommage conseillé :

- minuscules ;
- pas d'espace ;
- pas d'accent ;
- nom descriptif.

Exemples :

`biolibs-microscope.jpg`

`libs-lung-si-al-fe.jpg`

`metals-health-team-2026.jpg`

## Afficher l'image dans une page

Dans une page située à la racine du site :

```markdown
![BioLIBS platform](images/biolibs-microscope.jpg)
```

Avec largeur contrôlée :

```markdown
![BioLIBS platform](images/biolibs-microscope.jpg){width=75%}
```

Pour une image de News, le plus simple est de la mettre directement dans le dossier du billet, puis d'ajouter dans son en-tête :

```yaml
image: image.jpg
```

---

# 3. Ajouter ou modifier un projet / essai clinique

Les projets ne doivent plus être recopiés dans plusieurs pages.

La source unique est :

`data/projects.yaml`

Chaque projet ressemble à ceci :

```yaml
- acronym: "PNEUMO-LIBS"
  title: "Multi-elemental imaging in pulmonary disease"
  period: "2026–"
  role: "Coordinator · Principal Investigator"
  kind: "Clinical research"
  theme: "Elemental imaging"
  clinical: true
  featured_home: true
  order: 10
  description: "Description courte du projet."
```

Après modification et commit, GitHub reconstruit automatiquement :

- les cartes de la page **Projects** ;
- les projets de **Clinical Research** ;
- les projets sélectionnés de la page **Research** ;
- les projets mis en avant sur la **Home**.

Ne pas modifier manuellement :

`generated/projects-all.md`

`generated/projects-home.md`

`generated/projects-clinical.md`

Ils sont régénérés automatiquement.

---

# 4. Modifier le texte d'une page

Principaux fichiers :

- `index.qmd` — page d'accueil ;
- `about.qmd` — biographie ;
- `research.qmd` — recherche ;
- `projects.qmd` — page des projets ;
- `biolibs.qmd` — BioLIBS ;
- `clinical-research.qmd` — recherche clinique ;
- `publications.qmd` — cadre de la page Publications ;
- `contact.qmd` — contact ;
- `news/index.qmd` — configuration de la page News.

Dans GitHub :

1. ouvrir le fichier ;
2. cliquer sur l'icône **crayon** ;
3. modifier le texte ;
4. **Commit changes** ;
5. vérifier le workflow **Actions** ;
6. regarder le résultat sur le site.

---

# 5. Ajouter une News

Créer un dossier sous :

`news/posts/`

Exemple :

`news/posts/2026-nouvelle-publication-libs/`

Puis créer dedans un fichier :

`index.qmd`

Exemple :

```yaml
---
title: "New LIBS publication"
date: 2026-11-11
description: "Short description shown on the News page."
categories: [Publications, Elemental imaging]
image: image.jpg
---

Texte du billet.

[Read the paper](https://doi.org/...)
```

Catégories recommandées : rester dans le petit vocabulaire existant et éviter de créer des synonymes.

---

# 6. Publications

Ne pas modifier manuellement :

`generated/publications.md`

`data/openalex_publications.json`

La liste est mise à jour automatiquement depuis **OpenAlex / ORCID**.

Pour contrôler le résultat final, regarder :

**https://bbusser-dev.github.io/publications.html**

Google Scholar reste disponible comme profil externe complémentaire.

---

# 7. Graphisme et mode sombre

Les réglages visuels sont principalement dans :

`styles.css`

Le bouton soleil/lune est géré par :

`theme-toggle.html`

`theme-toggle.css`

La configuration générale Quarto est dans :

`_quarto.yml`

Pour les modifications ordinaires de contenu, ne pas toucher à ces fichiers.

---

# 8. Vérification rapide après toute modification

Checklist :

- [ ] le fichier a bien été enregistré par un **Commit changes** ;
- [ ] l'onglet **Actions** montre un workflow récent ;
- [ ] **Publish Quarto website** est vert ;
- [ ] ouvrir **https://bbusser-dev.github.io** ;
- [ ] vérifier ordinateur + fenêtre étroite/mobile ;
- [ ] tester le bouton soleil/lune ;
- [ ] cliquer sur les nouveaux liens ;
- [ ] vérifier que les images ne sont ni cassées ni trop grandes.

---

# 9. Si je ne veux pas manipuler GitHub moi-même

Donner simplement à ChatGPT l'instruction en langage naturel, par exemple :

> Ajoute cette image à la page BioLIBS après le paragraphe sur l'instrument.

> Ajoute ce nouvel essai clinique dans Projects et Clinical Research.

> Crée une News à partir de ce DOI et de cette image.

> Corrige ce texte dans About.

ChatGPT peut modifier directement ce dépôt GitHub.

---

# 10. Règle simple

**Contenu unique, réutilisable, puis génération automatique.**

Quand une information existe dans un fichier structuré comme `data/projects.yaml`, ne pas la recopier ailleurs à la main.
