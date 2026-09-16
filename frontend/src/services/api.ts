import axios from 'axios'
import { MarketData, Signal, Candle, Indicators } from '../types'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_BASE}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const marketApi = {
  getAll: () => api.get<MarketData[]>('/markets/'),
  getOne: (symbol: string) => api.get<MarketData>(`/markets/${symbol}`),
  getTopMovers: () => api.get(`/markets/top-movers/summary`),
}

export const signalApi = {
  getAll: (limit?: number) => api.get<Signal[]>('/signals/', { params: { limit } }),
  getById: (id: number) => api.get<Signal>(`/signals/${id}`),
  getBySymbol: (symbol: string) => api.get<Signal[]>(`/signals/by-symbol/${symbol}`),
}

export const chartApi = {
  getCandles: (symbol: string, timeframe: string, limit?: number) =>
    api.get<{ candles: Candle[] }>(`/charts/${symbol}/candles`, {
      params: { timeframe, limit },
    }),
  getIndicators: (symbol: string, timeframe: string) =>
    api.get<{ indicators: Indicators }>(`/charts/${symbol}/indicators`, {
      params: { timeframe },
    }),
}

export const authApi = {
  validateMiniApp: (initData: string) =>
    api.post('/auth/validate-mini-app', { init_data: initData }),
}

export default api
