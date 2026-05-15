/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        'tlh-teal': '#158c8b',
        'tlh-teal-dark': '#117170',
        'tlh-dark': '#132b42',
        'tlh-warm': '#fef3e2',
        'tlh-sand': '#f9f4eb',
        'tlh-purple': '#A47EAF',
      },
      fontSize: {
        'lg': '1.15rem',
        'xl': '1.15rem',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        'serif': ['Source Serif Pro', 'Georgia', 'serif'],
      }
    }
  },
  plugins: [],
}
