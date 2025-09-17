#!/bin/bash

# PyMCP-C2 Installation Script

echo "Installing PyMCP-C2..."

# Check Python version
python3 -c 'import sys; print("Python version: ", sys.version)'
if [ $? -ne 0 ]; then
    echo "Python 3 is required. Please install it first."
    exit 1
fi

# Create virtual environments
echo "Creating virtual environments..."
python3 -m venv mcp_server/venv
python3 -m venv mcp_agent/venv
python3 -m venv mcp_console/venv

# Install server dependencies
echo "Installing server dependencies..."
cd mcp_server
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

# Install agent dependencies
echo "Installing agent dependencies..."
cd mcp_agent
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

# Install console dependencies
echo "Installing console dependencies..."
cd mcp_console
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

echo "Installation complete!"
echo "Please set up your environment variables in .env file"
echo "And generate SSL certificates with:"
echo "openssl req -x509 -newkey rsa:4096 -keyout mcp_server/key.pem -out mcp_server/cert.pem -days 365 -nodes"
