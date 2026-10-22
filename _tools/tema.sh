#!/bin/sh
# Genera export/tema-llananzanes.zip (completo) y export/tema-llananzanes-ligero.zip (sin foto/vídeo/audio)
set -e
R=$(cd "$(dirname "$0")/.." && pwd); T=$(mktemp -d); D=$T/llananzanes
mkdir -p $D && cp "$R"/_tools/tema/*.php "$R"/_tools/tema/style.css $D/ && rsync -a "$R"/web/ $D/web/
cd $T && rm -f "$R"/export/tema-llananzanes*.zip
zip -qr "$R"/export/tema-llananzanes.zip llananzanes
zip -qr "$R"/export/tema-llananzanes-ligero.zip llananzanes -x 'llananzanes/web/assets/img/*' 'llananzanes/web/assets/video/*' 'llananzanes/web/assets/audio/*'
ls -lh "$R"/export/tema-llananzanes*.zip | awk '{print $5, $9}'
