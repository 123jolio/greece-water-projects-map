#!/bin/bash
set -e

echo "===== Setting up Python 3.10 environment ====="

# Update package lists
echo "Updating package lists..."
apt-get update -qq

# Install Python 3.10 and required system packages
echo "Installing Python 3.10 and system dependencies..."
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    python3-pip \
    python3-wheel \
    libxml2-dev \
    libxslt1-dev \
    gcc \
    g++ \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    proj-data \
    proj-bin \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.10 as the default
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
update-alternatives --set python3 /usr/bin/python3.10

# Upgrade pip and setuptools
echo "Upgrading pip and setuptools..."
python3 -m pip install --upgrade pip setuptools wheel

# Create and activate virtual environment
python3 -m venv /home/adminuser/venv
source /home/adminuser/venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install any additional packages that might be needed
pip install pyarrow  # Required for pandas on some systems

echo "Setup completed successfully"
