// This ensures no CORS error when the frontend fetches from FastAPI backend on port 8000.


import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/gita': 'http://127.0.0.1:8000',
      '/sentiment': 'http://127.0.0.1:8000',
      '/chatbot': 'http://127.0.0.1:8000'
    }
  }
})