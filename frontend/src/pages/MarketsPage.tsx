import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Search, Filter } from 'lucide-react'
import { marketApi } from '../services/api'
import { MarketData } from '../types'

const MarketsPage = () => {
  const [markets, setMarkets] = useState<MarketData[]>([])
  const [filtered, setFiltered] = useState<MarketData[]>([])
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState('all')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadMarkets()
  }, [])

  useEffect(() => {
    filterMarkets()
  }, [markets, search, filter])

  const loadMarkets = async () => {
    try {
      const response = await marketApi.getAll()
      setMarkets(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Failed to load markets:', error)
      setLoading(false)
    }
  }

  const filterMarkets = () => {
    let result = markets

    if (search) {
      result = result.filter((m) => m.symbol.toLowerCase().includes(search.toLowerCase()))
    }

    if (filter === 'gainers') {
      result = result.filter((m) => m.change_24h_percent > 0).sort((a, b) => b.change_24h_percent - a.change_24h_percent)
    } else if (filter === 'losers') {
      result = result.filter((m) => m.change_24h_percent < 0).sort((a, b) => a.change_24h_percent - b.change_24h_percent)
    }

    setFiltered(result)
  }

  return (
    <div className="px-4 py-6 max-w-6xl mx-auto">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold text-slate-100 mb-6">Markets</h1>

        {/* Search and Filter */}
        <div className="flex gap-3 mb-6">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-3 text-slate-400" size={20} />
            <input
              type="text"
              placeholder="Search coins..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
          </div>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:border-blue-500"
          >
            <option value="all">All</option>
            <option value="gainers">Gainers</option>
            <option value="losers">Losers</option>
          </select>
        </div>

        {/* Market List */}
        <div className="space-y-3">
          {loading ? (
            Array(10)
              .fill(null)
              .map((_, i) => <div key={i} className="glass-card h-16 animate-pulse border border-slate-700"></div>)
          ) : filtered.length > 0 ? (
            filtered.map((market) => (
              <motion.div
                key={market.symbol}
                className="glass-card p-4 flex justify-between items-center border border-slate-700 hover:border-slate-500 cursor-pointer transition-all"
                whileHover={{ x: -4 }}
              >
                <div>
                  <p className="font-semibold text-slate-100 text-number">{market.symbol}</p>
                  <p className="text-xs text-slate-400">24h Volume: ${(market.volume_24h / 1e9).toFixed(2)}B</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold text-slate-100 text-number">${market.price.toFixed(2)}</p>
                  <p className={`text-sm font-semibold ${market.change_24h_percent >= 0 ? 'text-green-400' : 'text-red-400'} text-number`}>
                    {market.change_24h_percent >= 0 ? '+' : ''}
                    {market.change_24h_percent.toFixed(2)}%
                  </p>
                </div>
              </motion.div>
            ))
          ) : (
            <div className="text-center text-slate-400 py-8">No markets found</div>
          )}
        </div>
      </motion.div>
    </div>
  )
}

export default MarketsPage
