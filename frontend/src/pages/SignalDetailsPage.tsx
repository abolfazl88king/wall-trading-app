import { useParams } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowDown, ArrowUp, TargetIcon, AlertCircle } from 'lucide-react'
import { signalApi } from '../services/api'
import { Signal } from '../types'

const SignalDetailsPage = () => {
  const { id } = useParams<{ id: string }>()
  const [signal, setSignal] = useState<Signal | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (id) {
      loadSignal(parseInt(id))
    }
  }, [id])

  const loadSignal = async (signalId: number) => {
    try {
      const response = await signalApi.getById(signalId)
      setSignal(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Failed to load signal:', error)
      setLoading(false)
    }
  }

  if (loading)
    return (
      <div className="px-4 py-6 max-w-2xl mx-auto">
        <div className="glass-card h-96 animate-pulse border border-slate-700"></div>
      </div>
    )

  if (!signal)
    return (
      <div className="px-4 py-6 max-w-2xl mx-auto text-center text-slate-400">Signal not found</div>
    )

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        {/* Header */}
        <div className="glass-card p-6 mb-6 border border-slate-700">
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-slate-400 text-sm mb-1">Trading Signal</p>
              <h1 className="text-3xl font-bold text-slate-100 text-number">{signal.symbol}</h1>
            </div>
            <div
              className={`px-4 py-2 rounded-lg font-bold flex items-center gap-2 ${
                signal.direction === 'LONG' ? 'bg-green-900/30 text-green-400' : 'bg-red-900/30 text-red-400'
              }`}
            >
              {signal.direction === 'LONG' ? <ArrowUp size={20} /> : <ArrowDown size={20} />}
              {signal.direction}
            </div>
          </div>
          <p className="text-slate-300">Confidence: {(signal.confidence * 100).toFixed(1)}%</p>
        </div>

        {/* Levels */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div className="glass-card p-4 border border-slate-700">
            <p className="text-slate-400 text-xs mb-1">Entry Price</p>
            <p className="text-2xl font-bold text-blue-400 text-number">${signal.entry_price.toFixed(2)}</p>
            <p className="text-xs text-slate-500 mt-1">Range: ${signal.entry_range_min.toFixed(2)} - ${signal.entry_range_max.toFixed(2)}</p>
          </div>

          <div className="glass-card p-4 border border-slate-700">
            <p className="text-slate-400 text-xs mb-1">Stop Loss</p>
            <p className="text-2xl font-bold text-red-400 text-number">${signal.stop_loss.toFixed(2)}</p>
          </div>

          <div className="glass-card p-4 border border-slate-700">
            <p className="text-slate-400 text-xs mb-1">Take Profit 1</p>
            <p className="text-2xl font-bold text-green-400 text-number">${signal.take_profit_1.toFixed(2)}</p>
          </div>

          <div className="glass-card p-4 border border-slate-700">
            <p className="text-slate-400 text-xs mb-1">Take Profit 2</p>
            <p className="text-2xl font-bold text-green-400 text-number">${signal.take_profit_2.toFixed(2)}</p>
          </div>
        </div>

        {/* Risk Reward */}
        <div className="glass-card p-6 mb-6 border border-slate-700">
          <div className="flex items-center gap-2 mb-3">
            <TargetIcon size={20} className="text-yellow-400" />
            <p className="font-semibold text-slate-100">Risk / Reward Ratio</p>
          </div>
          <p className="text-3xl font-bold text-yellow-400 text-number">{signal.risk_reward_ratio.toFixed(2)}x</p>
        </div>

        {/* Analysis Scores */}
        <div className="glass-card p-6 mb-6 border border-slate-700">
          <p className="font-semibold text-slate-100 mb-4">Analysis Breakdown</p>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-slate-400 text-sm">Trend</span>
                <span className="text-slate-300 text-sm font-semibold">{(signal.trend_score * 100).toFixed(0)}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${signal.trend_score * 100}%` }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-slate-400 text-sm">Momentum</span>
                <span className="text-slate-300 text-sm font-semibold">{(signal.momentum_score * 100).toFixed(0)}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div className="bg-purple-500 h-2 rounded-full" style={{ width: `${signal.momentum_score * 100}%` }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-slate-400 text-sm">Structure</span>
                <span className="text-slate-300 text-sm font-semibold">{(signal.structure_score * 100).toFixed(0)}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div className="bg-green-500 h-2 rounded-full" style={{ width: `${signal.structure_score * 100}%` }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-slate-400 text-sm">Volume</span>
                <span className="text-slate-300 text-sm font-semibold">{(signal.volume_score * 100).toFixed(0)}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div className="bg-yellow-500 h-2 rounded-full" style={{ width: `${signal.volume_score * 100}%` }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Reasons */}
        <div className="glass-card p-6 border border-slate-700">
          <p className="font-semibold text-slate-100 mb-4">Signal Reasons</p>
          <ul className="space-y-2">
            {signal.reasons.map((reason, idx) => (
              <li key={idx} className="flex items-start gap-2 text-slate-300 text-sm">
                <span className="text-green-400 font-bold mt-0.5">✓</span>
                {reason}
              </li>
            ))}
          </ul>
        </div>

        {/* Warning */}
        {signal.late_entry_rejected && (
          <motion.div
            className="glass-card p-4 mt-6 border border-red-500 bg-red-500/10 flex items-start gap-3"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <AlertCircle className="text-red-400 mt-0.5" size={20} />
            <div>
              <p className="font-semibold text-red-400">Late Entry Detected</p>
              <p className="text-sm text-red-300">Current price is too far from entry point. Signal rejected.</p>
            </div>
          </motion.div>
        )}
      </motion.div>
    </div>
  )
}

export default SignalDetailsPage
