import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
// We'll keep the import for App.css in case we need custom styles
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 p-4">
      <div className="flex gap-8 mb-8">
        <a href="https://vite.dev" target="_blank" className="hover:opacity-80">
          <img src={viteLogo} className="h-24 w-auto" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank" className="hover:opacity-80">
          <img src={reactLogo} className="h-24 w-auto animate-spin-slow" alt="React logo" />
        </a>
      </div>
      <h1 className="text-4xl font-bold mb-6">Stock Analysis App</h1>
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md max-w-md w-full mb-8">
        <button 
          onClick={() => setCount((count) => count + 1)}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded mb-4 transition-colors"
        >
          Count is {count}
        </button>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          This is a test of our Tailwind CSS setup. Later we'll build our stock analysis frontend here.
        </p>
      </div>
      <p className="text-sm text-center text-gray-500 dark:text-gray-400 max-w-md">
        This frontend will connect to your Python backend for analyzing and comparing stocks
      </p>
    </div>
  )
}

export default App
