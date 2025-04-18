"""
AI Analysis Module

This module provides functions for analyzing stock data using AI tools (OpenAI).
"""

import os
from datetime import datetime
import openai
from dotenv import load_dotenv


class AIAnalysis:
    """Class for AI-powered stock analysis."""
    
    def __init__(self, api_key=None):
        """
        Initialize with OpenAI API key.
        
        Args:
            api_key (str, optional): OpenAI API key. If None, looks for 
                                    OPENAI_API_KEY in environment variables.
        """
        # Load environment variables if no API key provided
        if api_key is None:
            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")
        
        self.api_key = api_key
        self.client = None
        
        if self.api_key:
            try:
                self.client = openai.OpenAI(api_key=api_key)
                print("OpenAI client initialized successfully.")
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}")
    
    def get_news_analysis(self, company_name, stock_symbol, price_trends=None):
        """
        Get news analysis from OpenAI.
        
        Args:
            company_name (str): Company name
            stock_symbol (str): Stock ticker symbol
            price_trends (str, optional): Price trends data
            
        Returns:
            str: News analysis text
        """
        if self.client is None:
            return "OpenAI client not initialized. Please set up your API key."
        
        try:
            # Current date for context
            today = datetime.now().strftime("%d %B %Y")
            prompt = f"""
                    Today is {today}. Provide a comprehensive summary of the most significant recent news about {company_name} ({stock_symbol}) 
                    that could impact its stock price and fundamental value. The user will provide you also with the price trend of the company. 
                    
                    Focus on:
                    
                    1. Recent earnings reports and financial performance.
                    2. Reasoning behind the price development of the stock in the past.  
                    2. Major business developments (new products, services, markets)
                    3. Future innovations, partnerships, or acquisitions. 
                    4. Leadership changes or organizational restructuring
                    5. Regulatory developments affecting the company
                    6. Macroeconomic factors influencing the company and its industry
                    7. Geopolitical events that might impact operations or supply chains
                    8. Competitive landscape changes

                    You should do a detailed internet search for each of the points above before reaching a conclusion.

                    Think in steps.
                    
                    Format your response as a well-structured analysis with clear sections and bullet points where appropriate.
                    Include dates of key events where possible. Highlight the potential impact of each development on the company's future performance.

                    {price_trends}
                    """
                
            response = self.client.responses.create(
                model="gpt-4o-mini",
                tools=[{ "type": "web_search_preview" }],
                input=prompt,
            )
            return response.output[1].content[0].text
        except Exception as e:
            return f"Error fetching news analysis: {e}"
    
    def generate_comprehensive_report(self, stock_symbol, stock_info, financial_ratios, 
                                    tech_indicators, news_analysis, price_trends=None):
        """
        Generate a comprehensive stock analysis report using OpenAI.
        
        Args:
            stock_symbol (str): Stock symbol
            stock_info (dict): Stock information dictionary
            financial_ratios (dict): Financial ratios dictionary
            tech_indicators (dict): Technical indicators dictionary
            news_analysis (str): News analysis text
            price_trends (str, optional): Price trends text
            
        Returns:
            str: Comprehensive analysis report
        """
        if self.client is None:
            return "OpenAI client not initialized. Please set up your API key."
        
        try:
            # Prepare financial ratios string
            ratios_str = "\n".join([f"{ratio}: {value}" for ratio, value in financial_ratios.items()])
            
            # Prepare technical indicators string
            tech_str = "\n".join([f"{indicator}: {value}" for indicator, value in tech_indicators.items()])
            
            # Prepare info summary
            info_summary = f"""
            Company: {stock_info.get('company_name', stock_symbol)}
            Symbol: {stock_symbol}
            Sector: {stock_info.get('sector', 'N/A')}
            Industry: {stock_info.get('industry', 'N/A')}
            Current Price: ${stock_info.get('current_price', 'N/A')}
            52-Week Range: ${stock_info.get('fiftyTwoWeekLow', 'N/A')} - ${stock_info.get('fiftyTwoWeekHigh', 'N/A')}
            Market Cap: ${stock_info.get('marketCap', 'N/A')}
            Beta: {stock_info.get('beta', 'N/A')}
            Price Trends: {price_trends}
            """
            
            # Current date for context
            today = datetime.now().strftime("%Y-%m-%d")
            
            prompt = f"""
            Today is {today}. As a financial analyst, provide a comprehensive investment analysis report for {stock_symbol} based on the following information:
            
            COMPANY INFORMATION:
            {info_summary}
            
            FINANCIAL RATIOS:
            {ratios_str}
            
            TECHNICAL INDICATORS (Most Recent):
            {tech_str}
            
            NEWS ANALYSIS:
            {news_analysis}
            
            Based on all this information, provide a comprehensive investment analysis with the following sections:
            
            1. Executive Summary - A brief overview of the company and its current situation
            2. Fundamental Analysis - Analysis of financial health, valuation, and growth prospects
            3. Technical Analysis - Interpretation of price movements and technical indicators
            4. News Impact Analysis - How recent news affects the company's prospects
            5. Risk Assessment - Key risks facing the company
            6. Investment Outlook - Overall assessment including strengths, weaknesses, opportunities, and threats
            7. Recommendation - Clear investment recommendation (Buy/Hold/Sell) with reasoning
            
            The report should be well-structured with clear sections and bullet points where appropriate.
            Focus on providing actionable insights based on the data provided.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Use appropriate model based on your OpenAI subscription
                messages=[
                    {"role": "system", "content": "You are a senior financial analyst with extensive experience in equity research and investment analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating comprehensive report: {e}"