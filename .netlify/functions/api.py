#!/usr/bin/env python3
"""
API handler for wallet scanning functionality
"""
import sys
import os
import json
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the wallet security agent
agent_available = False
try:
    from wallet_security_agent import WalletSecurityAgent
    from wallet_visualizer import WalletVisualizer
    agent_available = True
    print("Successfully imported wallet security agent and visualizer")
except Exception as e:
    print(f"Warning: Could not import wallet security agent: {e}")
    import traceback
    traceback.print_exc()
    agent_available = False

# Global storage for scan results (in production, use a proper database)
scan_results = {}
scan_status = {}

def handler(event, context):
    """Handle API requests"""
    try:
        path = event.get('path', '')
        method = event.get('httpMethod', 'GET')
        
        # Handle CORS
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        
        # Handle preflight requests
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # Parse body for POST requests and query parameters for GET requests
        body = {}
        if method == 'POST' and event.get('body'):
            try:
                body = json.loads(event.get('body', '{}'))
            except:
                body = {}
        elif method == 'GET' and event.get('queryStringParameters'):
            body = event.get('queryStringParameters', {})
        
        # Route requests based on path
        if path.endswith('/scan') and method == 'POST':
            return handle_scan(body, headers)
        elif path.endswith('/status') and method == 'GET':
            return handle_status(body, headers)
        elif path.endswith('/health') and method == 'GET':
            return handle_health(headers)
        elif path.endswith('/test') and method == 'GET':
            return handle_test(headers)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Endpoint not found', 'path': path})
            }
            
    except Exception as e:
        print(f"Error in API handler: {e}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }

def handle_health(headers):
    """Health check endpoint"""
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'status': 'healthy',
            'message': 'Sentient Wallet Security AI Agent is running',
            'agent_available': agent_available
        })
    }

def handle_test(headers):
    """Test endpoint to verify API is working"""
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'message': 'API is working',
            'agent_available': agent_available,
            'timestamp': time.time()
        })
    }

def handle_scan(body, headers):
    """Handle wallet scanning requests"""
    try:
        if not agent_available:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({'error': 'Wallet security agent not available'})
            }
        
        address = body.get('address', '')
        
        if not address:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Address is required'})
            }
        
        # Check if already scanning
        if address in scan_status and scan_status[address] == "scanning":
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Wallet already being scanned'})
            }
        
        # Start background scan
        scan_status[address] = "scanning"
        scan_results[address] = ""
        
        # For now, do a simple scan (in production, use background processing)
        try:
            agent = WalletSecurityAgent()
            visualizer = WalletVisualizer()
            
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
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Scan started',
                'address': address
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': f'Scan failed: {str(e)}'})
        }

def handle_status(body, headers):
    """Handle status check requests"""
    try:
        # Extract address from query parameters or body
        address = body.get('address', '')
        
        if not address:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Address is required'})
            }
        
        if address not in scan_status:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'status': 'not_found'})
            }
        
        status = scan_status[address]
        result = scan_results.get(address, "")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': status,
                'result': result
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': f'Status check failed: {str(e)}'})
        }
