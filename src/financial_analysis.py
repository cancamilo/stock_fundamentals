"""
Financial Analysis Module

This module provides functions to analyze financial data and calculate key financial ratios.
"""

import pandas as pd
import numpy as np
from src.data import StockData


class FinancialAnalysis:
    """Class for financial ratio calculation and analysis."""

    def __init__(self, stock_data: StockData):
        """
        Initialize with stock data.
        
        Args:
            stock_data (StockData): Instance of StockData class
        """
        self.stock_data = stock_data
    
    def calculate_financial_ratios(self):
        """
        Calculate important financial ratios for fundamental analysis.
        
        Returns:
            dict: Dictionary of financial ratios
        """
        if self.stock_data.info is None:
            print("Stock info not available. Fetch stock data first.")
            return {}
        
        info = self.stock_data.info
        ratios = {}
        
        # Valuation Ratios
        ratios['P/E Ratio'] = info.get('trailingPE', 'N/A')
        ratios['Forward P/E'] = info.get('forwardPE', 'N/A')
        ratios['P/B Ratio'] = info.get('priceToBook', 'N/A')
        ratios['P/S Ratio'] = info.get('priceToSalesTrailing12Months', 'N/A')
        ratios['EV/EBITDA'] = info.get('enterpriseToEbitda', 'N/A')
        
        # PEG Ratio (Price/Earnings to Growth)
        pe = info.get('trailingPE', None)
        earnings_growth = info.get('earningsGrowth', None)
        if isinstance(pe, (int, float)) and isinstance(earnings_growth, (int, float)) and earnings_growth != 0:
            ratios['PEG Ratio'] = pe / (earnings_growth * 100)
        else:
            ratios['PEG Ratio'] = 'N/A'
        
        # Profitability Ratios
        ratios['Gross Margin'] = info.get('grossMargins', 'N/A')
        ratios['Operating Margin'] = info.get('operatingMargins', 'N/A')
        ratios['Net Profit Margin'] = info.get('profitMargins', 'N/A')
        ratios['ROE'] = info.get('returnOnEquity', 'N/A')
        ratios['ROA'] = info.get('returnOnAssets', 'N/A')
        
        # Liquidity Ratios
        ratios['Current Ratio'] = info.get('currentRatio', 'N/A')
        ratios['Quick Ratio'] = info.get('quickRatio', 'N/A')
        
        # Debt Ratios
        ratios['Debt-to-Equity'] = info.get('debtToEquity', 'N/A')
        ratios['Interest Coverage'] = info.get('interestCoverage', 'N/A')
        
        # Dividend Ratios
        ratios['Dividend Yield'] = info.get('dividendYield', 'N/A')
        ratios['Payout Ratio'] = info.get('payoutRatio', 'N/A')
        
        # Growth Rates
        ratios['Revenue Growth (YoY)'] = info.get('revenueGrowth', 'N/A')
        ratios['Earnings Growth (YoY)'] = info.get('earningsGrowth', 'N/A')
        
        return ratios

    def format_financial_ratios(self, ratios):
        """
        Format financial ratios for display.
        
        Args:
            ratios (dict): Dictionary of financial ratios
            
        Returns:
            pandas.DataFrame: DataFrame with formatted ratios
        """
        ratios_df = pd.DataFrame(list(ratios.items()), columns=['Ratio', 'Value'])
        
        # Convert numeric values
        ratios_df['Value'] = pd.to_numeric(ratios_df['Value'], errors='ignore')
        
        # Format values for display
        formatted_values = []
        for idx, row in ratios_df.iterrows():
            if row['Ratio'] in ['Dividend Yield', 'Gross Margin', 'Operating Margin', 
                              'Net Profit Margin', 'ROE', 'ROA', 'Payout Ratio',
                              'Revenue Growth (YoY)', 'Earnings Growth (YoY)']:
                if isinstance(row['Value'], (int, float)):
                    formatted_values.append(f"{row['Value']:.2%}")
                else:
                    formatted_values.append(row['Value'])
            elif row['Ratio'] == 'PEG Ratio':
                if isinstance(row['Value'], (int, float)):
                    formatted_values.append(f"{row['Value']:.2f}")
                else:
                    formatted_values.append(row['Value'])
            else:
                if isinstance(row['Value'], (int, float)):
                    formatted_values.append(f"{row['Value']:.2f}")
                else:
                    formatted_values.append(row['Value'])
                    
        ratios_df['Formatted Value'] = formatted_values
        return ratios_df[['Ratio', 'Formatted Value']]
        
    def get_financial_highlights(self):
        """
        Get key financial highlights from the most recent annual data.
        
        Returns:
            str: Formatted string with financial highlights
        """
        if self.stock_data.income_stmt_annual is None or self.stock_data.balance_sheet_annual is None:
            print("Financial statements not available. Fetch financial statements first.")
            return ""
        
        highlights = []
        
        # Extract data from income statement
        if not self.stock_data.income_stmt_annual.empty:
            recent_year = self.stock_data.income_stmt_annual.columns[0]
            revenue = self.stock_data.income_stmt_annual.loc['Total Revenue', recent_year] / 1e6
            
            if revenue is not None:
                highlights.append(f"Revenue: ${revenue:.2f}M")
            
            net_income = self.stock_data.income_stmt_annual.loc['Net Income', recent_year] / 1e6
            if net_income is not None:
                highlights.append(f"Net Income: ${net_income:.2f}M")
            
            ebitda = self.stock_data.income_stmt_annual.loc['EBITDA', recent_year] / 1e6
            if ebitda is not None:
                highlights.append(f"EBITDA: ${ebitda:.2f}M")
        
        # Extract data from balance sheet
        if not self.stock_data.balance_sheet_annual.empty:
            recent_year = self.stock_data.balance_sheet_annual.columns[0]
            total_assets = self.stock_data.balance_sheet_annual.loc['Total Assets', recent_year] / 1e6
            if total_assets is not None:
                highlights.append(f"Total Assets: ${total_assets:.2f}M")
            
            total_liabilities = self.stock_data.balance_sheet_annual.loc['Total Liabilities Net Minority Interest', recent_year]
            if total_liabilities is not None:
                highlights.append(f"Total Liabilities: ${total_liabilities:.2f}M")
                
                # Calculate equity
                equity = total_assets - total_liabilities
                highlights.append(f"Equity: ${equity:.2f}M")
        
        return "\n".join(highlights)