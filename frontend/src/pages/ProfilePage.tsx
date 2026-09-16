import { motion } from 'framer-motion'
import { User, Settings, LogOut, Bell } from 'lucide-react'
import { TelegramWebApp } from '../utils/telegram'

const ProfilePage = () => {
  const user = TelegramWebApp.getUser()

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold text-slate-100 mb-6">Profile</h1>

        {/* User Info */}
        <div className="glass-card p-6 mb-6 border border-slate-700">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center">
              <User size={32} className="text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-slate-100">
                {user?.first_name} {user?.last_name}
              </h2>
              {user?.username && <p className="text-slate-400">@{user.username}</p>}
              {user?.id && <p className="text-xs text-slate-500 mt-1">ID: {user.id}</p>}
            </div>
          </div>
          {user?.is_premium && (
            <div className="px-3 py-1 bg-yellow-500/20 text-yellow-400 rounded-full text-xs font-semibold inline-block">
              Premium Member
            </div>
          )}
        </div>

        {/* Settings */}
        <div className="glass-card border border-slate-700">
          <div className="p-4 border-b border-slate-600 flex items-center gap-3 cursor-pointer hover:bg-slate-700/50 transition">
            <Bell size={20} className="text-blue-400" />
            <div>
              <p className="font-semibold text-slate-100">Notifications</p>
              <p className="text-xs text-slate-400">Manage alerts and signals</p>
            </div>
          </div>
          <div className="p-4 border-b border-slate-600 flex items-center gap-3 cursor-pointer hover:bg-slate-700/50 transition">
            <Settings size={20} className="text-purple-400" />
            <div>
              <p className="font-semibold text-slate-100">Settings</p>
              <p className="text-xs text-slate-400">App preferences</p>
            </div>
          </div>
          <div className="p-4 flex items-center gap-3 cursor-pointer hover:bg-slate-700/50 transition">
            <LogOut size={20} className="text-red-400" />
            <div>
              <p className="font-semibold text-slate-100">Exit App</p>
              <p className="text-xs text-slate-400">Close WALL</p>
            </div>
          </div>
        </div>

        {/* App Info */}
        <div className="glass-card p-6 mt-6 border border-slate-700 text-center">
          <p className="text-slate-400 text-sm mb-2">WALL Trading Terminal</p>
          <p className="text-slate-500 text-xs">Version 1.0.0</p>
          <p className="text-slate-600 text-xs mt-4">© 2024 WALL. All rights reserved.</p>
        </div>
      </motion.div>
    </div>
  )
}

export default ProfilePage
