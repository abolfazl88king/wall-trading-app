export class TelegramWebApp {
  static init() {
    if (window.Telegram?.WebApp) {
      window.Telegram.WebApp.ready()
    }
  }

  static expand() {
    if (window.Telegram?.WebApp) {
      window.Telegram.WebApp.expand()
    }
  }

  static getUser() {
    return window.Telegram?.WebApp?.initDataUnsafe?.user || null
  }

  static getInitData() {
    return window.Telegram?.WebApp?.initData || ''
  }

  static showAlert(message: string) {
    if (window.Telegram?.WebApp) {
      window.Telegram.WebApp.showAlert(message)
    } else {
      alert(message)
    }
  }

  static showConfirm(message: string, callback: (ok: boolean) => void) {
    if (window.Telegram?.WebApp) {
      window.Telegram.WebApp.showConfirm(message, callback)
    } else {
      callback(window.confirm(message))
    }
  }

  static setHeaderColor(color: string) {
    if (window.Telegram?.WebApp) {
      window.Telegram.WebApp.setHeaderColor(color)
    }
  }
}

export default TelegramWebApp
