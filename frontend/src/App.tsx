import { useEffect, useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { motion } from 'framer-motion'

// Pages
import HomePage from './pages/HomePage'
import MarketsPage from './pages/MarketsPage'
import SignalDetailsPage from './pages/SignalDetailsPage'
import ProfilePage from './pages/ProfilePage'
import ChartPage from './pages/ChartPage'

// Components
import Navigation from './components/Navigation'
import TelegramInit from './utils/telegram'

function App() {
  const [tgReady, setTgReady] = useState(false)

  useEffect(() => {
    TelegramInit.init()
    setTgReady(true)
    TelegramInit.expand()
  }, [])

  return (
    <Router>
      <motion.div
        className="min-h-screen bg-slate-900"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <Navigation />
        <main className="pt-16 pb-20">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/markets" element={<MarketsPage />} />
            <Route path="/signal/:id" element={<SignalDetailsPage />} />
            <Route path="/chart/:symbol" element={<ChartPage />} />
            <Route path="/profile" element={<ProfilePage />} />
          </Routes>
        </main>
        <Toaster position="bottom-center" />
      </motion.div>
    </Router>
  )
}

export default App
