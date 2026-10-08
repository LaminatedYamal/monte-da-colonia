/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        monte: {
          burgundy: '#5B1526', // rich wine red
          gold: '#C5A059',     // prestige gold
          olive: '#4A5B38',    // alentejo olive green
          sand: '#F7F5F0',     // luxury warm paper background
          earth: '#2B231D',    // deep warm charcoal/black
          cream: '#FAF8F5'
        }
      },
      fontFamily: {
        serif: ['Playfair Display', 'Cormorant Garamond', 'Georgia', 'serif'],
        garamond: ['"Cormorant Garamond"', 'Georgia', 'serif'],
        cinzel: ['Cinzel', 'Playfair Display', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif']
      }
    },
  },
  plugins: [],
};
