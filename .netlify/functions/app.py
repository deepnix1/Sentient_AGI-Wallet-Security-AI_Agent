#!/usr/bin/env python3
"""
Sentient Wallet Security AI Agent - Netlify Function
Serverless function to serve the Flask application
"""
import sys
import os
import json
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Try to import Flask app with error handling
try:
    from app import app
    flask_app_available = True
except Exception as e:
    print(f"Warning: Could not import Flask app: {e}")
    flask_app_available = False

def handler(event, context):
    """Netlify function handler"""
    try:
        # Check if Flask app is available
        if not flask_app_available:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'Flask application not available',
                    'message': 'Please check the deployment configuration'
                })
            }
        
        # Import Flask test client for handling requests
        with app.test_client() as client:
            # Parse the event
            path = event.get('path', '/')
            method = event.get('httpMethod', 'GET')
            headers = event.get('headers', {})
            body = event.get('body', '')
            
            # Handle static files
            if path.startswith('/static/'):
                # Serve static files directly
                static_path = path.lstrip('/')
                full_path = project_root / static_path
                
                if full_path.exists():
                    with open(full_path, 'rb') as f:
                        content = f.read()
                    
                    # Determine content type
                    content_type = 'text/plain'
                    if static_path.endswith('.css'):
                        content_type = 'text/css'
                    elif static_path.endswith('.js'):
                        content_type = 'application/javascript'
                    elif static_path.endswith('.png'):
                        content_type = 'image/png'
                    elif static_path.endswith('.jpg') or static_path.endswith('.jpeg'):
                        content_type = 'image/jpeg'
                    
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': content_type},
                        'body': content.decode('utf-8') if content_type.startswith('text/') else content
                    }
            
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
            
    except Exception as e:
        print(f"Error in handler: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }

# For local testing
if __name__ == "__main__":
    if flask_app_available:
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Flask app not available for local testing")
