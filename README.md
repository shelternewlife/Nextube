# Nextube — Neon Liquid Sort Puzzle

A multilingual static website for **Nextube**, the Android liquid-sorting puzzle game by DevImpact.

- Google Play: https://play.google.com/store/apps/details?id=com.game.Nextube.devimpact
- Android package: `com.game.Nextube.devimpact`
- Website: https://shelternewlife.github.io/Nextube/

## What the game offers

Nextube is a neon-style liquid sorting puzzle. Players tap a tube and then a destination tube to pour liquid when the top colours match and the destination has room. The objective is to finish with one colour in each tube. The Google Play description also identifies Undo and Reset controls, progressive levels, stars and coins, cosmetic tube skins and backgrounds, offline core gameplay, and ads.

## Website

- Eight published locales: US English, Canadian English, Canadian French, Spanish, Portuguese, French, German and Italian.
- About, features, download, FAQ, tips, blog, guide and comparison pages in each published locale.
- Localized feature detail pages, country flag images, canonical URLs, reciprocal hreflang, Open Graph and Schema.org structured data.
- Google Play screenshots and app icon, plus tracked Google Play calls to action.
- Generated XML and text sitemaps, robots.txt and llms.txt.

## Build and validate

```bash
python -m unittest discover -s tests -v
python scripts/build.py
python scripts/validate.py
```

The generated static site is written to `dist/`. GitHub Actions tests, builds, validates and deploys the site to GitHub Pages from `main`.

## Content source

Product claims and screenshots are based on the official Google Play listing. Search-volume estimates are not asserted; keyword groups are starting targets for review in Search Console.
