import { defineConfig } from "vite";

export default defineConfig({
  root: "./publish",
  build: {
    rollupOptions: {
      input: {
        ninja: './styles/ninja.js',
        shiki: './styles/style.css'
      },
      output: {
        dir: './publish',
        entryFileNames: '[name].js'
      }
    }
  }
});
