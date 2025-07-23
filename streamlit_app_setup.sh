#!/bin/bash

# Exit on error and print commands
set -ex

# Set timezone to prevent tzdata interactive prompt
export DEBIAN_FRONTEND=noninteractive
ln -fs /usr/share/zoneinfo/UTC /etc/localtime

# Update package lists and upgrade existing packages
echo "Updating and upgrading system packages..."
apt-get update
apt-get upgrade -y

# Install system dependencies
echo "Installing system dependencies..."
apt-get install -y --no-install-recommends \
    libxml2-dev \
    libxslt1-dev \
    python3-lxml \
    python3-dev \
    python3-pip \
    python3-venv \
    gcc \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv /home/adminuser/venv
source /home/adminuser/venv/bin/activate

# Upgrade pip and setuptools first
python -m pip install --upgrade pip==23.0.1 setuptools==68.0.0 wheel==0.40.0

# Install build dependencies first
python -m pip install --no-cache-dir numpy==1.24.3

# Install other requirements
echo "Installing Python dependencies..."
python -m pip install --no-cache-dir -r requirements.txt

# Verify installation
echo "Verifying installations..."
python -c "import pandas; print(f'Pandas version: {pandas.__version__}')"
python -c "import streamlit; print(f'Streamlit version: {streamlit.__version__}')"

echo "✅ Setup completed successfully!"
exit 0
