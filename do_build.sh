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

# Assemble deploy/ from ONLY the assets the runner serves in production.
# Everything else in the repo is build/dev-only and must never be published:
#   build-tools/ __pycache__/ build.env* build_package.py do_build.sh serve.sh
#   README.md config.json .vscode/ .DS_Store and other dotfiles, plus the
#   untrusted/ template, editor backups and samples.
rm -rf deploy
mkdir -p deploy/untrusted

# Runtime asset directories (served as-is).
cp -r css lib package shaders deploy/

# Runtime root files.
cp favicon.ico index.html deploy/

# untrusted/: only the files the runner loads (not the template/backups/samples).
cp untrusted/run.js deploy/untrusted/
[ -d untrusted/images ] && cp -r untrusted/images deploy/untrusted/

# Generate run.html from template (TRUSTED_HOST baked in) and stamp run.js.
sed "s|TRUSTED_HOST_TEMPLATE|$TRUSTED_HOST|g" untrusted/run.html.template > deploy/untrusted/run.html
BUILD_DATE=$(date +%Y%m%d%H%M)
sed -i '' "s|PACKAGE_BUILD_TEMPLATE|$BUILD_DATE|g" deploy/untrusted/run.js

# Upload to GCS. NOTE: cp is additive — it does not remove objects already in the
# bucket, so stale files from earlier full-repo deploys must be cleaned out once.
echo "Uploading to $BUCKET..."
gsutil -m cp -r deploy/* $BUCKET/

echo "=== Deploy complete! ==="
