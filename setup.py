#!/usr/bin/env python3
"""
Setup script for Sentient Wallet Security AI Agent
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        return True
    
    print("\n🔑 Creating .env file...")
    print("You'll need to add your Etherscan API key to the .env file")
    print("Get a free API key from: https://etherscan.io/apis")
    
    try:
        with open(env_file, 'w') as f:
            f.write("# Etherscan API Key\n")
            f.write("# Get your free API key from: https://etherscan.io/apis\n")
            f.write("ETHERSCAN_API_KEY=your_api_key_here\n")
        print("✅ .env file created")
        print("⚠️  IMPORTANT: Edit .env file and replace 'your_api_key_here' with your actual API key")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def main():
    """Main setup function"""
    print("🔒 Sentient Wallet Security AI Agent - Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your Etherscan API key")
    print("2. Run: python wallet_security_agent.py")
    print("3. Enter an EVM wallet address to scan")
    
    print("\nFor help, see README.md")

if __name__ == "__main__":
    main()
