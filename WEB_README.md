# 🌐 Sentient Wallet Security AI Agent - Web Interface

## 🎨 Modern Dark Theme Web Application

A beautiful, responsive web interface for the EVM Wallet Security AI Agent with a sleek dark theme, smooth animations, and modern UI/UX design.

## ✨ Features

### 🎯 **Visual Design**
- **Dark Theme**: Elegant dark color scheme with blue/purple accents
- **Glassmorphism**: Modern glass-like UI elements with backdrop blur effects
- **Responsive**: Mobile-first design that works on all devices
- **Animations**: Smooth fade-in animations and hover effects
- **Particles**: Floating background particles for dynamic feel

### 🔧 **Functionality**
- **Real-time Scanning**: Live wallet security analysis
- **Address Validation**: Instant EVM address format checking
- **Progress Indicators**: Loading states and status updates
- **Error Handling**: User-friendly error messages
- **Responsive Results**: Beautifully formatted security reports

## 🚀 Quick Start

### 1. **Start the Web Interface**

**Windows:**
```bash
start_web.bat
```

**Mac/Linux:**
```bash
chmod +x start_web.sh
./start_web.sh
```

**Manual:**
```bash
python app.py
```

### 2. **Open Your Browser**
Navigate to: `http://localhost:5000`

### 3. **Start Scanning**
- Enter an EVM wallet address
- Click "Scan Wallet" or press Enter
- View real-time security analysis results

## 🎨 Design Features

### **Color Scheme**
- **Primary**: Deep space blues (#0f0f23, #1a1a2e, #16213e)
- **Accents**: Cyan (#00d4ff), Purple (#7c3aed), Orange (#f59e0b)
- **Text**: White (#ffffff), Light blue (#a8b2d1)
- **Cards**: Semi-transparent white with backdrop blur

### **UI Elements**
- **Glass Cards**: Translucent panels with blur effects
- **Gradient Buttons**: Beautiful gradient scan button
- **Floating Particles**: Animated background elements
- **Smooth Transitions**: CSS animations and hover effects

### **Responsive Design**
- **Mobile**: Stacked layout for small screens
- **Tablet**: Adaptive grid system
- **Desktop**: Full-width layout with optimal spacing

## 🔧 Technical Details

### **Frontend**
- **HTML5**: Semantic markup structure
- **CSS3**: Modern CSS with custom properties and animations
- **JavaScript**: ES6+ async/await for API calls
- **Font Awesome**: Beautiful icons throughout the interface

### **Backend**
- **Flask**: Lightweight Python web framework
- **Background Processing**: Async wallet scanning
- **REST API**: Clean API endpoints for frontend communication
- **Real-time Updates**: Polling-based result retrieval

### **API Endpoints**
- `POST /scan` - Start wallet scanning
- `GET /status/<address>` - Get scan status and results
- `POST /api/validate-address` - Validate address format

## 📱 Mobile Experience

The web interface is fully responsive and provides an excellent mobile experience:

- **Touch-friendly**: Large buttons and input fields
- **Optimized Layout**: Stacked design for small screens
- **Fast Loading**: Optimized for mobile networks
- **Native Feel**: Smooth scrolling and touch interactions

## 🎯 Usage Examples

### **Basic Scanning**
1. Enter wallet address: `0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6`
2. Click "Scan Wallet"
3. View security report with risk score and recommendations

### **Address Validation**
- Real-time validation as you type
- Clear error messages for invalid addresses
- Support for all EVM-compatible chains

## 🔒 Security Features

- **Input Validation**: Client and server-side address validation
- **Error Handling**: Secure error messages without information leakage
- **Background Processing**: Non-blocking wallet analysis
- **Rate Limiting**: Built-in protection against abuse

## 🚀 Performance

- **Fast Loading**: Optimized CSS and JavaScript
- **Efficient API**: Minimal network requests
- **Smooth Animations**: Hardware-accelerated CSS transitions
- **Responsive Design**: Instant feedback on all interactions

## 🎉 Ready to Use!

Your beautiful dark-themed web interface is ready! The design combines modern aesthetics with powerful functionality, providing users with an intuitive way to scan wallet addresses for security risks.

**Next Steps:**
1. Start the web server
2. Open in your browser
3. Start scanning wallets with style! 🚀
