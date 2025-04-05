import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
export default defineConfig({
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src')  // ✅ 加上这行
      }
    },
    server: {
      host: 'localhost',
      port: 5173,
      open: true,
      fs: {
        strict: false
      },
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // 你 Django 的地址
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
