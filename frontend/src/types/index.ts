export interface MarketData {
  symbol: string
  price: number
  high_24h: number
  low_24h: number
  volume_24h: number
  change_24h_percent: number
  last_updated: string
}

export interface Signal {
  id: number
  symbol: string
  direction: 'LONG' | 'SHORT'
  entry_price: number
  entry_range_min: number
  entry_range_max: number
  stop_loss: number
  take_profit_1: number
  take_profit_2: number
  risk_reward_ratio: number
  confidence: number
  trend_score: number
  momentum_score: number
  structure_score: number
  volume_score: number
  volatility_score: number
  reasons: string[]
  atr_value: number
  late_entry_rejected: boolean
  is_active: boolean
  entry_alert_sent: boolean
  created_at: string
  updated_at: string
}

export interface Candle {
  t: number
  o: number
  h: number
  l: number
  c: number
  v: number
}

export interface Indicators {
  ema_20?: number
  ema_50?: number
  ema_200?: number
  rsi?: number
  atr?: number
  macd?: number
  macd_signal?: number
  macd_histogram?: number
}

export interface TelegramUser {
  id: number
  first_name: string
  last_name?: string
  username?: string
  language_code?: string
  is_premium?: boolean
}
