# Cloud service to run RapydScript WebVPython programs

This is a runner for RapydScript WebVPython programs. The runner is meant to be embedded as an iframe within a host application. The host communicates with the runner through the iframe's "postMessage" method.

The runner can send results, errors, and screen grabs back to the host window postMessge.

You must configure the "trusted host" environment variable on the deployed system to match the root URL of the host using this runner.

