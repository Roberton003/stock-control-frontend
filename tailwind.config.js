/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0C4B6A',      // Azul petróleo
        secondary: '#3DBEA3',    // Verde água
        accent: '#FF6B35',       // Laranja
        light: '#F8F9FA',        // Cinza claro
        dark: '#2D3748',         // Cinza escuro
      }
    },
  },
  plugins: [],
}

