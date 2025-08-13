# Sentient Wallet Security AI Agent - Vercel Deployment Guide

This guide explains how to deploy the Sentient Wallet Security AI Agent as a serverless Python application on Vercel.

## 🚀 Quick Start

### Prerequisites
- Vercel account
- Git repository with the project
- Etherscan API key

### 1. Environment Variables
Set up your environment variables in Vercel:
- Go to your Vercel project dashboard
- Navigate to Settings > Environment Variables
- Add: `ETHERSCAN_API_KEY` with your Etherscan API key

### 2. Deploy to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Follow the prompts to link to your Vercel account
```

## 📁 Project Structure

```
├── api/
│   └── index.py              # FastAPI application (Vercel entry point)
├── wallet_security_agent.py  # Core wallet analysis logic
├── wallet_visualizer.py      # Visualization and dashboard generation
├── requirements.txt          # Python dependencies
├── vercel.json              # Vercel configuration
└── .env                     # Local environment variables (not deployed)
```

## 🔧 API Endpoints

### Root Endpoint
- **GET** `/`
- Returns basic API information

### Health Check
- **GET** `/health`
- Returns API health status

### Wallet Analysis
- **POST** `/analyze`
- **Body**: `{"wallet_address": "0x..."}`
- Returns comprehensive security analysis and dashboard data

### Address Validation
- **POST** `/validate`
- **Body**: `{"wallet_address": "0x..."}`
- Returns address format validation

### Transaction History
- **GET** `/transactions/{address}`
- Returns transaction history for a wallet address

## 🧪 Testing Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file:
```
ETHERSCAN_API_KEY=your_etherscan_api_key_here
```

### 3. Run the API
```bash
cd api
python index.py
```

### 4. Test Endpoints
```bash
# Test the API
python test_vercel_api.py
```

Or use curl:
```bash
# Root endpoint
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health

# Analyze wallet
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"wallet_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"}'
```

## 🔒 Security Features

The API includes:
- Input validation for wallet addresses
- Error handling and graceful failures
- CORS middleware for cross-origin requests
- Rate limiting (handled by Vercel)

## 📊 Response Format

### Successful Analysis Response
```json
{
  "success": true,
  "address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
  "security_report": "Detailed security analysis...",
  "dashboard_data": {
    "summary": {
      "total_transactions": 150,
      "total_volume": "25.5 ETH",
      "unique_addresses": 45,
      "first_transaction": "2023-01-15"
    },
    "timeline": {...},
    "risk_distribution": {...},
    "value_flow": {...},
    "network": {...}
  }
}
```

### Error Response
```json
{
  "success": false,
  "address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
  "error": "Analysis failed: Invalid API key"
}
```

## 🛠️ Customization

### Adding New Endpoints
1. Add new route handlers in `api/index.py`
2. Update the root endpoint documentation
3. Test locally before deploying

### Modifying Analysis Logic
1. Update `wallet_security_agent.py` for core analysis
2. Update `wallet_visualizer.py` for visualization changes
3. The API will automatically use the updated logic

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are in `requirements.txt`
   - Check that module paths are correct

2. **API Key Issues**
   - Verify `ETHERSCAN_API_KEY` is set in Vercel environment variables
   - Test the API key locally first

3. **Timeout Issues**
   - Vercel has a 10-second timeout limit
   - Consider optimizing API calls for large transaction histories

4. **Memory Issues**
   - Vercel has memory limits for serverless functions
   - Consider limiting transaction history size for very active wallets

### Debug Mode
For local debugging, the API runs with detailed error messages. In production, errors are sanitized for security.

## 📈 Performance Optimization

- Transaction history is limited to prevent timeouts
- Dashboard data is generated efficiently
- API responses are optimized for size

## 🔄 Deployment Updates

To update the deployment:
```bash
# Make your changes
git add .
git commit -m "Update API functionality"

# Deploy to Vercel
vercel --prod
```

## 📞 Support

For issues with:
- **Vercel Deployment**: Check Vercel documentation
- **API Functionality**: Review the test script and logs
- **Etherscan API**: Verify your API key and rate limits

---

**Built with ❤️ by @jackyjoeeth**
