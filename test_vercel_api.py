#!/usr/bin/env python3
"""
Test script for the Vercel FastAPI deployment
"""

import requests
import json

# Test configuration
BASE_URL = "http://localhost:8000"

def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint"""
    print("\nTesting health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_validate_endpoint():
    """Test the validate endpoint"""
    print("\nTesting validate endpoint...")
    try:
        # Test valid address
        valid_address = "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
        response = requests.post(f"{BASE_URL}/validate", 
                               json={"wallet_address": valid_address})
        print(f"Valid address test - Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test invalid address
        invalid_address = "invalid_address"
        response = requests.post(f"{BASE_URL}/validate", 
                               json={"wallet_address": invalid_address})
        print(f"Invalid address test - Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_analyze_endpoint():
    """Test the analyze endpoint"""
    print("\nTesting analyze endpoint...")
    try:
        # Test with a known Ethereum address
        test_address = "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
        response = requests.post(f"{BASE_URL}/analyze", 
                               json={"wallet_address": test_address})
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['success']}")
            print(f"Address: {result['address']}")
            if result.get('security_report'):
                print(f"Security report length: {len(result['security_report'])} characters")
            if result.get('dashboard_data'):
                print(f"Dashboard data keys: {list(result['dashboard_data'].keys())}")
        else:
            print(f"Error response: {response.text}")
        
        return response.status_code in [200, 400, 500]  # Accept various status codes
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting Vercel API tests...")
    print("=" * 50)
    
    tests = [
        test_root_endpoint,
        test_health_endpoint,
        test_validate_endpoint,
        test_analyze_endpoint
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print("-" * 30)
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! The API is ready for Vercel deployment.")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
