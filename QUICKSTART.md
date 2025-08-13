# 🚀 Quick Start Guide

## Get Started in 3 Easy Steps

### 1. 🐍 Check Python Version
Make sure you have Python 3.10 or higher:
```bash
python --version
```

### 2. 🚀 Run Setup (Choose Your Platform)

**Windows:**
```bash
setup.bat
```

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Manual Setup:**
```bash
python setup.py
```

### 3. 🔑 Get Your API Key
1. Go to [Etherscan API](https://etherscan.io/apis)
2. Create a free account
3. Generate an API key
4. Edit the `.env` file and replace `your_api_key_here` with your actual key

### 4. 🎯 Start Scanning Wallets
```bash
python wallet_security_agent.py
```

## 🧪 Test the Agent First
Before scanning real wallets, test the functionality:
```bash
python test_agent.py
```

## 📱 Example Usage
```
🔒 Sentient Wallet Security AI Agent
========================================

Enter an EVM wallet address to scan (or 'quit' to exit):
Address: 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6

==================================================
🔒 WALLET SECURITY REPORT
==================================================
Address: 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6
Risk Score: 0/100
Risk Level: 🟢 SAFE

✅ No security issues detected

💡 RECOMMENDATIONS:
  ✅ Wallet appears safe - no suspicious activity detected
==================================================
```

## 🆘 Need Help?
- Check the main [README.md](README.md) for detailed information
- Ensure your `.env` file contains the correct API key
- Make sure you have an internet connection for API calls

## 🔒 Security Features
- ✅ Address validation
- ✅ Transaction analysis
- ✅ Malicious contract detection
- ✅ Risk scoring (0-100)
- ✅ Personalized recommendations
- ✅ Privacy-first (no private keys needed)
