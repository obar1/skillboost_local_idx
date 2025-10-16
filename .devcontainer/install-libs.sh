#!/bin/bash
set -e

# Update package list and install required libraries
apt-get update && \
apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 && \
apt-get clean
