#!/bin/bash

# Install system dependencies
apt-get update
apt-get install -y \
    libxml2-dev \
    libxslt1-dev \
    python3-lxml \
    python3-dev \
    python3-pip \
    python3-venv

# Create and activate virtual environment
python3 -m venv /home/adminuser/venv
source /home/adminuser/venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install any additional packages that might be needed
pip install pyarrow  # Required for pandas on some systems

echo "Setup completed successfully"
