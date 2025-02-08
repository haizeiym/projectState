import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    cors: true,
  },
  build: {
    target: 'es2015',
    outDir: 'dist',
    assetsDir: 'assets',
    rollupOptions: {
      external: ['@rollup/rollup-linux-arm64-musl'],
      output: {
        format: 'es'
      }
    }
  }
})