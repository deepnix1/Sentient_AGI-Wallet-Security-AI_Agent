#!/usr/bin/env python3
"""
Sentient Wallet Security AI Agent - Netlify Function
Serverless function to serve the Flask application
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import Flask app
from app import app

# Create a handler for Netlify
def handler(event, context):
    """Netlify function handler"""
    # Import Flask test client for handling requests
    with app.test_client() as client:
        # Parse the event
        path = event.get('path', '/')
        method = event.get('httpMethod', 'GET')
        headers = event.get('headers', {})
        body = event.get('body', '')
        
        # Convert Netlify event to Flask request
        if method == 'POST':
            response = client.post(path, data=body, headers=headers)
        elif method == 'PUT':
            response = client.put(path, data=body, headers=headers)
        elif method == 'DELETE':
            response = client.delete(path, headers=headers)
        else:
            response = client.get(path, headers=headers)
        
        # Return Netlify-compatible response
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data(as_text=True)
        }

# For local testing
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
