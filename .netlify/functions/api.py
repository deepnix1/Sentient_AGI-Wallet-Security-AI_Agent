#!/usr/bin/env python3
"""
Sentient Wallet Security AI Agent - Netlify Serverless Function
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent.parent))

from wallet_security_agent import WalletSecurityAgent
import json

# Initialize agent
try:
    wallet_agent = WalletSecurityAgent()
except Exception as e:
    print(f"Warning: Could not initialize agent: {e}")
    wallet_agent = None

def generate_basic_stats(transactions):
    """Generate basic transaction statistics"""
    if not transactions:
        return {}
    
    total_transactions = len(transactions)
    total_volume = 0
    unique_addresses = set()
    
    for tx in transactions:
        # Convert from wei to ETH
        value = float(tx.get('value', 0)) / 1e18
        total_volume += value
        
        # Collect unique addresses
        if tx.get('from'):
            unique_addresses.add(tx.get('from'))
        if tx.get('to'):
            unique_addresses.add(tx.get('to'))
    
    return {
        "total_transactions": total_transactions,
        "total_volume": f"{total_volume:.6f} ETH",
        "unique_addresses": len(unique_addresses),
        "average_transaction_value": f"{total_volume / total_transactions:.6f} ETH" if total_transactions > 0 else "0 ETH"
    }

def handler(event, context):
    """Netlify serverless function handler"""
    try:
        # Parse the request
        method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        
        # Handle CORS
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Content-Type': 'application/json'
        }
        
        # Handle preflight OPTIONS request
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # Route the request
        if path == '/' or path == '/api':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'message': 'Wallet Security AI Agent is running',
                    'version': 'netlify'
                })
            }
        
        elif path == '/api/health':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'status': 'healthy',
                    'agent_initialized': wallet_agent is not None,
                    'version': 'netlify'
                })
            }
        
        elif path == '/api/validate' and method == 'POST':
            try:
                body = json.loads(event.get('body', '{}'))
                wallet_address = body.get('wallet_address', '')
                
                if not wallet_agent:
                    wallet_agent = WalletSecurityAgent()
                
                is_valid = wallet_agent.validate_address(wallet_address)
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'address': wallet_address,
                        'valid': is_valid
                    })
                }
            except Exception as e:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({
                        'error': f'Validation failed: {str(e)}'
                    })
                }
        
        elif path == '/api/analyze' and method == 'POST':
            try:
                body = json.loads(event.get('body', '{}'))
                wallet_address = body.get('wallet_address', '')
                
                if not wallet_agent:
                    wallet_agent = WalletSecurityAgent()
                
                # Validate address
                if not wallet_agent.validate_address(wallet_address):
                    return {
                        'statusCode': 400,
                        'headers': headers,
                        'body': json.dumps({
                            'success': False,
                            'address': wallet_address,
                            'error': 'Invalid wallet address format'
                        })
                    }
                
                # Get transactions and analyze
                transactions = wallet_agent.get_transactions(wallet_address)
                security_report = wallet_agent.scan_wallet(wallet_address)
                basic_stats = generate_basic_stats(transactions)
                
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'success': True,
                        'address': wallet_address,
                        'security_report': security_report,
                        'basic_stats': basic_stats
                    })
                }
            except Exception as e:
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({
                        'success': False,
                        'address': body.get('wallet_address', ''),
                        'error': f'Analysis failed: {str(e)}'
                    })
                }
        
        elif path.startswith('/api/transactions/') and method == 'GET':
            try:
                # Extract address from path
                address = path.split('/')[-1]
                
                if not wallet_agent:
                    wallet_agent = WalletSecurityAgent()
                
                if not wallet_agent.validate_address(address):
                    return {
                        'statusCode': 400,
                        'headers': headers,
                        'body': json.dumps({
                            'error': 'Invalid wallet address format'
                        })
                    }
                
                transactions = wallet_agent.get_transactions(address)
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'address': address,
                        'transaction_count': len(transactions),
                        'transactions': transactions[:10]  # Limit to first 10
                    })
                }
            except Exception as e:
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({
                        'error': f'Failed to fetch transactions: {str(e)}'
                    })
                }
        
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({
                    'error': 'Endpoint not found'
                })
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'Internal server error: {str(e)}'
            })
        }
