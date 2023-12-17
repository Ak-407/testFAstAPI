import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    rollupOptions: {
      external: ['RegistrationForm'],
    },
  },
  resolve: {
    alias: {
      '@': '/src',  // Adjust the alias as needed
    },
  },
  plugins: [react()],
})
