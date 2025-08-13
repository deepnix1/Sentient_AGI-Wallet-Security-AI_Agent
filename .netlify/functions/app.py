#!/usr/bin/env python3
"""
Main app function for serving the wallet scanner interface
"""
import os
import json
from pathlib import Path

def handler(event, context):
    """Netlify function handler for main app routes"""
    try:
        path = event.get('path', '/')
        
        # Get the project root
        project_root = Path(__file__).parent.parent.parent
        
        # Handle different routes
        if path == '/' or path == '/index.html':
            # Serve the main page
            index_path = project_root / 'templates' / 'index.html'
            if index_path.exists():
                with open(index_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'text/html'},
                    'body': content
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': {'Content-Type': 'text/plain'},
                    'body': 'Main page not found'
                }
        
        elif path.startswith('/dashboard/'):
            # For now, redirect to main page (dashboard functionality can be added later)
            return {
                'statusCode': 302,
                'headers': {'Location': '/'},
                'body': ''
            }
        
        else:
            # Default to serving index.html for SPA routing
            index_path = project_root / 'templates' / 'index.html'
            if index_path.exists():
                with open(index_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'text/html'},
                    'body': content
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': {'Content-Type': 'text/plain'},
                    'body': 'Page not found'
                }
                
    except Exception as e:
        print(f"Error in app handler: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': 'Internal server error'
        }
