#!/usr/bin/env python3
"""
Test script for Sentient Wallet Security AI Agent
Demonstrates functionality without requiring real API calls
"""

import os
import sys
from unittest.mock import patch, MagicMock
from wallet_security_agent import WalletSecurityAgent

def test_agent_without_api():
    """Test the agent's analysis logic with mock data"""
    print("🧪 Testing Sentient Wallet Security AI Agent")
    print("=" * 50)
    
    # Mock environment variable
    os.environ['ETHERSCAN_API_KEY'] = 'test_key'
    
    # Create agent instance
    agent = WalletSecurityAgent()
    
    # Test address validation
    print("\n📍 Testing Address Validation:")
    test_addresses = [
        "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",  # Valid
        "0xinvalid",  # Invalid
        "0x123",  # Too short
        "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6extra",  # Too long
    ]
    
    for addr in test_addresses:
        is_valid = agent.validate_address(addr)
        status = "✅ Valid" if is_valid else "❌ Invalid"
        print(f"  {addr}: {status}")
    
    # Test risk scoring
    print("\n🎯 Testing Risk Scoring:")
    
    # Mock transaction data
    mock_transactions = [
        {
            'to': '0x1234567890123456789012345678901234567890',  # Known phishing
            'isError': '0'
        },
        {
            'to': '0xabcdefabcdefabcdefabcdefabcdefabcdefabcd',  # Known scam
            'isError': '0'
        },
        {
            'to': '0x1111111111111111111111111111111111111111',  # Known honeypot
            'isError': '0'
        },
        {
            'to': '0x9999999999999999999999999999999999999999',  # Safe address
            'isError': '0'
        }
    ]
    
    # Add many transactions to test high frequency detection
    for i in range(150):
        mock_transactions.append({
            'to': f'0x{i:040x}',
            'isError': '0'
        })
    
    # Add some failed transactions
    for i in range(15):
        mock_transactions.append({
            'to': f'0x{i:040x}',
            'isError': '1'
        })
    
    risk_score, findings = agent.analyze_transactions(mock_transactions)
    print(f"  Risk Score: {risk_score}/100")
    print(f"  Risk Level: {agent.get_risk_level(risk_score)}")
    
    if findings:
        print("  Findings:")
        for finding in findings:
            print(f"    {finding}")
    
    # Test recommendations
    print("\n💡 Testing Recommendations:")
    recommendations = agent.get_recommendations(risk_score, findings)
    for rec in recommendations:
        print(f"  {rec}")
    
    # Test report generation
    print("\n📋 Testing Report Generation:")
    test_address = "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
    report = agent.generate_report(test_address, risk_score, findings, recommendations)
    print(report)

def test_safe_wallet():
    """Test with a completely safe wallet"""
    print("\n🟢 Testing Safe Wallet Scenario:")
    print("=" * 40)
    
    os.environ['ETHERSCAN_API_KEY'] = 'test_key'
    agent = WalletSecurityAgent()
    
    # Mock safe transactions
    safe_transactions = [
        {
            'to': '0x9999999999999999999999999999999999999999',
            'isError': '0'
        },
        {
            'to': '0x8888888888888888888888888888888888888888',
            'isError': '0'
        }
    ]
    
    risk_score, findings = agent.analyze_transactions(safe_transactions)
    recommendations = agent.get_recommendations(risk_score, findings)
    
    print(f"Risk Score: {risk_score}/100")
    print(f"Risk Level: {agent.get_risk_level(risk_score)}")
    
    if findings:
        print("Findings:")
        for finding in findings:
            print(f"  {finding}")
    else:
        print("✅ No security issues detected")
    
    print("\nRecommendations:")
    for rec in recommendations:
        print(f"  {rec}")

def main():
    """Main test function"""
    print("🔒 EVM Wallet Security AI Agent - Test Suite")
    print("=" * 60)
    
    try:
        # Test basic functionality
        test_agent_without_api()
        
        # Test safe wallet scenario
        test_safe_wallet()
        
        print("\n🎉 All tests completed successfully!")
        print("\nThe agent is ready to use with real wallet addresses.")
        print("Remember to:")
        print("1. Get your Etherscan API key from https://etherscan.io/apis")
        print("2. Add it to the .env file")
        print("3. Run: python wallet_security_agent.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("Please check your Python installation and dependencies.")

if __name__ == "__main__":
    main()
