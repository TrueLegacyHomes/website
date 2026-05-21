#!/bin/bash
set -e

# Estate Sales - Part 2: Mailchimp Email Only
# Run this AFTER reviewing the staging site from Part 1

WORKSPACE="/Users/admin/.openclaw/workspace/tlh-rebuild"

# Find the most recent temp directory
TMP_DIR=$(ls -dt /tmp/estate-sales-* 2>/dev/null | head -1)

if [ -z "$TMP_DIR" ] || [ ! -d "$TMP_DIR" ]; then
  echo "❌ ERROR: No estate sales data found!"
  echo ""
  echo "You need to run Part 1 first:"
  echo "  'run the estate sales pages script'"
  echo ""
  exit 1
fi

echo "📧 Estate Sales Update - Part 2: Mailchimp Email"
echo "📦 Using data from: $TMP_DIR"
echo ""

# Check if required files exist
if [ ! -f "$TMP_DIR/sales.json" ] || [ ! -f "$TMP_DIR/addresses.txt" ]; then
  echo "❌ ERROR: Missing required data files in $TMP_DIR"
  echo ""
  echo "You need to run Part 1 first:"
  echo "  'run the estate sales pages script'"
  echo ""
  exit 1
fi

# Generate Mailchimp email
echo "🔨 Generating Mailchimp email..."
python3 "$WORKSPACE/scripts/generate-mailchimp-email.py" "$TMP_DIR"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ PART 2 COMPLETE - Mailchimp Email Created!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📧 Mailchimp:"
echo "   Status: DRAFT (ready to review/send)"
echo "   Email HTML: $TMP_DIR/email.html"
echo ""
echo "🚀 Next Steps:"
echo "   1. Review the Mailchimp draft (check preview link above)"
echo "   2. Send when ready via Mailchimp dashboard"
echo ""
