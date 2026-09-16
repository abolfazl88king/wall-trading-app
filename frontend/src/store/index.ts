import { create } from 'zustand'
import { MarketData, Signal } from '../types'

interface AppStore {
  markets: Map<string, MarketData>
  signals: Signal[]
  selectedSymbol: string
  updateMarket: (data: MarketData) => void
  updateSignals: (signals: Signal[]) => void
  setSelectedSymbol: (symbol: string) => void
}

export const useAppStore = create<AppStore>((set) => ({
  markets: new Map(),
  signals: [],
  selectedSymbol: 'BTCUSDT',
  updateMarket: (data) =>
    set((state) => {
      const newMarkets = new Map(state.markets)
      newMarkets.set(data.symbol, data)
      return { markets: newMarkets }
    }),
  updateSignals: (signals) => set({ signals }),
  setSelectedSymbol: (symbol) => set({ selectedSymbol: symbol }),
}))
