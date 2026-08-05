/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#00d4ff',
        dark: '#0a0a0f',
        dark2: '#12121a',
        dark3: '#1a1a2e',
      }
    },
  },
  plugins: [],
}