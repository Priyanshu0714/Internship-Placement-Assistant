/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./script.js",
    "./internship_assistant/**/*.{html,js}", // Fixed relative path
    "./templates/webapp/**/*.{html,js}", // Include HTML files in templates
    "./static/webapp/**/*.{html,js}", // Include JS files in static
  ],
  theme: {
    extend: {
      fontFamily: {
        custom: ["CustomFont", "sans-serif"],
      },
    },
  },
  plugins: [],
  corePlugins: {
    scrollbar: false,
  },
};
