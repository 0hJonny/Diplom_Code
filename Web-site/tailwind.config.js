/** @type {import('tailwindcss').Config} */

export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        accent: {},
        bkg: "rgb(var(--color-bkg) / <alpha-value>)",
        textPrimary: "rgb(var(--color-text-primary) / <alpha-value>)",
        textSub: "rgb(var(--color-text-sub) / <alpha-value>)",
        textTitle: "rgb(var(--color-text-title) / <alpha-value>)",
      },
    },
  },
  plugins: [],
};
