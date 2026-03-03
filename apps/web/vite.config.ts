import { defineConfig } from "vite";

export default defineConfig({
  base: process.env.VITE_APP_BASE_PATH || "/",
  test: {
    environment: "jsdom",
    setupFiles: "./src/test/setup.ts"
  }
});
