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
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 dark:from-gray-900 dark:to-blue-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white sm:text-5xl mb-3">
            Stock <span className="text-blue-600 dark:text-blue-400">Analysis</span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Enter a stock ticker to get detailed financial analysis and metrics
          </p>
        </div>
        
        {/* Search Form */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden mb-8 transition-all duration-300 hover:shadow-xl">
          <form onSubmit={handleSubmit} className="p-6">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="relative flex-grow">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
                  </svg>
                </div>
                <input
                  type="text"
                  value={ticker}
                  onChange={(e) => setTicker(e.target.value)}
                  placeholder="Enter stock ticker (e.g., AAPL)"
                  className="block w-full pl-10 pr-3 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg transition-all duration-200"
                />
              </div>
              <button 
                type="submit"
                disabled={loading}
                className="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-lg shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed min-w-[120px]"
              >
                {loading ? (
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                ) : null}
                {loading ? 'Analyzing...' : 'Analyze'}
              </button>
            </div>
          </form>
        </div>
      
        {/* Error Message */}
        {error && (
          <div className="bg-red-50 dark:bg-red-900/30 border-l-4 border-red-500 p-4 rounded-md mb-8 animate-fadeIn">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
              </div>
            </div>
          </div>
        )}
        
        {/* Stock Data Results */}
        {stockData && (
          <div className="animate-fadeIn">
            {/* Company Header Card */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden mb-6">
              <div className="md:flex">
                <div className="p-8">
                  <div className="flex items-center">
                    <div className="h-12 w-12 flex items-center justify-center bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300 rounded-lg text-xl font-bold">
                      {ticker.toUpperCase().slice(0, 2)}
                    </div>
                    <div className="ml-4">
                      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                        {stockData.company_info.company_name} 
                        <span className="ml-2 text-gray-500 dark:text-gray-400">({ticker.toUpperCase()})</span>
                      </h2>
                      <p className="text-gray-600 dark:text-gray-300 text-sm">{stockData.company_info.sector} • {stockData.company_info.industry}</p>
                    </div>
                  </div>
                  
                  <div className="mt-6 border-t border-gray-200 dark:border-gray-700 pt-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-gray-500 dark:text-gray-400">Current Price</p>
                        <p className="text-xl font-semibold text-gray-900 dark:text-white">${stockData.company_info.current_price}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Financial Highlights Card */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden mb-6">
              <div className="px-6 py-5 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M3 3a1 1 0 000 2h10a1 1 0 100-2H3zm0 4a1 1 0 000 2h6a1 1 0 100-2H3zm0 4a1 1 0 100 2h4a1 1 0 100-2H3z" clipRule="evenodd" />
                  </svg>
                  Financial Highlights
                </h3>
              </div>
              <div className="p-6">
                <div className="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-lg">
                  <pre className="whitespace-pre-wrap text-gray-700 dark:text-gray-200 font-mono text-sm">{stockData.financial_highlights}</pre>
                </div>
              </div>
            </div>
            
            {/* Financial Ratios Card */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden mb-6">
              <div className="px-6 py-5 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
                  </svg>
                  Financial Ratios
                </h3>
              </div>
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {Object.entries(stockData.financial_ratios).map(([key, value]) => (
                    <div key={key} className="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-lg">
                      <p className="text-sm font-medium text-gray-500 dark:text-gray-400">{key}</p>
                      <p className="mt-1 text-lg font-semibold text-gray-900 dark:text-white">{String(value)}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
