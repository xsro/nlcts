
// vite.config.js
import {resolve} from 'path'
import wasm from "vite-plugin-wasm";

/** @type {import('vite').UserConfig} */
export default {
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        fen: resolve(__dirname, 'fen.html')
      }
    }
  },
  plugins: [
    wasm()
  ]
}
