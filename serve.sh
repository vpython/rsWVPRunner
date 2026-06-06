#!/bin/bash
# Serves the RapydScript runner on port 8090.
#
# FLASK_HOST must match the origin of the flaskHost that will load this runner
# in an iframe, because run.html uses it as the trusted postMessage origin.
# Default is localhost for normal dev; override for external device testing:
#
#   FLASK_HOST=http://192.168.1.66:8080 ./serve.sh
#
# --bind 0.0.0.0 makes the server reachable on all network interfaces, not
# just localhost, so tablets and phones on the same network can access it.

FLASK_HOST=${FLASK_HOST:-"http://localhost:8080"}
sed "s|TRUSTED_HOST_TEMPLATE|$FLASK_HOST|g" untrusted/run.html.template > untrusted/run.html
echo "Serving rsWVPRunner on port 8090 (trusted host: $FLASK_HOST)"
python3 -m http.server 8090 --bind 0.0.0.0
