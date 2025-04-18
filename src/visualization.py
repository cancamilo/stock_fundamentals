"""
Visualization Module

This module provides functions for visualizing stock data and analysis results.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class StockVisualization:
    """Class for creating and displaying stock visualizations."""

    def __init__(self, stock_data):
        """
        Initialize with stock data.
        
        Args:
            stock_data (StockData): Instance of StockData class
        """
        self.stock_data = stock_data
        
        # Configure plotting
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_theme(style="darkgrid")
    
    def create_price_volume_chart(self):
        """
        Create an interactive price and volume chart.
        
        Returns:
            plotly.graph_objects.Figure: Interactive price and volume chart
        """
        if self.stock_data.hist_data_2y is None:
            print("Historical data not available. Fetch stock data first.")
            return None
        
        # Create the figure
        fig = make_subplots(
            rows=2, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.05, 
            subplot_titles=('Price', 'Volume'),
            row_heights=[0.7, 0.3]
        )
        
        # Add price candlestick
        fig.add_trace(
            go.Candlestick(
                x=self.stock_data.hist_data_2y.index,
                open=self.stock_data.hist_data_2y['Open'],
                high=self.stock_data.hist_data_2y['High'],
                low=self.stock_data.hist_data_2y['Low'],
                close=self.stock_data.hist_data_2y['Close'],
                name="Price"
            ),
            row=1, col=1
        )
        
        # Add moving averages
        hist_data_2y = self.stock_data.hist_data_2y.copy()
        hist_data_2y['MA50'] = hist_data_2y['Close'].rolling(window=50).mean()
        hist_data_2y['MA200'] = hist_data_2y['Close'].rolling(window=200).mean()
        
        fig.add_trace(
            go.Scatter(
                x=hist_data_2y.index,
                y=hist_data_2y['MA50'],
                name="50-Day MA",
                line=dict(color='orange', width=1)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=hist_data_2y.index,
                y=hist_data_2y['MA200'],
                name="200-Day MA",
                line=dict(color='purple', width=1)
            ),
            row=1, col=1
        )
        
        # Volume
        colors = ['red' if row['Open'] > row['Close'] else 'green' 
                for i, row in hist_data_2y.iterrows()]
        fig.add_trace(
            go.Bar(
                x=hist_data_2y.index,
                y=hist_data_2y['Volume'],
                name="Volume",
                marker_color=colors
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            title=f"{self.stock_data.symbol} Historical Price and Volume (2 Years)",
            xaxis_rangeslider_visible=False,
            height=800,
            width=1200,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    def create_technical_chart(self, tech_data):
        """
        Create an interactive technical analysis chart.
        
        Args:
            tech_data (pandas.DataFrame): DataFrame with technical indicators
            
        Returns:
            plotly.graph_objects.Figure: Interactive technical analysis chart
        """
        if tech_data is None:
            print("Technical indicator data not available.")
            return None
        
        # Create the figure
        fig = make_subplots(
            rows=3, cols=1, 
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('Price with Bollinger Bands', 'RSI', 'MACD'),
            row_heights=[0.5, 0.25, 0.25]
        )
        
        # Price with Bollinger Bands
        fig.add_trace(
            go.Scatter(
                x=tech_data.index,
                y=tech_data['Close'],
                name="Close Price",
                line=dict(color='blue')
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=tech_data.index,
                y=tech_data['BB_Upper'],
                name="BB Upper",
                line=dict(color='gray', width=1)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=tech_data.index,
                y=tech_data['BB_Middle'],
                name="BB Middle",
                line=dict(color='gray', width=1, dash='dash')
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=tech_data.index,
                y=tech_data['BB_Lower'],
                name="BB Lower",
                line=dict(color='gray', width=1)
            ),
            row=1, col=1
        )
        
        # RSI
        fig.add_trace(
            go.Scatter(
                x=tech_data.index,
                y=tech_data['RSI'],
                name="RSI",
                line=dict(color='purple')
            ),
            row=2, col=1
        )
        
        # Add RSI overbought/oversold lines
        fig.add_trace(
            go.Scatter(
                x=tech_data.index,
                y=[70] * len(tech_data),
                name="Overbought",
                line=dict(color='red', width=1, dash='dash')
            ),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=tech_data.index,
                y=[30] * len(tech_data),
                name="Oversold",
                line=dict(color='green', width=1, dash='dash')
            ),
            row=2, col=1
        )
        
        # MACD
        fig.add_trace(
            go.Scatter(
                x=tech_data.index,
                y=tech_data['MACD'],
                name="MACD",
                line=dict(color='blue')
            ),
            row=3, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=tech_data.index,
                y=tech_data['MACD_Signal'],
                name="Signal Line",
                line=dict(color='red')
            ),
            row=3, col=1
        )
        
        # MACD Histogram
        colors = ['green' if val >= 0 else 'red' for val in tech_data['MACD_Histogram']]
        fig.add_trace(
            go.Bar(
                x=tech_data.index,
                y=tech_data['MACD_Histogram'],
                name="MACD Histogram",
                marker_color=colors
            ),
            row=3, col=1
        )
        
        # Update layout
        fig.update_layout(
            title=f"{self.stock_data.symbol} Technical Indicators (1 Year)",
            height=900,
            width=1200,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # Add y-axis titles
        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="RSI", row=2, col=1)
        fig.update_yaxes(title_text="MACD", row=3, col=1)
        
        return fig
    
    @staticmethod
    def safe_plot_display(figure):
        """
        Safely display a plotly figure, with fallback to a static image if nbformat is missing.
        
        Args:
            figure (plotly.graph_objects.Figure): Plotly figure to display
        """
        try:
            # Try to display the interactive plot
            figure.show()
        except ValueError as e:
            if "nbformat" in str(e):
                # If nbformat is missing or outdated, switch to a non-interactive display
                print("Warning: Interactive plot could not be displayed due to missing or outdated nbformat.")
                print("Displaying static plot instead. Run `!pip install nbformat>=4.2.0` and restart kernel for interactive plots.")
                # Generate a static image
                img_bytes = figure.to_image(format="png")
                from IPython.display import Image, display
                display(Image(img_bytes))
            else:
                # If it's another error, re-raise it
                raise