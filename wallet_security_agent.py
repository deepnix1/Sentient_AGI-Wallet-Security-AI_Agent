#!/usr/bin/env python3
"""
EVM Wallet Security AI Agent
Scans EVM wallet addresses for security risks and provides risk assessment
"""

import os
import re
import requests
from typing import Dict, List, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WalletSecurityAgent:
    def __init__(self):
        self.api_key = os.getenv('ETHERSCAN_API_KEY')
        if not self.api_key:
            raise ValueError("ETHERSCAN_API_KEY not found in .env file")
        
        # Known malicious contract patterns and addresses
        # In a production environment, this would be fetched from a real-time database
        self.malicious_patterns = {
            'phishing_scam': [
                '0x1234567890123456789012345678901234567890',  # Example phishing address
                '0xabcdefabcdefabcdefabcdefabcdefabcdefabcd',  # Example scam address
            ],
            'honeypot': [
                '0x1111111111111111111111111111111111111111',  # Example honeypot
            ],
            'rugpull': [
                '0x2222222222222222222222222222222222222222',  # Example rugpull
            ]
        }
        
        # Risk weights for different types of malicious activities
        self.risk_weights = {
            'phishing_scam': 30,
            'honeypot': 25,
            'rugpull': 20,
            'suspicious_pattern': 15,
            'high_frequency_trading': 10
        }

    def validate_address(self, address: str) -> bool:
        """Validate EVM wallet address format"""
        if not address.startswith('0x'):
            return False
        if len(address) != 42:
            return False
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            return False
        return True

    def get_transactions(self, address: str) -> List[Dict]:
        """Fetch transaction history from Etherscan API"""
        url = "https://api.etherscan.io/api"
        params = {
            'module': 'account',
            'action': 'txlist',
            'address': address,
            'startblock': 0,
            'endblock': 99999999,
            'sort': 'desc',
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == '1':
                return data['result']
            else:
                print(f"API Error: {data.get('message', 'Unknown error')}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching transactions: {e}")
            return []

    def analyze_transactions(self, transactions: List[Dict]) -> Tuple[int, List[str]]:
        """Analyze transactions for security risks"""
        risk_score = 0
        findings = []
        
        if not transactions:
            return risk_score, findings
        
        # Check for malicious contract interactions
        for tx in transactions:
            to_address = tx.get('to', '')
            if to_address in self.malicious_patterns['phishing_scam']:
                risk_score += self.risk_weights['phishing_scam']
                findings.append(f"⚠️ Interaction with {to_address[:10]}... - Phishing scam detected")
            
            elif to_address in self.malicious_patterns['honeypot']:
                risk_score += self.risk_weights['honeypot']
                findings.append(f"⚠️ Interaction with {to_address[:10]}... - Honeypot contract detected")
            
            elif to_address in self.malicious_patterns['rugpull']:
                risk_score += self.risk_weights['rugpull']
                findings.append(f"⚠️ Interaction with {to_address[:10]}... - Rugpull contract detected")
        
        # Check for suspicious patterns
        if len(transactions) > 100:
            risk_score += self.risk_weights['high_frequency_trading']
            findings.append("⚠️ High frequency trading detected - potential bot activity")
        
        # Check for failed transactions (potential scam attempts)
        failed_txs = [tx for tx in transactions if tx.get('isError') == '1']
        if len(failed_txs) > 10:
            risk_score += 10
            findings.append("⚠️ Multiple failed transactions detected - potential scam attempts")
        
        # Cap risk score at 100
        risk_score = min(risk_score, 100)
        
        return risk_score, findings

    def get_risk_level(self, risk_score: int) -> str:
        """Convert risk score to human-readable risk level"""
        if risk_score == 0:
            return "🟢 SAFE"
        elif risk_score <= 25:
            return "🟡 LOW RISK"
        elif risk_score <= 50:
            return "🟠 MEDIUM RISK"
        elif risk_score <= 75:
            return "🔴 HIGH RISK"
        else:
            return "🔴 CRITICAL RISK"

    def get_recommendations(self, risk_score: int, findings: List[str]) -> List[str]:
        """Generate security recommendations based on risk assessment"""
        recommendations = []
        
        if risk_score == 0:
            recommendations.append("✅ Wallet appears safe - no suspicious activity detected")
        else:
            if any("Phishing scam" in finding for finding in findings):
                recommendations.append("🚨 IMMEDIATE ACTION: Revoke all token approvals to suspicious contracts")
                recommendations.append("🔒 Check for unauthorized transactions and report if funds are missing")
            
            if any("Honeypot" in finding for finding in findings):
                recommendations.append("⚠️ Be cautious - some contracts may be designed to trap users")
                recommendations.append("🔍 Research contracts before interacting with them")
            
            if any("Rugpull" in finding for finding in findings):
                recommendations.append("💸 Potential rugpull detected - avoid similar contracts in the future")
                recommendations.append("📚 Learn about common DeFi scams and red flags")
            
            recommendations.append("🔐 Use hardware wallets for large holdings")
            recommendations.append("📱 Enable 2FA on all exchange accounts")
            recommendations.append("🔍 Always verify contract addresses before transactions")
        
        return recommendations

    def generate_report(self, address: str, risk_score: int, findings: List[str], recommendations: List[str]) -> str:
        """Generate a formatted security report"""
        report = []
        report.append("=" * 50)
        report.append("🔒 SENTIENT WALLET SECURITY REPORT")
        report.append("=" * 50)
        report.append(f"Address: {address}")
        report.append(f"Risk Score: {risk_score}/100")
        report.append(f"Risk Level: {self.get_risk_level(risk_score)}")
        report.append(f"👨‍💻 Analyzed by: @jackyjoeeth")
        report.append("")
        
        if findings:
            report.append("🚨 SECURITY FINDINGS:")
            for finding in findings:
                report.append(f"  {finding}")
        else:
            report.append("✅ No security issues detected")
        
        report.append("")
        report.append("💡 RECOMMENDATIONS:")
        for rec in recommendations:
            report.append(f"  {rec}")
        
        report.append("")
        report.append("=" * 50)
        report.append("Report generated by Sentient Wallet Security AI Agent")
        report.append("Powered by @jackyjoeeth")
        report.append("=" * 50)
        
        return "\n".join(report)

    def scan_wallet(self, address: str) -> str:
        """Main method to scan a wallet and return security report"""
        print(f"🔍 Scanning wallet: {address}")
        
        # Validate address
        if not self.validate_address(address):
            return "❌ Invalid EVM address format. Address must start with '0x' and be 42 characters long."
        
        # Fetch transactions
        print("📡 Fetching transaction history...")
        transactions = self.get_transactions(address)
        
        if not transactions:
            return "❌ Unable to fetch transaction history. Please check the address and try again."
        
        print(f"📊 Analyzing {len(transactions)} transactions...")
        
        # Analyze for risks
        risk_score, findings = self.analyze_transactions(transactions)
        
        # Generate recommendations
        recommendations = self.get_recommendations(risk_score, findings)
        
        # Generate and return report
        return self.generate_report(address, risk_score, findings, recommendations)


def main():
    """Main function to run the wallet security agent"""
    print("🔒 Sentient Wallet Security AI Agent")
    print("=" * 40)
    
    try:
        agent = WalletSecurityAgent()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("Please create a .env file with your ETHERSCAN_API_KEY")
        return
    
    while True:
        print("\nEnter an EVM wallet address to scan (or 'quit' to exit):")
        address = input("Address: ").strip()
        
        if address.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye! Stay safe!")
            break
        
        if not address:
            print("❌ Please enter a valid address")
            continue
        
        print("\n" + "=" * 50)
        report = agent.scan_wallet(address)
        print(report)
        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
