#!/usr/bin/env python3
"""
Sentient Wallet Security AI Agent - Vercel Deployment
FastAPI serverless application for wallet security analysis
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import json

# Import our existing modules
from wallet_security_agent import WalletSecurityAgent
from wallet_visualizer import WalletVisualizer

# Initialize FastAPI app
app = FastAPI(
    title="Sentient Wallet Security AI Agent",
    description="AI-powered wallet security analysis and visualization",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class WalletAnalysisRequest(BaseModel):
    wallet_address: str

class WalletAnalysisResponse(BaseModel):
    success: bool
    address: str
    security_report: Optional[str] = None
    dashboard_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Initialize agents
try:
    wallet_agent = WalletSecurityAgent()
    visualizer = WalletVisualizer()
except Exception as e:
    print(f"Warning: Could not initialize agents: {e}")
    wallet_agent = None
    visualizer = None

@app.get("/")
async def root():
    """Root endpoint"""
    # Requirement: return exactly this message
    return {"message": "Wallet Security AI Agent is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents_initialized": wallet_agent is not None and visualizer is not None
    }

@app.post("/analyze", response_model=WalletAnalysisResponse)
async def analyze_wallet(request: WalletAnalysisRequest):
    """Analyze a wallet address for security risks"""
    try:
        # Lazy init if global init failed (e.g., missing env during import)
        global wallet_agent, visualizer
        if wallet_agent is None:
            try:
                wallet_agent = WalletSecurityAgent()
            except Exception as init_err:
                return WalletAnalysisResponse(
                    success=False,
                    address=request.wallet_address,
                    error=f"Agent initialization failed: {str(init_err)}"
                )
        if visualizer is None:
            try:
                visualizer = WalletVisualizer()
            except Exception as init_err:
                return WalletAnalysisResponse(
                    success=False,
                    address=request.wallet_address,
                    error=f"Visualizer initialization failed: {str(init_err)}"
                )
        # Validate the wallet address
        if not wallet_agent.validate_address(request.wallet_address):
            raise HTTPException(
                status_code=400, 
                detail="Invalid wallet address format. Must be a valid EVM address (0x...)"
            )
        
        # Get transaction history
        transactions = wallet_agent.get_transactions(request.wallet_address)
        
        if not transactions:
            return WalletAnalysisResponse(
                success=True,
                address=request.wallet_address,
                security_report="No transactions found for this wallet address.",
                dashboard_data={
                    "summary": {
                        "total_transactions": 0,
                        "total_volume": "0 ETH",
                        "unique_addresses": 0,
                        "first_transaction": "N/A"
                    },
                    "timeline": {"dates": [], "counts": []},
                    "risk_distribution": {"values": [100], "labels": ["No Data"]},
                    "value_flow": {"periods": [], "values": []},
                    "network": {"x": [0], "y": [0], "labels": ["No Data"], "sizes": [20]}
                }
            )
        
        # Generate security report
        security_report = wallet_agent.scan_wallet(request.wallet_address)
        
        # Generate dashboard data
        dashboard_data = visualizer.create_interactive_dashboard(transactions, request.wallet_address)
        
        return WalletAnalysisResponse(
            success=True,
            address=request.wallet_address,
            security_report=security_report,
            dashboard_data=dashboard_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return WalletAnalysisResponse(
            success=False,
            address=request.wallet_address,
            error=f"Analysis failed: {str(e)}"
        )

@app.post("/validate")
async def validate_address(request: WalletAnalysisRequest):
    """Validate wallet address format"""
    try:
        global wallet_agent
        if wallet_agent is None:
            wallet_agent = WalletSecurityAgent()
        is_valid = wallet_agent.validate_address(request.wallet_address)
        return {
            "address": request.wallet_address,
            "valid": is_valid
        }
    except Exception as e:
        return {
            "address": request.wallet_address,
            "valid": False,
            "error": str(e)
        }

@app.get("/transactions/{address}")
async def get_transactions(address: str):
    """Get transaction history for a wallet address"""
    try:
        global wallet_agent
        if wallet_agent is None:
            wallet_agent = WalletSecurityAgent()
        if not wallet_agent.validate_address(address):
            raise HTTPException(
                status_code=400, 
                detail="Invalid wallet address format"
            )
        
        transactions = wallet_agent.get_transactions(address)
        return {
            "address": address,
            "transaction_count": len(transactions),
            "transactions": transactions[:10]  # Limit to first 10 for API response
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch transactions: {str(e)}")

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
