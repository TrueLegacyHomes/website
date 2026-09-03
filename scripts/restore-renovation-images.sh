#!/usr/bin/env bash
# restore-renovation-images.sh
# Downloads renovation property images from Wayback Machine
# Run this from the tlh-rebuild root directory
# Usage: bash scripts/restore-renovation-images.sh

set -e

REPO="$(cd "$(dirname "$0")/.." && pwd)/renovations"
WB_STAMP="20260405090138"
WB_BASE="http://web.archive.org/web/${WB_STAMP}id_"
CW="https://wordpress-1007224-3553830.cloudwaysapps.com/wp-content/uploads"

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

download_image() {
  local addr="$1"
  local yearmonth="$2"
  local filename="$3"
  local out="$REPO/$addr/images/$filename"

  if [ -f "$out" ] && [ -s "$out" ]; then
    echo "  [skip] $filename"
    return
  fi

  local src_url="${WB_BASE}/${CW}/${yearmonth}/${filename}"
  echo "  [dl]   $filename"
  curl -sL --max-time 60 --retry 3 --retry-delay 2 \
    -A "$UA" \
    -o "$out" \
    "$src_url"
  
  # Verify it's actually an image (not an error page)
  local size=$(wc -c < "$out" 2>/dev/null || echo 0)
  if [ "$size" -lt 5000 ]; then
    echo "  [WARN] $filename may be corrupt (${size} bytes) — check manually"
  else
    echo "  [ok]   $filename (${size} bytes)"
  fi
  sleep 0.5
}

echo "=== Restoring 25112-vespucci-rd ==="
mkdir -p "$REPO/25112-vespucci-rd/images"
for f in \
  1-2-1030x686.jpg 2-2-1030x548.jpg 4-3-1030x776.jpg 5-2-1030x693.jpg \
  6-2-1030x686.jpg 8-3-1030x686.jpg 9-2-1030x686.jpg 11-3-1030x698.jpg \
  12-3-1030x686.jpg 13-2-1030x686.jpg 14-3-1030x686.jpg 16-2-1030x692.jpg \
  17-2-1030x922.jpg 18-2-1030x698.jpg 19-2-1030x686.jpg 20-2-1030x693.jpg \
  21-2-1030x686.jpg 24-2-1030x686.jpg 27-2-1030x698.jpg 29-1-1030x686.jpg; do
  download_image "25112-vespucci-rd" "2025/08" "$f"
done

echo ""
echo "=== Restoring 8195-dracaena-dr ==="
mkdir -p "$REPO/8195-dracaena-dr/images"
for f in \
  1-cropped-1030x823.jpg 3-1-1030x686.jpg 4-1-1030x686.jpg 6-1030x686.jpg \
  7-1-1030x705.jpg 8-1-1030x686.jpg 9-1030x705.jpg 10-1-1030x752.jpg \
  11-1-1030x734.jpg 12-1-1030x686.jpg 14-1-1030x686.jpg 15-1-1030x705.jpg \
  16-1030x686.jpg 17-1030x686.jpg 19-1030x686.jpg 20-1030x686.jpg \
  21-1030x686.jpg 22-1-1030x686.jpg 23-1-1030x722.jpg 24-1030x686.jpg; do
  download_image "8195-dracaena-dr" "2025/08" "$f"
done

echo ""
echo "=== Restoring 33-grassy-knoll-ln ==="
mkdir -p "$REPO/33-grassy-knoll-ln/images"
for f in \
  1-1030x686.jpg 2-1030x674.jpg 3-1030x686.jpg 4-1030x692.jpg \
  5-1030x686.jpg 7-1030x745.jpg 8-1030x686.jpg 10-1030x686.jpg \
  11-1030x706.jpg 12-1030x686.jpg 13-1030x686.jpg 14-1030x686.jpg \
  15-1030x686.jpg 18-1030x686.jpg 22-1030x686.jpg 23-1030x687.jpg \
  25-1030x686.jpg 27-1030x695.jpg 30-1030x726.jpg 34-1030x686.jpg; do
  download_image "33-grassy-knoll-ln" "2025/08" "$f"
done

echo ""
echo "=== Restoring 5432-marjan-ave ==="
mkdir -p "$REPO/5432-marjan-ave/images"
for f in \
  1-11-1030x577.jpg 2-9-1030x686.jpg 3-12-1030x686.jpg 4-14-1030x686.jpg \
  5-13-1030x686.jpg 7-13-1030x696.jpg 10-15-1030x698.jpg 11-14-1030x693.jpg \
  12-121-9-1030x686.jpg 14-13-1030x686.jpg 15-8-1030x703.jpg 16-121-9-1030x686.jpg \
  17-14-1030x686.jpg 18-15-1030x686.jpg 19-14-1030x686.jpg 21-9-1030x686.jpg \
  22-6-1030x686.jpg 26-5-1030x686.jpg 27-3-1030x686.jpg 30-1030x686.jpg; do
  download_image "5432-marjan-ave" "2025/07" "$f"
done

echo ""
echo "=== All done ==="
echo "Images saved to renovations/<address>/images/"
echo "Run: git add renovations/*/images/ && git commit -m 'Restore renovation images from Wayback Machine'"
