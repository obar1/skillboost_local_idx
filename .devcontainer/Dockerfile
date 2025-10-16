
# Use the official Python dev container base image
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# Copy the install script into the container
COPY install-libs.sh /tmp/install-libs.sh

# Make the script executable and run it
RUN chmod +x /tmp/install-libs.sh && /tmp/install-libs.sh

# Clean up the script after installation
RUN rm /tmp/install-libs.sh
