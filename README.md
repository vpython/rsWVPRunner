# This is a static deployment of a RapydScript runner

This is a runner for RapydScript WebVPython programs. The runner must be embedded as an iframe within a host application. The host communicates with the runner through the iframe's "postMessage" method.

The runner can send results, errors, and screen grabs to the host window postMessge.

You must configure the "trusted host" environment variable on the deployed system to match the root URL of the host using this runner.

Because this is a static deployment, you need to configure the trusted host in the /untrusted/run.html file.
