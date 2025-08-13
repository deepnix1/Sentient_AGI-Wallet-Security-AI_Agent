# Sentient Wallet Security AI Agent - Deployment Guide

## Platform-Specific Start Commands

### 1. **Render** 
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app`
- **Build Command**: `pip install -r requirements.txt`
- **Environment Variables**: 
  - `ETHERSCAN_API_KEY` (required)
  - `PORT` (auto-set by Render)

### 2. **Heroku**
- **Start Command**: Uses `Procfile` automatically
- **Build Command**: `pip install -r requirements.txt`
- **Environment Variables**: 
  - `ETHERSCAN_API_KEY` (required)

### 3. **Railway**
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app`
- **Build Command**: `pip install -r requirements.txt`

### 4. **DigitalOcean App Platform**
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app`
- **Build Command**: `pip install -r requirements.txt`

### 5. **Vercel** (Alternative)
- **Start Command**: `python app.py` (for development)
- **Note**: Vercel works better with serverless functions

### 6. **Netlify** (Current)
- **Start Command**: Uses serverless functions in `.netlify/functions/`
- **Build Command**: `pip install -r .netlify/functions/requirements.txt`

## Environment Variables Required

```bash
ETHERSCAN_API_KEY=your_etherscan_api_key_here
```

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Or with gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 1 app:app
```

## Production Considerations

1. **Security**: Always use environment variables for API keys
2. **Performance**: Use Gunicorn with appropriate worker count
3. **Timeout**: Set timeout to 120 seconds for wallet scanning
4. **CORS**: Already configured for cross-origin requests
5. **Static Files**: Serve from `/static/` directory

## Troubleshooting

### Common Issues:
1. **Port Issues**: Make sure to use `$PORT` environment variable
2. **Import Errors**: All dependencies are in `requirements.txt`
3. **API Key**: Ensure `ETHERSCAN_API_KEY` is set
4. **CORS**: Frontend should work with any of these deployments

### Testing Deployment:
```bash
# Test the API endpoints
curl -X GET "https://your-app-url.com/health"
curl -X POST "https://your-app-url.com/scan" -H "Content-Type: application/json" -d '{"address":"0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"}'
```

## Recommended Platform

For this Flask application, **Render** or **Railway** are recommended as they:
- Support Python applications well
- Have good free tiers
- Handle environment variables properly
- Support the required dependencies
