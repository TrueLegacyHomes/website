#!/bin/bash
set -e

# Estate Sales - Part 1: Website Pages Only
# Run this first, review staging, then run the email script separately

WORKSPACE="/Users/admin/.openclaw/workspace/tlh-rebuild"
SCRIPTS="/Users/admin/.openclaw/workspace/scripts"
TMP_DIR="/tmp/estate-sales-$(date +%s)"

echo "🏠 Estate Sales Update - Part 1: Website Pages"
echo "📁 Working directory: $WORKSPACE"
echo "📦 Temp directory: $TMP_DIR"
mkdir -p "$TMP_DIR"

# Step 1: Fetch sales from EstateSales.net
echo ""
echo "📥 Step 1: Fetching sales from EstateSales.net..."
cd "$SCRIPTS"
node fetch-estatesales-company.js 137708 > "$TMP_DIR/sales-raw.json" 2>&1

# Extract just the JSON (skip stderr)
cat "$TMP_DIR/sales-raw.json" | grep -A 9999 '^\[' > "$TMP_DIR/sales.json"

SALE_IDS=$(cat "$TMP_DIR/sales.json" | jq -r '.[].id')
SALE_COUNT=$(echo "$SALE_IDS" | wc -l | tr -d ' ')
echo "✅ Found $SALE_COUNT sales"

# Step 2: Match addresses from your input file
echo ""
echo "📍 Step 2: Matching addresses by zip code..."

INPUT_FILE="$WORKSPACE/scripts/addresses-input.txt"

if [ ! -f "$INPUT_FILE" ]; then
  echo "❌ ERROR: addresses-input.txt not found!"
  echo "   Create it at: $INPUT_FILE"
  exit 1
fi

# Parse input addresses (skip comments and empty lines)
grep -v '^#' "$INPUT_FILE" | grep -v '^[[:space:]]*$' > "$TMP_DIR/input-addresses.txt"

if [ ! -s "$TMP_DIR/input-addresses.txt" ]; then
  echo "❌ ERROR: No addresses found in addresses-input.txt!"
  echo "   Please paste addresses into: $INPUT_FILE"
  exit 1
fi

ADDRESS_COUNT=$(wc -l < "$TMP_DIR/input-addresses.txt" | tr -d ' ')
echo "   Found $ADDRESS_COUNT addresses in input file"

# Extract sales with zip codes
cat "$TMP_DIR/sales.json" | jq -r '.[] | "\(.id)|\(.city)|\(.zip)"' > "$TMP_DIR/sale-locations.txt"

> "$TMP_DIR/addresses.txt"  # Clear file

while read line; do
  sale_id=$(echo "$line" | cut -d'|' -f1)
  city=$(echo "$line" | cut -d'|' -f2 | sed 's/ /-/g')
  zip=$(echo "$line" | cut -d'|' -f3)
  
  echo "  Matching sale $sale_id (zip: $zip)..."
  
  # Find matching address by zip code
  matched_address=$(grep -i "$zip" "$TMP_DIR/input-addresses.txt" | head -1)
  
  if [ -n "$matched_address" ]; then
    # Parse the address: "Street, City, ST Zip"
    street=$(echo "$matched_address" | sed 's/,.*$//')
    echo "$sale_id|$street|$(echo $city | sed 's/-/ /g')|$zip" >> "$TMP_DIR/addresses.txt"
    echo "    ✅ $street"
  else
    echo "    ⚠️  No match found for zip $zip"
    echo "$sale_id|Address TBD|$(echo $city | sed 's/-/ /g')|$zip" >> "$TMP_DIR/addresses.txt"
  fi
done < "$TMP_DIR/sale-locations.txt"

# Step 3: Extract images with Playwright
echo ""
echo "🖼️  Step 3: Extracting images with Playwright..."
for sale_id in $SALE_IDS; do
  echo "  Extracting sale $sale_id..."
  node "$SCRIPTS/extract-estatesales-images.js" "$sale_id" > "$TMP_DIR/sale-${sale_id}-guids.txt" 2>&1
  guid_count=$(grep -o '[0-9a-f-]\{36\}' "$TMP_DIR/sale-${sale_id}-guids.txt" | wc -l | tr -d ' ')
  echo "    ✅ $guid_count GUIDs extracted"
done

# Step 4: Validate images (critical - removes 403s)
echo ""
echo "✅ Step 4: Validating images (parallel)..."
for sale_id in $SALE_IDS; do
  echo "  Validating sale $sale_id..."
  grep -o '[0-9a-f-]\{36\}' "$TMP_DIR/sale-${sale_id}-guids.txt" | xargs -P 20 -I {} sh -c '
    code=$(curl -s -o /dev/null -w "%{http_code}" "https://picturescdn.estatesales.net/'"$sale_id"'/1-2/{}.jpg")
    [ "$code" = "200" ] && echo "{}"
  ' > "$TMP_DIR/sale-${sale_id}-validated.txt" || true
  
  validated_count=$(wc -l < "$TMP_DIR/sale-${sale_id}-validated.txt" | tr -d ' ')
  echo "    ✅ $validated_count images validated"
done

# Step 5: Generate static site pages
echo ""
echo "📄 Step 5: Generating website pages..."
cd "$WORKSPACE"
git checkout staging
git pull origin staging

chmod +x "$WORKSPACE/scripts/generate-pages.py"
python3 "$WORKSPACE/scripts/generate-pages.py" "$TMP_DIR"

# Step 6: Commit to staging
echo ""
echo "📤 Step 6: Pushing to staging..."
git add -A
git commit -m "Update estate sales for $(date +%Y-%m-%d)"
git push origin staging

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ PART 1 COMPLETE - Website Pages Created!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📊 Summary:"
echo "   Sales processed: $SALE_COUNT"
echo "   Temp directory: $TMP_DIR"
echo ""
echo "🌐 Review staging site:"
echo "   https://staging.website-252.pages.dev/upcoming-sales/"
echo ""
echo "🚀 Next Steps:"
echo "   1. Review the staging site"
echo "   2. When ready, tell Clark: 'run the estate sales email script'"
echo "   3. After email is created, push to production:"
echo "      → cd $WORKSPACE"
echo "      → git checkout main && git merge staging && git push origin main"
echo ""
echo "💾 Data saved for email script:"
echo "   $TMP_DIR"
echo ""
