import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Home, TrendingUp, User, Menu, X } from 'lucide-react'

const Navigation = () => {
  const [mobileOpen, setMobileOpen] = useState(false)
  const location = useLocation()

  const isActive = (path: string) => location.pathname === path

  const navItems = [
    { path: '/', label: 'Home', icon: Home },
    { path: '/markets', label: 'Markets', icon: TrendingUp },
    { path: '/profile', label: 'Profile', icon: User },
  ]

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur border-b border-slate-800">
      <div className="max-w-6xl mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center">
              <span className="text-white font-bold text-sm">W</span>
            </div>
            <span className="font-bold text-slate-100 hidden sm:inline">WALL</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex gap-1">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link key={path} to={path}>
                <motion.button
                  whileHover={{ y: -2 }}
                  className={`px-4 py-2 rounded-lg flex items-center gap-2 font-semibold transition ${
                    isActive(path)
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-300 hover:text-slate-100 hover:bg-slate-800'
                  }`}
                >
                  <Icon size={18} />
                  {label}
                </motion.button>
              </Link>
            ))}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden text-slate-300 hover:text-slate-100"
          >
            {mobileOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="md:hidden mt-4 pb-4 space-y-2 border-t border-slate-800 pt-4"
          >
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                onClick={() => setMobileOpen(false)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition ${
                  isActive(path)
                    ? 'bg-blue-600 text-white'
                    : 'text-slate-300 hover:text-slate-100 hover:bg-slate-800'
                }`}
              >
                <Icon size={18} />
                {label}
              </Link>
            ))}
          </motion.div>
        )}
      </div>
    </nav>
  )
}

export default Navigation
