"""
Stock Data Retrieval Module

This module provides functions to fetch and organize stock market data.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class StockData:
    """Class for fetching and organizing stock data."""

    def __init__(self, symbol):
        """
        Initialize with a stock symbol.
        
        Args:
            symbol (str): Stock ticker symbol (e.g., 'AAPL')
        """
        self.symbol = symbol
        self.stock = None
        self.hist_data_2y = None
        self.hist_data_1y = None
        self.balance_sheet_annual = None
        self.balance_sheet_quarterly = None
        self.income_stmt_annual = None
        self.income_stmt_quarterly = None
        self.cash_flow_annual = None
        self.cash_flow_quarterly = None
        self.info = None
        
    def fetch_stock_data(self, years=0.2):
        """
        Fetch historical stock data for the specified number of years.
        
        Args:
            years (int): Number of years of historical data to fetch
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years*365)
            
            self.stock = yf.Ticker(self.symbol)
            
            # Fetch the data
            self.hist_data_2y = self.stock.history(
                start=start_date, 
                end=end_date, 
                auto_adjust=True
            )
            
            # Convert timezone-aware datetimes to timezone-naive
            self.hist_data_2y.index = self.hist_data_2y.index.tz_localize(None)
            
            if self.hist_data_2y.empty:
                print(f"No data found for symbol {self.symbol}")
                return False
                
            # Set 1-year data as a subset of 2-year data
            start_date_1y = end_date - timedelta(days=365)
            self.hist_data_1y = self.hist_data_2y[self.hist_data_2y.index >= start_date_1y]
            
            # Get company info
            self.info = self.stock.info
            
            return True
            
        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return False
            
    def fetch_financial_statements(self):
        """
        Fetch financial statements from Yahoo Finance.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.stock is None:
                self.stock = yf.Ticker(self.symbol)
            
            # Balance Sheet
            self.balance_sheet_annual = self.stock.balance_sheet
            self.balance_sheet_quarterly = self.stock.quarterly_balance_sheet
            
            # Income Statement
            self.income_stmt_annual = self.stock.income_stmt
            self.income_stmt_quarterly = self.stock.quarterly_income_stmt
            
            # Cash Flow
            self.cash_flow_annual = self.stock.cashflow
            self.cash_flow_quarterly = self.stock.quarterly_cashflow
            
            return True
            
        except Exception as e:
            print(f"Error fetching financial statements: {e}")
            return False
    
    def get_company_info(self):
        """
        Get basic company information.
        
        Returns:
            dict: Dictionary with company name, sector, industry
        """
        if self.info is None:
            if self.stock is None:
                self.stock = yf.Ticker(self.symbol)
            self.info = self.stock.info
            
        company_name = self.info.get('longName', self.symbol)
        sector = self.info.get('sector', 'N/A')
        industry = self.info.get('industry', 'N/A')
        
        return {
            'company_name': company_name,
            'sector': sector,
            'industry': industry,
            'current_price': self.info.get('currentPrice', 'N/A')
        }
    
    def calculate_price_trends(self):
        """
        Calculate price trends over different time periods.
        
        Returns:
            str: Formatted string with price trends information
        """
        if self.hist_data_1y is None:
            print("Historical data not available. Call fetch_stock_data() first.")
            return None
            
        as_of_date = self.hist_data_1y.index[-1]
        trends = {}
        periods = {
            '3m': 90,
            '6m': 180,
            '12m': 365
        }
        
        for label, days in periods.items():
            past_date = as_of_date - pd.Timedelta(days=days)
            # Find the closest available date in the index
            past_idx = self.hist_data_1y.index.searchsorted(past_date)
            if past_idx >= len(self.hist_data_1y):
                trends[label] = None
                continue
            past_price = self.hist_data_1y.iloc[past_idx]['Close']
            current_price = self.hist_data_1y.loc[as_of_date]['Close']
            if pd.isna(past_price) or pd.isna(current_price):
                trends[label] = None
            else:
                trends[label] = f"{100 * (current_price - past_price) / past_price:.2f}%"

        # All-time high and low
        all_time_high = self.hist_data_2y['Close'].max()
        all_time_high_date = self.hist_data_2y['Close'].idxmax()
        all_time_low = self.hist_data_2y['Close'].min()
        all_time_low_date = self.hist_data_2y['Close'].idxmin()
        
        # Format output string
        output = []
        if trends.get('3m') is not None:
            output.append(f"3-month price change: {trends['3m']} (Change in closing price over the last 3 months)")
        if trends.get('6m') is not None:
            output.append(f"6-month price change: {trends['6m']} (Change in closing price over the last 6 months)")
        if trends.get('12m') is not None:
            output.append(f"12-month price change: {trends['12m']} (Change in closing price over the last 12 months)")
        output.append(f"All-time high: ${all_time_high:.2f} on {all_time_high_date.date()} (Highest closing price in available data)")
        output.append(f"All-time low: ${all_time_low:.2f} on {all_time_low_date.date()} (Lowest closing price in available data)")
        
        return "\n".join(output)