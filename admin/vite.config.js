import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src')
    }
  },
  server: {
    port: 8000,
    open: true, // 服务启动时是否自动打开浏览器
    cors: true, // 允许跨域
    host: "localhost",
  },
})
