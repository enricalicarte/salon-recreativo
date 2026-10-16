# Salón Recreativo · Alica Games Studio
Escaparate de minijuegos. Web estática para GitHub Pages (Settings → Pages → Deploy from a branch → `main` / root).

## Regenerar la web
`python3 tools/build_seo.py` genera, a partir de `tools/source.html`, `tools/games.json` y `tools/i18n.py`:
- `index.html`
- `jugar/<juego>/`: una ficha por juego
- páginas temáticas, `estudio/`, `aviso-legal/`, `privacidad/`, `cookies/`
- `sitemap.xml`, `robots.txt`, `404.html`, `manifest.webmanifest`, `sw.js`

## Configuración (arriba de `tools/build_seo.py`)
- `BASE`: URL pública. `INDEXABLE`: `False` hasta lanzar en el dominio definitivo.
- `OWNER`: titular, NIF, domicilio y email para el aviso legal, la privacidad.
- `GOATCOUNTER`: código de GoatCounter para activar la analítica sin cookies.
