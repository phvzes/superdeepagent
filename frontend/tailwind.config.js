
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#00e0ff',
        secondary: '#6c5dd3',
        background: '#121212',
        surface: '#1e1e1e',
        error: '#cf6679',
        success: '#4caf50',
        warning: '#ff9800',
      },
    },
  },
  plugins: [],
}
