#!/usr/bin/env python3
"""
Sentient Wallet Security AI Agent - Transaction Visualizer
Provides interactive visualization of wallet transactions and security analysis
"""

import json
import plotly.graph_objects as go
import plotly.express as px
import plotly.utils
import networkx as nx
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Any
import re

class WalletVisualizer:
    def __init__(self):
        self.colors = {
            'safe': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'info': '#3b82f6',
            'dark': '#1f2937'
        }
    
    def create_transaction_timeline(self, transactions: List[Dict]) -> str:
        """Create interactive transaction timeline chart"""
        if not transactions:
            return "No transactions to visualize"
        
        # Prepare data for timeline
        timeline_data = []
        for tx in transactions:
            timestamp = int(tx.get('timeStamp', 0))
            date = datetime.fromtimestamp(timestamp)
            
            # Determine transaction type and color
            tx_type = "Incoming" if tx.get('from') != tx.get('to') else "Internal"
            color = self.colors['info'] if tx_type == "Incoming" else self.colors['warning']
            
            # Add risk indicators
            risk_level = "Low"
            if tx.get('isError') == '1':
                risk_level = "High"
                color = self.colors['danger']
            
            timeline_data.append({
                'date': date,
                'type': tx_type,
                'risk': risk_level,
                'hash': tx.get('hash', ''),
                'value': float(tx.get('value', 0)) / 1e18,  # Convert from wei to ETH
                'color': color
            })
        
        # Create timeline chart
        fig = go.Figure()
        
        # Add timeline markers
        for i, tx in enumerate(timeline_data):
            fig.add_trace(go.Scatter(
                x=[tx['date']],
                y=[i],
                mode='markers',
                marker=dict(
                    size=12,
                    color=tx['color'],
                    symbol='circle'
                ),
                text=f"Type: {tx['type']}<br>Risk: {tx['risk']}<br>Value: {tx['value']:.6f} ETH<br>Hash: {tx['hash'][:10]}...",
                hoverinfo='text',
                name=f"{tx['type']} - {tx['risk']} Risk"
            ))
        
        fig.update_layout(
            title="Transaction Timeline Analysis",
            xaxis_title="Date",
            yaxis_title="Transaction Index",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400,
            showlegend=True
        )
        
        return plotly.utils.PlotlyJSONEncoder().encode(fig)
    
    def create_network_graph(self, transactions: List[Dict]) -> str:
        """Create interactive network graph showing wallet connections"""
        if not transactions:
            return "No transactions to visualize"
        
        # Build network graph
        G = nx.DiGraph()
        node_colors = []
        node_sizes = []
        node_labels = {}
        
        # Add nodes and edges
        for tx in transactions:
            from_addr = tx.get('from', '')
            to_addr = tx.get('to', '')
            
            if from_addr and to_addr:
                # Add nodes
                if from_addr not in G:
                    G.add_node(from_addr)
                    node_colors.append(self.colors['info'])
                    node_sizes.append(20)
                    node_labels[from_addr] = from_addr[:8] + '...'
                
                if to_addr not in G:
                    G.add_node(to_addr)
                    node_colors.append(self.colors['warning'])
                    node_sizes.append(20)
                    node_labels[to_addr] = to_addr[:8] + '...'
                
                # Add edge
                G.add_edge(from_addr, to_addr)
        
        # Calculate layout
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Create network visualization
        edge_trace = go.Scatter(
            x=[], y=[], line=dict(width=0.5, color='#888'),
            hoverinfo='none', mode='lines')

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])

        node_trace = go.Scatter(
            x=[], y=[], text=[], mode='markers', hoverinfo='text',
            marker=dict(color=node_colors, size=node_sizes, line_width=2))

        for node in G.nodes():
            x, y = pos[node]
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
            node_trace['text'] += tuple([node_labels[node]])

        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title='Wallet Connection Network',
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           template="plotly_dark",
                           plot_bgcolor='rgba(0,0,0,0)',
                           paper_bgcolor='rgba(0,0,0,0)',
                           font=dict(color='white'),
                           height=500
                       ))
        
        return plotly.utils.PlotlyJSONEncoder().encode(fig)
    
    def create_risk_distribution(self, transactions: List[Dict]) -> str:
        """Create risk distribution pie chart"""
        if not transactions:
            return "No transactions to analyze"
        
        # Analyze risk distribution
        risk_counts = {'Low': 0, 'Medium': 0, 'High': 0}
        
        for tx in transactions:
            if tx.get('isError') == '1':
                risk_counts['High'] += 1
            elif float(tx.get('value', 0)) > 1e18:  # More than 1 ETH
                risk_counts['Medium'] += 1
            else:
                risk_counts['Low'] += 1
        
        # Create pie chart
        fig = px.pie(
            values=list(risk_counts.values()),
            names=list(risk_counts.keys()),
            color_discrete_map={
                'Low': self.colors['safe'],
                'Medium': self.colors['warning'],
                'High': self.colors['danger']
            }
        )
        
        fig.update_layout(
            title="Transaction Risk Distribution",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
        
        return plotly.utils.PlotlyJSONEncoder().encode(fig)
    
    def create_value_flow_chart(self, transactions: List[Dict]) -> str:
        """Create value flow chart showing incoming/outgoing amounts"""
        if not transactions:
            return "No transactions to analyze"
        
        # Prepare data
        dates = []
        incoming = []
        outgoing = []
        
        for tx in transactions:
            timestamp = int(tx.get('timeStamp', 0))
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            value = float(tx.get('value', 0)) / 1e18
            
            if date not in dates:
                dates.append(date)
                incoming.append(0)
                outgoing.append(0)
            
            idx = dates.index(date)
            if tx.get('from') != tx.get('to'):  # Not internal
                if value > 0:
                    incoming[idx] += value
                else:
                    outgoing[idx] += abs(value)
        
        # Create area chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=incoming,
            fill='tonexty',
            name='Incoming',
            line_color=self.colors['safe']
        ))
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=outgoing,
            fill='tonexty',
            name='Outgoing',
            line_color=self.colors['danger']
        ))
        
        fig.update_layout(
            title="Value Flow Over Time",
            xaxis_title="Date",
            yaxis_title="ETH Value",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400
        )
        
        return plotly.utils.PlotlyJSONEncoder().encode(fig)
    
    def create_interactive_dashboard(self, transactions: List[Dict], address: str) -> Dict[str, Any]:
        """Create complete interactive dashboard with all visualizations"""
        dashboard = {
            'address': address,
            'total_transactions': len(transactions),
            'charts': {}
        }
        
        try:
            # Generate all visualizations
            dashboard['charts']['timeline'] = self.create_transaction_timeline(transactions)
            dashboard['charts']['network'] = self.create_network_graph(transactions)
            dashboard['charts']['risk_distribution'] = self.create_risk_distribution(transactions)
            dashboard['charts']['value_flow'] = self.create_value_flow_chart(transactions)
            
            # Add transaction summary
            dashboard['summary'] = self.generate_transaction_summary(transactions)
            
        except Exception as e:
            dashboard['error'] = f"Visualization error: {str(e)}"
        
        return dashboard
    
    def generate_transaction_summary(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Generate comprehensive transaction summary"""
        if not transactions:
            return {}
        
        total_incoming = 0
        total_outgoing = 0
        failed_transactions = 0
        unique_addresses = set()
        
        for tx in transactions:
            value = float(tx.get('value', 0)) / 1e18
            from_addr = tx.get('from', '')
            to_addr = tx.get('to', '')
            
            if tx.get('isError') == '1':
                failed_transactions += 1
            
            if from_addr:
                unique_addresses.add(from_addr)
            if to_addr:
                unique_addresses.add(to_addr)
            
            # Determine if incoming or outgoing based on transaction direction
            if from_addr != to_addr:  # Not internal transfer
                if from_addr == '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6':  # Outgoing
                    total_outgoing += value
                else:  # Incoming
                    total_incoming += value
        
        return {
            'total_transactions': len(transactions),
            'total_incoming_eth': round(total_incoming, 6),
            'total_outgoing_eth': round(total_outgoing, 6),
            'net_flow_eth': round(total_incoming - total_outgoing, 6),
            'failed_transactions': failed_transactions,
            'success_rate': round(((len(transactions) - failed_transactions) / len(transactions)) * 100, 2),
            'unique_addresses': len(unique_addresses),
            'first_transaction': datetime.fromtimestamp(int(transactions[-1].get('timeStamp', 0))).strftime('%Y-%m-%d %H:%M:%S'),
            'last_transaction': datetime.fromtimestamp(int(transactions[0].get('timeStamp', 0))).strftime('%Y-%m-%d %H:%M:%S')
        }
