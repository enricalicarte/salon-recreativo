# Salón Recreativo
Escaparate de juegos. Web estática: `index.html` + carpeta `juegos/`.
Publicar: Settings → Pages → Deploy from a branch → `main` / root.

## SEO
`python3 tools/build_seo.py` regenera `index.html`, `jugar/*/index.html` (una página por juego), `sitemap.xml`, `robots.txt` y `404.html` a partir de `tools/source.html` y `tools/games.json`.
