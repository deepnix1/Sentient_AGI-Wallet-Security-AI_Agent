#!/usr/bin/env python3
"""
Sentient Wallet Security AI Agent - Web Interface
Flask web application with modern dark theme
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from wallet_security_agent import WalletSecurityAgent
from wallet_visualizer import WalletVisualizer
import threading
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variable to store scan results
scan_results = {}
scan_status = {}

def scan_wallet_background(address):
    """Background wallet scanning function"""
    try:
        agent = WalletSecurityAgent()
        visualizer = WalletVisualizer()
        scan_status[address] = "scanning"
        
        # Simulate some processing time for better UX
        time.sleep(1)
        
        # Get the scan result
        result = agent.scan_wallet(address)
        
        # Get transaction data for visualization
        transactions = agent.get_transactions(address)
        
        # Create interactive dashboard
        dashboard = visualizer.create_interactive_dashboard(transactions, address)
        
        # Store both results
        scan_results[address] = {
            'security_report': result,
            'dashboard': dashboard
        }
        scan_status[address] = "completed"
        
    except Exception as e:
        scan_results[address] = f"Error: {str(e)}"
        scan_status[address] = "error"

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Sentient Wallet Security AI Agent'})

@app.route('/scan', methods=['POST'])
def scan_wallet():
    """API endpoint to scan a wallet"""
    data = request.get_json()
    address = data.get('address', '').strip()
    
    if not address:
        return jsonify({'error': 'Address is required'}), 400
    
    # Check if already scanning
    if address in scan_status and scan_status[address] == "scanning":
        return jsonify({'error': 'Wallet already being scanned'}), 400
    
    # Start background scan
    scan_status[address] = "scanning"
    scan_results[address] = ""
    
    thread = threading.Thread(target=scan_wallet_background, args=(address,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Scan started', 'address': address})

@app.route('/api/scan', methods=['POST'])
def api_scan_wallet():
    """API endpoint to scan a wallet (for production)"""
    return scan_wallet()

@app.route('/status/<address>')
def get_status(address):
    """Get scan status for an address"""
    if address not in scan_status:
        return jsonify({'status': 'not_found'})
    
    status = scan_status[address]
    result = scan_results.get(address, "")
    
    return jsonify({
        'status': status,
        'result': result
    })

@app.route('/api/status')
def api_get_status():
    """Get scan status for an address (for production)"""
    address = request.args.get('address')
    if not address:
        return jsonify({'error': 'Address parameter is required'}), 400
    
    if address not in scan_status:
        return jsonify({'status': 'not_found'})
    
    status = scan_status[address]
    result = scan_results.get(address, "")
    
    return jsonify({
        'status': status,
        'result': result
    })

@app.route('/api/validate-address', methods=['POST'])
def validate_address():
    """Validate EVM address format"""
    data = request.get_json()
    address = data.get('address', '').strip()
    
    try:
        agent = WalletSecurityAgent()
        is_valid = agent.validate_address(address)
        return jsonify({'valid': is_valid})
    except:
        return jsonify({'valid': False})

@app.route('/dashboard/<address>')
def dashboard(address):
    """Interactive dashboard page"""
    return render_template('dashboard.html', address=address)

@app.route('/api/dashboard/<address>')
def get_dashboard_data(address):
    """Get dashboard data for an address"""
    try:
        # Check if we have scan results for this address
        if address not in scan_results or scan_status.get(address) != "completed":
            return jsonify({'error': 'No scan data available for this address'}), 404
        
        result = scan_results[address]
        
        # If it's a string (error), return error
        if isinstance(result, str):
            return jsonify({'error': result}), 500
        
        # Return the dashboard data
        return jsonify(result.get('dashboard', {}))
        
    except Exception as e:
        return jsonify({'error': f'Failed to get dashboard data: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
