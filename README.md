# PyMCP-C2 (Python Master Control Program - Command & Control)

A modular, Python-based Command and Control (C2) framework designed for educational purposes and authorized red team security testing. This project integrates an AI-assisted operator console to provide tactical suggestions during an engagement.

---

## ⚠️ LEGAL AND ETHICAL WARNING ⚠️

**PYMCP-C2 IS STRICTLY FOR AUTHORIZED SECURITY TESTING AND EDUCATIONAL PURPOSES ONLY.**

### IMPORTANT LEGAL NOTICE

1. **LAWFUL USE ONLY**: This software may only be used on systems for which you have explicit, written permission from the owner. Unauthorized use is illegal and may result in criminal charges.

2. **COMPLIANCE WITH LAWS**: Users are solely responsible for ensuring their use of this tool complies with all applicable local, state, national, and international laws and regulations.

3. **NO WARRANTY**: This software is provided "as is" without any warranty. The developers assume no liability for damages or legal issues resulting from the use or misuse of this tool.

4. **ETHICAL GUIDELINES**: 
   - Always obtain proper authorization before testing
   - Respect privacy and data integrity
   - Do not cause damage to systems
   - Report vulnerabilities responsibly
   - Maintain confidentiality of findings

5. **EXPORT CONTROL**: This software may be subject to export control regulations. By using this software, you confirm that you are not in a country where such export would be prohibited.

### Intended Use Cases
- Authorized penetration testing engagements
- Security research with proper authorization
- Educational purposes in controlled environments
- Red team exercises with explicit permission

### Prohibited Uses
- Unauthorized access to computer systems
- Network reconnaissance without permission
- Data exfiltration without authorization
- Disruption of services or systems
- Any illegal activities

By using this software, you acknowledge that you understand and agree to these terms and assume full responsibility for your actions.

---

## Features

* **Python-based Server & Agent:** Cross-platform and easy to modify.
* **RESTful API:** C2 communication over standard HTTP/S protocols.
* **Modular Agent Tasks:** Easily extend agent capabilities.
* **AI-Powered Console:** Integrated OpenAI (GPT) assistant for reconnaissance analysis and tactical advice.
* **Metasploit Integration:** Access to Metasploit's exploit library and automation capabilities.
* **Encrypted Communications:** All communications are encrypted using AES-256.
* **Authentication:** JWT-based authentication for agents and operators.
* **Comprehensive Logging:** Detailed logging for audit and analysis.

## Project Structure

# PyMCP-C2/
## ├──mcp_server/          # C2 Server component
## ├──mcp_agent/           # Agent implant
## ├──mcp_console/         # Operator console with AI
## ├──docs/                # Documentation
## ├──tests/               # Test cases
## ├──scripts/             # Utility scripts
## └──config/              # Configuration files


## Getting Started

### Prerequisites

* Python 3.8+
* An OpenAI API Key (for the AI features)
* Metasploit Framework (optional, for Metasploit integration)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/PyMCP-C2.git
    cd PyMCP-C2
    ```

2. Run the installation script:
    ```bash
    ./scripts/install.sh
    ```

3. Alternatively, install dependencies manually:
    ```bash
    pip install -r requirements.txt
    cd mcp_server && pip install -r requirements.txt
    cd ../mcp_agent && pip install -r requirements.txt
    cd ../mcp_console && pip install -r requirements.txt
    ```

4. Set up environment variables:
    ```bash
    cp .env.example .env
    # Edit .env with your settings
    ```

### Usage

1. **Start the Server:**
    ```bash
    cd mcp_server
    python server.py
    ```

2. **Run an Agent:**
    ```bash
    cd mcp_agent
    python agent.py --server-url https://your-server-ip:443
    ```

3. **Launch the Operator Console:**
    ```bash
    cd mcp_console
    python console.py --server-url https://localhost:443
    ```

## Documentation

For detailed documentation, see the [docs](docs/) directory:

- [SECURITY.md](docs/SECURITY.md) - Security protocols and best practices
- [LAWFUL_USE.md](docs/LAWFUL_USE.md) - Legal and ethical guidelines
- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deployment guide

## Contributing

We welcome contributions! Please read our contributing guidelines before submitting a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- 📧 Email: security@example.com
- 🐛 Issues: GitHub Issues page
- 📚 Documentation: GitHub Wiki

## Security

To report security vulnerabilities, please email security@example.com rather than creating a public issue.
