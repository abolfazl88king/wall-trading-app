import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowUp, TrendingUp, Zap } from 'lucide-react'
import { useAppStore } from '../store'
import { marketApi } from '../services/api'
import { MarketData } from '../types'

const HomePage = () => {
  const [loading, setLoading] = useState(true)
  const [markets, setMarkets] = useState<MarketData[]>()
  const [btcPrice, setBtcPrice] = useState<number>(0)
  const { updateMarket } = useAppStore()

  useEffect(() => {
    loadMarkets()
    const interval = setInterval(loadMarkets, 5000)
    return () => clearInterval(interval)
  }, [])

  const loadMarkets = async () => {
    try {
      const response = await marketApi.getAll()
      const data = response.data
      setMarkets(data)
      data.forEach((market) => updateMarket(market))
      const btc = data.find((m) => m.symbol === 'BTCUSDT')
      if (btc) setBtcPrice(btc.price)
      setLoading(false)
    } catch (error) {
      console.error('Failed to load markets:', error)
      setLoading(false)
    }
  }

  return (
    <div className="px-4 py-6 max-w-6xl mx-auto">
      {/* Header */}
      <motion.div
        className="mb-8"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex items-center gap-3 mb-2">
          <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center">
            <span className="text-white font-bold text-xl">W</span>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-slate-100">WALL</h1>
            <p className="text-slate-400 text-sm">Premium Trading Terminal</p>
          </div>
        </div>
      </motion.div>

      {/* BTC Price Card */}
      {btcPrice > 0 && (
        <motion.div
          className="glass-card mb-6 p-6 border border-slate-700"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <p className="text-slate-400 text-sm mb-2">Bitcoin Price</p>
          <div className="flex items-baseline gap-3">
            <span className="text-4xl font-bold text-slate-100 text-number">${btcPrice.toFixed(2)}</span>
            <span className="text-green-400 flex items-center gap-1 text-number">
              <ArrowUp size={20} />
              +2.5%
            </span>
          </div>
        </motion.div>
      )}

      {/* Quick Stats */}
      <motion.div
        className="grid grid-cols-3 gap-4 mb-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <div className="glass-card p-4 text-center border border-slate-700">
          <div className="text-slate-400 text-xs mb-2">Active Signals</div>
          <div className="text-2xl font-bold text-blue-400">12</div>
        </div>
        <div className="glass-card p-4 text-center border border-slate-700">
          <div className="text-slate-400 text-xs mb-2">Win Rate</div>
          <div className="text-2xl font-bold text-green-400">68%</div>
        </div>
        <div className="glass-card p-4 text-center border border-slate-700">
          <div className="text-slate-400 text-xs mb-2">Avg R:R</div>
          <div className="text-2xl font-bold text-yellow-400">2.5x</div>
        </div>
      </motion.div>

      {/* Markets Grid */}
      <div className="mb-6">
        <h2 className="text-xl font-bold text-slate-100 mb-4">Market Overview</h2>
        {loading ? (
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="glass-card h-24 animate-pulse border border-slate-700"></div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {markets?.slice(0, 6).map((market) => (
              <motion.div
                key={market.symbol}
                className="glass-card p-4 border border-slate-700 hover:border-slate-500 transition-all cursor-pointer"
                whileHover={{ y: -2 }}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-slate-300 font-semibold text-number">{market.symbol}</p>
                    <p className="text-2xl font-bold text-slate-100 text-number">${market.price.toFixed(2)}</p>
                  </div>
                  <div
                    className={`text-right ${
                      market.change_24h_percent >= 0 ? 'text-green-400' : 'text-red-400'
                    }`}
                  >
                    <div className="flex items-center gap-1 justify-end text-number">
                      {market.change_24h_percent >= 0 ? <ArrowUp size={16} /> : <ArrowUp size={16} className="rotate-180" />}
                      {Math.abs(market.change_24h_percent).toFixed(2)}%
                    </div>
                    <p className="text-xs text-slate-400 mt-1">Vol: ${(market.volume_24h / 1e9).toFixed(2)}B</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default HomePage
