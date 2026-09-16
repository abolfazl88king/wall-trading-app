import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { motion } from 'framer-motion'

const ChartPage = () => {
  const { symbol } = useParams<{ symbol: string }>()

  return (
    <div className="px-4 py-6 max-w-6xl mx-auto">
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        <h1 className="text-3xl font-bold text-slate-100 mb-6">{symbol} Chart</h1>

        {/* Chart Placeholder - Ready for Lightweight Charts integration */}
        <div className="glass-card p-6 h-96 border border-slate-700 flex items-center justify-center">
          <p className="text-slate-400">Chart will be integrated with Lightweight Charts library</p>
        </div>

        {/* Timeframe Selector */}
        <div className="flex gap-2 mt-6 mb-6">
          {['1m', '5m', '15m', '1h', '4h', '1D'].map((tf) => (
            <button
              key={tf}
              className="px-4 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-slate-100 transition font-semibold text-sm"
            >
              {tf}
            </button>
          ))}
        </div>
      </motion.div>
    </div>
  )
}

export default ChartPage
