# 🚀 **Netlify Deployment Guide for Sentient Wallet Security AI Agent**

## 📋 **Prerequisites**

- GitHub repository with your code
- Netlify account (free at [netlify.com](https://netlify.com))
- Etherscan API key (for wallet analysis functionality)

## 🎯 **Deployment Steps**

### **Step 1: Push to GitHub**
```bash
git add .
git commit -m "Add Netlify deployment configuration"
git push origin main
```

### **Step 2: Deploy to Netlify**

#### **Option A: Netlify Dashboard (Recommended)**
1. Go to [netlify.com](https://netlify.com) and sign in
2. Click **"New site from Git"**
3. Choose **GitHub** as your Git provider
4. Select your repository: `deepnix1/Sentient_AGI-Wallet-Security-AI_Agent`
5. Configure build settings:
   - **Build command**: `pip install -r .netlify/functions/requirements.txt`
   - **Publish directory**: `.`
   - **Python version**: `3.10`
6. Click **"Deploy site"**

#### **Option B: Netlify CLI**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy
netlify deploy --prod
```

### **Step 3: Configure Environment Variables**
1. In your Netlify dashboard, go to **Site settings** → **Environment variables**
2. Add your Etherscan API key:
   - **Key**: `ETHERSCAN_API_KEY`
   - **Value**: Your actual API key from Etherscan

### **Step 4: Test Your Deployment**
Your site will be available at: `https://your-site-name.netlify.app`

## 🔧 **API Endpoints**

Once deployed, your API will be available at:

- **Root**: `https://your-site.netlify.app/`
- **Health Check**: `https://your-site.netlify.app/api/health`
- **Validate Address**: `https://your-site.netlify.app/api/validate`
- **Analyze Wallet**: `https://your-site.netlify.app/api/analyze`
- **Get Transactions**: `https://your-site.netlify.app/api/transactions/{address}`

## 📱 **Test Your API**

### **Health Check**
```bash
curl https://your-site.netlify.app/api/health
```

### **Validate Wallet Address**
```bash
curl -X POST https://your-site.netlify.app/api/validate \
  -H "Content-Type: application/json" \
  -d '{"wallet_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"}'
```

### **Analyze Wallet**
```bash
curl -X POST https://your-site.netlify.app/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"wallet_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"}'
```

## 🎨 **Customization**

### **Update Logo**
Replace `static/images/sentient-logo.png` with your preferred logo

### **Modify Styling**
Edit the CSS in `index.html` to match your brand colors

### **Add More Endpoints**
Extend the `handler` function in `.netlify/functions/api.py`

## 🚨 **Troubleshooting**

### **Build Failures**
- Check that Python 3.10 is specified in `netlify.toml`
- Ensure all dependencies are in `.netlify/functions/requirements.txt`
- Verify file paths are correct

### **API Errors**
- Check environment variables are set correctly
- Verify Etherscan API key is valid
- Check Netlify function logs in the dashboard

### **CORS Issues**
- CORS headers are already configured in the function
- If issues persist, check browser console for errors

## 📊 **Monitoring**

- **Function Logs**: Available in Netlify dashboard under **Functions**
- **Site Analytics**: Built-in analytics in Netlify dashboard
- **Performance**: Automatic performance monitoring

## 🔄 **Updates**

To update your deployment:
1. Make changes to your code
2. Commit and push to GitHub
3. Netlify will automatically redeploy

## 💡 **Pro Tips**

- **Custom Domain**: Add your own domain in Netlify settings
- **Branch Deploys**: Deploy previews for pull requests
- **Form Handling**: Use Netlify Forms for contact forms
- **Redirects**: Configure custom redirects in `netlify.toml`

## 🎉 **Success!**

Your Sentient Wallet Security AI Agent is now running in the cloud on Netlify!

**Built with ❤️ by @jackyjoeeth**
