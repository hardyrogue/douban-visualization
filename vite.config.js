import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: 'localhost',
    port: 5173,
    open: true,
    fs: {
      strict: false
    },
    // ✅ history fallback 设置
    historyApiFallback: true
  }
})
