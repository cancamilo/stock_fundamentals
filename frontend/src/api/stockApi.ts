/**
 * Stock API client
 * Functions to call the backend API for stock analysis
 */

const API_BASE_URL = 'http://localhost:8000';

/**
 * Get stock analysis data for a given ticker
 * @param ticker - Stock ticker symbol (e.g., 'AAPL')
 */
export async function getStockAnalysis(ticker: string) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/stock/${ticker}`);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch stock data');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching stock data:', error);
    throw error;
  }
}
