
// vite.config.js
import {resolve} from 'path'
import wasm from "vite-plugin-wasm";
import topLevelAwait from "vite-plugin-top-level-await";

/** @type {import('vite').UserConfig} */
export default {
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        // fen: resolve(__dirname, 'fen.html')
      },
      output: {
      }
    }
  },
  plugins: [
    wasm(),
    topLevelAwait({
      // The export name of top-level await promise for each chunk module
      promiseExportName: "__tla",
      // The function to generate import names of top-level await promise in each chunk module
      promiseImportName: i => `__tla_${i}`
    })
  ]
}
