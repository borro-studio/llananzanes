# El Mirador de Llananzanes · rediseño web (borrador)

Rediseño de la web de El Mirador de Llananzanes, casas rurales en Llananzanes (Aller, Asturias). Trabajo de Borro Studio.

- **Vista previa:** https://borro-studio.github.io/llananzanes/
- `web/`: la web, HTML estático sin dependencias externas (fuentes e iconos en local).
- `_tools/`: scripts de capturas, vídeo y exportación a PDF / Illustrator.

Borrador en revisión: las páginas llevan `noindex`.

## Publicar cambios

```bash
git add -A && git commit -m "..." && git push
git subtree push --prefix web origin gh-pages
```
