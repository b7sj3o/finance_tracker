import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    host: 'tracker-frontend-4460ec945ddd.herokuapp.com/',
    port: 4200
  },
  plugins: [react()],
})
