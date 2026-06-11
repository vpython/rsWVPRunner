#!/bin/bash
set -e

# Load build env if present
if [ -f build.env ]; then
    source build.env
fi

TRUSTED_HOST=${TRUSTED_HOST:?"TRUSTED_HOST must be set (e.g. https://www.glowscript.org)"}
BUCKET=${BUCKET:-"gs://rswvprunner"}

echo "=== Building rsWVPRunner ==="
echo "Trusted host: $TRUSTED_HOST"
echo "Bucket: $BUCKET"

# Build deploy directory from source
rm -rf deploy
cp -r . deploy
rm -rf deploy/deploy deploy/.git

# Generate run.html from template
sed "s|TRUSTED_HOST_TEMPLATE|$TRUSTED_HOST|g" deploy/untrusted/run.html.template > deploy/untrusted/run.html

# Stamp today's date into run.js for cache-busting
BUILD_DATE=$(date +%Y%m%d%H%M)
sed -i '' "s|PACKAGE_BUILD_TEMPLATE|$BUILD_DATE|g" deploy/untrusted/run.js

# Upload to GCS
echo "Uploading to $BUCKET..."
gsutil -m cp -r deploy/* $BUCKET/

echo "=== Deploy complete! ==="
