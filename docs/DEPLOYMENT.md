# Deployment Guide

## Server Deployment
1. Install dependencies: `pip install -r requirements.txt`
2. Generate SSL certificates: `openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes`
3. Set environment variables: `cp .env.example .env` and edit
4. Start server: `python server.py`

## Agent Deployment
1. Install dependencies: `pip install -r requirements.txt`
2. Configure agent: edit `config/office_b_agent.yaml`
3. Run agent: `python agent.py --server-url https://server-ip:443`

## Console Deployment
1. Install dependencies: `pip install -r requirements.txt`
2. Set OpenAI API key: `export OPENAI_API_KEY=your-key`
3. Run console: `python console.py --server-url https://server-ip:443`

## Metasploit Integration
1. Start Metasploit RPC: `msfrpcd -P your-password -S -f`
2. Configure environment variables for RPC connection
3. Use `msf_exploit` command in console

