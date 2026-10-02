#!/usr/bin/env bash
# Renders the Luma cover images to share/ using headless Chrome.
#   bash tools/luma/render.sh
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p ../../share
CHROME=${CHROME:-google-chrome}
for variant in abstract photo; do
  query=""; [ "$variant" = photo ] && query="?bg=photo"
  "$CHROME" --headless=new --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --virtual-time-budget=8000 --window-size=1600,1600 \
    --screenshot="../../share/luma-cover-$variant.png" "file://$PWD/cover.html$query" 2>/dev/null
  echo "share/luma-cover-$variant.png"
done
