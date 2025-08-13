#!/usr/bin/env python3
"""
Test script for Netlify function locally
"""

import json
import sys
from pathlib import Path

# Add the netlify functions directory to path
sys.path.append(str(Path(__file__).parent / '.netlify' / 'functions'))

from api import handler

def test_netlify_function():
    """Test the Netlify function locally"""
    print("Testing Netlify function locally...")
    print("=" * 50)
    
    # Test root endpoint
    print("\n1. Testing root endpoint...")
    event = {
        'httpMethod': 'GET',
        'path': '/',
        'body': None
    }
    response = handler(event, None)
    print(f"Status: {response['statusCode']}")
    print(f"Response: {response['body']}")
    
    # Test health endpoint
    print("\n2. Testing health endpoint...")
    event = {
        'httpMethod': 'GET',
        'path': '/api/health',
        'body': None
    }
    response = handler(event, None)
    print(f"Status: {response['statusCode']}")
    print(f"Response: {response['body']}")
    
    # Test validate endpoint
    print("\n3. Testing validate endpoint...")
    event = {
        'httpMethod': 'POST',
        'path': '/api/validate',
        'body': json.dumps({
            'wallet_address': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6'
        })
    }
    response = handler(event, None)
    print(f"Status: {response['statusCode']}")
    print(f"Response: {response['body']}")
    
    # Test analyze endpoint
    print("\n4. Testing analyze endpoint...")
    event = {
        'httpMethod': 'POST',
        'path': '/api/analyze',
        'body': json.dumps({
            'wallet_address': '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6'
        })
    }
    response = handler(event, None)
    print(f"Status: {response['statusCode']}")
    print(f"Response: {response['body'][:200]}...")  # Truncate long responses
    
    print("\n✅ Netlify function test completed!")

if __name__ == "__main__":
    test_netlify_function()
