# 🔒 Sentient Wallet Security AI Agent

## Overview
This project is an **AI-powered security agent** that scans any EVM (Ethereum Virtual Machine) wallet address and provides a **risk assessment** based on known malicious contracts and suspicious transaction patterns.  
The goal is to protect crypto users from **scams, phishing, and malicious token approvals** before they lose funds.

**Built with ❤️ by @jackyjoeeth**

The agent will:
- Take an **EVM wallet address** as input
- Fetch transaction history using the **Etherscan API**
- Check if the wallet interacted with known **malicious smart contracts**
- Assign a **risk score** and provide security recommendations
- Be built in a **single Python file** for simplicity

## Features
- **Address validation** – Ensures correct EVM format before scanning  
- **Transaction analysis** – Uses Etherscan API to retrieve wallet activity  
- **Malicious contract detection** – Compares against a database of known scam contracts  
- **Risk scoring** – Assigns a security risk level (0–100)  
- **User-friendly output** – Prints findings in a clear and readable format  
- **Privacy-first** – Non-custodial, no private keys required

## Tech Stack
- **Python 3.10+** – Core programming language
- **Etherscan API** – To fetch on-chain wallet transactions
- **Requests** – For making API calls
- **python-dotenv** – For securely storing API keys
- *(Optional)* Scam database API – For real-time malicious address checks

## Setup Instructions
### 1. Install Python
Make sure Python 3.10 or higher is installed:
```bash
python --version
```

### 2. Create Project Folder
```bash
mkdir evm-security-agent
cd evm-security-agent
```

### 3. Install Dependencies
```bash
pip install requests python-dotenv
```

### 4. Get Etherscan API Key
1. Go to [Etherscan API](https://etherscan.io/apis)
2. Create a free account
3. Generate an API key

### 5. Create `.env` File
In the project root:
```
ETHERSCAN_API_KEY=your_api_key_here
```

### 6. Build the Agent
Create a file named:
```
wallet_security_agent.py
```
It will:
- Read `.env` file for API key  
- Take EVM wallet input from the user  
- Fetch transaction history from Etherscan  
- Check for known scam contracts  
- Output a security report with risk score & recommendations  

## How the Agent Works
1. **Input**: User enters an EVM wallet address.  
2. **Validation**: Checks correct address format (starts with `0x`, 42 characters).  
3. **Fetch Data**: Queries Etherscan API for transactions.  
4. **Analyze**: Compares each transaction’s `to` address against a malicious contracts list.  
5. **Risk Scoring**: Adds points for each malicious interaction.  
6. **Output**: Prints a human-readable report.

## Running the Agent
```bash
python wallet_security_agent.py
```

Example Output:
```
=== Wallet Security Report ===
Address: 0xAbCd1234...
Risk Score: 50
Findings:
 - ⚠️ Interaction with 0xBadContract... - Phishing scam
Recommendation: High risk detected. Revoke approvals immediately.
```

## Future Improvements
- Connect to **real-time scam databases** (e.g., ScamSniffer API)  
- Multi-chain support (Polygon, BSC, Arbitrum, etc.)  
- Web dashboard for non-technical users  
- AI-based anomaly detection  
