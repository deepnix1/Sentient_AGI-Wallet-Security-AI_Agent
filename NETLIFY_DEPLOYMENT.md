# Sentient Wallet Security AI Agent - Netlify Deployment Guide

This guide explains how to deploy the Sentient Wallet Security AI Agent to Netlify as a serverless application.

## 🚀 **Quick Start**

### **Prerequisites**
- Netlify account
- Git repository with the project
- Etherscan API key

### **1. Environment Variables**
Set up your environment variables in Netlify:
- Go to your Netlify site dashboard
- Navigate to **Site settings** > **Environment variables**
- Add: `ETHERSCAN_API_KEY` with your Etherscan API key

### **2. Deploy to Netlify**

#### **Option A: Deploy via Netlify UI (Recommended)**
1. Go to [netlify.com](https://netlify.com) and sign in
2. Click **"New site from Git"**
3. Choose your Git provider (GitHub, GitLab, etc.)
4. Select your repository: `deepnix1/Sentient_AGI-Wallet-Security-AI_Agent`
5. Set build settings:
   - **Build command**: `pip install -r .netlify/functions/requirements.txt`
   - **Publish directory**: `.`
6. Click **"Deploy site"**

#### **Option B: Deploy via Netlify CLI**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Initialize and deploy
netlify init
netlify deploy --prod
```

## 📁 **Project Structure for Netlify**

```
├── .netlify/
│   └── functions/
│       ├── app.py              # Netlify serverless function
│       └── requirements.txt    # Python dependencies for Netlify
├── app.py                      # Main Flask application
├── wallet_security_agent.py    # Core wallet analysis logic
├── wallet_visualizer.py        # Visualization and dashboard generation
├── templates/                  # HTML templates
├── static/                     # Static assets (CSS, JS, images)
├── netlify.toml               # Netlify configuration
└── requirements.txt            # Main project dependencies
```

## 🔧 **How It Works**

1. **Netlify Function**: `.netlify/functions/app.py` serves as the serverless entry point
2. **Flask Integration**: The function imports and serves your existing Flask app
3. **Static Files**: Templates and static assets are served directly by Netlify
4. **API Endpoints**: All your existing Flask routes work through the Netlify function

## 🌐 **Available Endpoints**

Your existing Flask routes are preserved:
- **GET** `/` - Main wallet scanner page
- **POST** `/scan` - Wallet scanning endpoint
- **GET** `/status/<address>` - Scan status
- **GET** `/dashboard/<address>` - Interactive dashboard
- **POST** `/api/validate-address` - Address validation

## 🧪 **Testing Locally**

### **1. Install Netlify CLI**
```bash
npm install -g netlify-cli
```

### **2. Test Netlify Function Locally**
```bash
# Start Netlify dev server
netlify dev

# Your site will be available at http://localhost:8888
```

### **3. Test Flask App Directly**
```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py

# Your site will be available at http://localhost:5000
```

## 🔒 **Environment Variables**

### **Required Variables**
- `ETHERSCAN_API_KEY` - Your Etherscan API key for blockchain data

### **Optional Variables**
- `FLASK_ENV` - Set to `production` for production deployment
- `DEBUG` - Set to `False` for production

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Build Failures**
   - Check that all dependencies are in `.netlify/functions/requirements.txt`
   - Ensure Python version compatibility (Netlify supports Python 3.7-3.10)

2. **Function Timeouts**
   - Netlify has a 10-second timeout limit
   - Consider optimizing API calls for large transaction histories

3. **Import Errors**
   - Verify that all Python modules are properly imported
   - Check that the function path is correct

4. **Environment Variables**
   - Ensure `ETHERSCAN_API_KEY` is set in Netlify dashboard
   - Variables are case-sensitive

### **Debug Mode**
For local debugging, the Flask app runs with detailed error messages. In production, errors are sanitized for security.

## 📈 **Performance Optimization**

- **Static Assets**: All CSS, JS, and images are served directly by Netlify CDN
- **Caching**: Netlify automatically caches static assets
- **Function Optimization**: Keep function execution time under 10 seconds

## 🔄 **Deployment Updates**

### **Automatic Deployments**
- Netlify automatically deploys when you push to your main branch
- Each commit triggers a new build and deployment

### **Manual Deployments**
```bash
# Deploy to production
netlify deploy --prod

# Deploy to preview
netlify deploy
```

## 📊 **Monitoring & Analytics**

- **Function Logs**: View in Netlify dashboard under **Functions** tab
- **Build Logs**: Available in **Deploys** section
- **Performance**: Monitor function execution times and errors

## 🌍 **Custom Domain**

1. Go to **Domain management** in your Netlify dashboard
2. Click **"Add custom domain"**
3. Follow the DNS configuration instructions
4. Netlify provides free SSL certificates automatically

## 📞 **Support**

For issues with:
- **Netlify Deployment**: Check Netlify documentation and community
- **Flask Application**: Review the function logs in Netlify dashboard
- **Etherscan API**: Verify your API key and rate limits

---

## 🎯 **Next Steps After Deployment**

1. **Test All Endpoints**: Verify that wallet scanning and dashboard work
2. **Set Environment Variables**: Ensure `ETHERSCAN_API_KEY` is configured
3. **Custom Domain**: Set up your preferred domain name
4. **Monitor Performance**: Check function execution times and errors
5. **Scale**: Netlify automatically scales based on traffic

---

**Built with ❤️ by @jackyjoeeth**
