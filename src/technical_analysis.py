"""
Technical Analysis Module

This module provides functions for calculating technical indicators for stock analysis.
"""

import pandas as pd
import numpy as np


class TechnicalAnalysis:
    """Class for calculating and analyzing technical indicators."""

    def __init__(self, stock_data):
        """
        Initialize with stock data.
        
        Args:
            stock_data (StockData): Instance of StockData class
        """
        self.stock_data = stock_data
    
    def calculate_technical_indicators(self, data=None):
        """
        Calculate technical indicators for the stock.
        
        Args:
            data (pandas.DataFrame, optional): Historical price data. 
                                             If None, uses stock_data.hist_data_1y.
        
        Returns:
            pandas.DataFrame: DataFrame with technical indicators
        """
        if data is None:
            if self.stock_data.hist_data_1y is None:
                print("Historical data not available. Fetch stock data first.")
                return None
            data = self.stock_data.hist_data_1y
        
        # Make a copy to avoid modifying the original dataframe
        df = data.copy()
        
        # Moving Averages
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA50'] = df['Close'].rolling(window=50).mean()
        df['MA200'] = df['Close'].rolling(window=200).mean()
        
        # Exponential Moving Averages
        df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
        
        # MACD
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        
        # Relative Strength Index (RSI)
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        df['BB_Std'] = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (df['BB_Std'] * 2)
        df['BB_Lower'] = df['BB_Middle'] - (df['BB_Std'] * 2)
        
        # Average True Range (ATR)
        df['TR1'] = abs(df['High'] - df['Low'])
        df['TR2'] = abs(df['High'] - df['Close'].shift())
        df['TR3'] = abs(df['Low'] - df['Close'].shift())
        df['TR'] = df[['TR1', 'TR2', 'TR3']].max(axis=1)
        df['ATR'] = df['TR'].rolling(window=14).mean()
        
        return df
    
    def get_recent_indicators(self, tech_data=None):
        """
        Get the most recent technical indicator values.
        
        Args:
            tech_data (pandas.DataFrame, optional): DataFrame with technical indicators.
                                                  If None, calculates them.
                                                  
        Returns:
            dict: Dictionary with most recent technical indicator values
        """
        if tech_data is None:
            tech_data = self.calculate_technical_indicators()
            if tech_data is None:
                return {}
        
        if tech_data.empty:
            return {}
        
        recent_date = tech_data.index[-1]
        indicators = {}
        
        for col in ['Close', 'RSI', 'MACD', 'MACD_Signal', 'MACD_Histogram', 
                  'ATR', 'BB_Upper', 'BB_Middle', 'BB_Lower']:
            if col in tech_data.columns:
                indicators[col] = tech_data.loc[recent_date, col]
        
        return indicators