#!/bin/bash

# Exit on error
set -e

# Update package lists
echo "Updating package lists..."
apt-get update

# Install system dependencies
echo "Installing system dependencies..."
apt-get install -y \
    libxml2-dev \
    libxslt1-dev \
    python3-lxml \
    python3-dev \
    python3-pip \
    python3-venv \
    gcc \
    g++

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv /home/adminuser/venv
source /home/adminuser/venv/bin/activate

# Upgrade pip and setuptools
echo "Upgrading pip and setuptools..."
pip install --upgrade pip setuptools wheel

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setup completed successfully"
