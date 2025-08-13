#!/usr/bin/env python3
"""
Static file handler for Netlify
"""

import os
import json
from pathlib import Path

def handler(event, context):
    """Handle static file requests"""
    try:
        path = event.get('path', '/')
        
        # Default to index.html for root path
        if path == '/':
            path = '/index.html'
        
        # Remove leading slash
        file_path = path.lstrip('/')
        
        # Map paths to actual files
        if file_path == 'index.html':
            file_path = 'templates/index.html'
        elif file_path.startswith('static/'):
            file_path = file_path
        else:
            file_path = 'templates/index.html'  # Fallback to index
        
        # Get the full path
        project_root = Path(__file__).parent.parent.parent
        full_path = project_root / file_path
        
        # Check if file exists
        if not full_path.exists():
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'text/plain'},
                'body': 'File not found'
            }
        
        # Read file content
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Determine content type
        content_type = 'text/html'
        if file_path.endswith('.css'):
            content_type = 'text/css'
        elif file_path.endswith('.js'):
            content_type = 'application/javascript'
        elif file_path.endswith('.png'):
            content_type = 'image/png'
        elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
            content_type = 'image/jpeg'
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': content_type},
            'body': content
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }
