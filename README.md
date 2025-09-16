# PyMCP-C2 (Python Master Control Program)

A modular, Python-based Command and Control (C2) framework designed for educational purposes and authorized red team security testing. This project integrates an AI-assisted operator console to provide tactical suggestions during an engagement.

---

### **⚠️ Ethical Use Warning ⚠️**

This tool is intended for use in authorized security research and penetration testing engagements **only**. Using this tool against systems without explicit, written permission from the system owner is illegal. The developers of this project are not responsible for any misuse or damage caused by this program.

---

### Features

* **Python-based Server & Agent:** Cross-platform and easy to modify.
* **RESTful API:** C2 communication over standard HTTP/S protocols.
* **Modular Agent Tasks:** Easily extend agent capabilities.
* **AI-Powered Console:** Integrated OpenAI (GPT) assistant for reconnaissance analysis and tactical advice.

### Project Structure

```

PyMCP-C2/ ├──mcp_server/          # C2 Server component ├──mcp_agent/           # Agent implant ├──mcp_console/         # Operator console with AI ├──docs/                # Documentation └──tests/               # Test cases

```

### Getting Started

#### Prerequisites

* Python 3.8+
* An OpenAI API Key (for the AI features)

#### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/PyMCP-C2.git
    cd PyMCP-C2
    ```
2.  Install dependencies for each component:
    ```bash
    cd mcp_server && pip install -r requirements.txt
    cd ../mcp_agent && pip install -r requirements.txt
    cd ../mcp_console && pip install -r requirements.txt
    ```
3.  Configure the server and agent with your IP address.

### Usage

1.  **Start the Server:**
    ```bash
    cd mcp_server
    python server.py
    ```
2.  **Run an Agent:**
    ```bash
    cd mcp_agent
    python agent.py
    ```
3.  **Launch the Operator Console:**
    ```bash
    cd mcp_console
    python console.py
    ```

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
