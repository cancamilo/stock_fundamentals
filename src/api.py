"""
Stock Analysis API Server

This module provides FastAPI endpoints to access stock data and analysis.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import Dict, Any

from src.data import StockData
from src.financial_analysis import FinancialAnalysis

app = FastAPI(title="Stock Analysis API")

# Enable CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Return a welcome message."""
    return {"message": "Welcome to the Stock Analysis API"}

@app.get("/api/stock/{ticker}")
async def get_stock_analysis(ticker: str):
    """
    Get financial analysis data for a given stock ticker.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL')
        
    Returns:
        dict: Stock analysis data including financial ratios and company info
    """
    try:
        # Initialize stock data object
        stock_data = StockData(ticker)
        
        # Fetch stock data
        stock_data.fetch_stock_data()

        # Fetch financial statements
        stock_data.fetch_financial_statements()
        
        # Get basic company info
        company_info = stock_data.get_company_info()
        
        # Get financial analysis
        financial_analysis = FinancialAnalysis(stock_data)
        financial_ratios = financial_analysis.calculate_financial_ratios()
        
        # Convert financial ratios to a more JSON-friendly format
        formatted_ratios = {}
        for key, value in financial_ratios.items():
            if isinstance(value, (int, float, str)):
                formatted_ratios[key] = value
            else:
                formatted_ratios[key] = str(value)
                
        # Get financial highlights
        financial_highlights = financial_analysis.get_financial_highlights()

        # Get historical price and volume data (2 years)
        price_volume_data = []
        if hasattr(stock_data, 'hist_data_2y') and stock_data.hist_data_2y is not None:
            df = stock_data.hist_data_2y.reset_index()
            for row in df.itertuples(index=False):
                price_volume_data.append({
                    'date': str(row.Date) if hasattr(row, 'Date') else str(row[0]),
                    'close': float(row.Close),
                    'volume': int(row.Volume)
                })

        # Optionally, add AI/News analysis and comprehensive report if available
        news_analysis = None
        comprehensive_report = None
        try:
            from src.ai_analysis import AIAnalysis
            from src.reporting import ReportGenerator
            ai = AIAnalysis()
            company_name = company_info['company_name']
            price_trends = stock_data.calculate_price_trends()
            news_analysis = ai.get_news_analysis(company_name, ticker, price_trends)
            comprehensive_report = ai.generate_comprehensive_report(
                ticker,
                stock_data.info,
                financial_ratios,
                None,  # recent_indicators, can be added if needed
                news_analysis,
                price_trends=price_trends
            )
        except Exception:
            pass

        # Return combined data
        result = {
            "company_info": company_info,
            "financial_ratios": formatted_ratios,
            "financial_highlights": financial_highlights,
            "price_volume_data": price_volume_data,
            "news_analysis": news_analysis,
            "comprehensive_report": comprehensive_report
        }
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing {ticker}: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
