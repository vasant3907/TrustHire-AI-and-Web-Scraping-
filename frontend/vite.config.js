import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  cacheDir: '.vite-cache-codex',
  server: {
    port: 5173,
    host: 'localhost',
    strictPort: true,
    open: false
  },
  build: {
    outDir: 'dist',
    sourcemap: false
  }
})
