import { useState } from 'react';
import { getStockAnalysis } from '../api/stockApi';

export function StockAnalysis() {
  const [ticker, setTicker] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stockData, setStockData] = useState<any>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    if (!ticker.trim()) {
      setError('Please enter a stock ticker symbol');
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      const data = await getStockAnalysis(ticker.toUpperCase());
      setStockData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch stock data');
      setStockData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Stock Analysis</h1>
      
      <form onSubmit={handleSubmit} className="mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            placeholder="Enter stock ticker (e.g., AAPL)"
            className="px-4 py-2 border rounded flex-1"
          />
          <button 
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Loading...' : 'Analyze'}
          </button>
        </div>
      </form>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      {stockData && (
        <div className="bg-white shadow-md rounded-md p-6">
          <div className="mb-6">
            <h2 className="text-xl font-bold">{stockData.company_info.company_name} ({ticker.toUpperCase()})</h2>
            <div className="text-gray-600">
              <p>Sector: {stockData.company_info.sector}</p>
              <p>Industry: {stockData.company_info.industry}</p>
              <p>Current Price: ${stockData.company_info.current_price}</p>
            </div>
          </div>
          
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-2">Financial Highlights</h3>
            <div className="bg-gray-50 p-4 rounded">
              <pre className="whitespace-pre-wrap">{stockData.financial_highlights}</pre>
            </div>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-2">Financial Ratios</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(stockData.financial_ratios).map(([key, value]) => (
                <div key={key} className="flex justify-between border-b pb-1">
                  <span className="font-medium">{key}:</span>
                  <span>{String(value)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
