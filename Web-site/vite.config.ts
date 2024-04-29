import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    watch: {
      usePolling: true,
    },
    // host: "localhost",
    host: "0.0.0.0",
    port: 3001,

    proxy: {
      "/api/v1": {
        target: `http://${process.env.GOLANG_API || "127.0.0.1:5000"}`,
        changeOrigin: true,
        secure: false,      
        ws: true,
      },
    },
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
});
