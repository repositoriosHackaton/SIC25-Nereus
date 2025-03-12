// tailwind.config.js
module.exports = {
    content: [
      './src/**/*.{html,js,jsx,ts,tsx}',
      './templates/index.html',
    ],
    theme: {
      extend: {
        colors: {
          'bgcolor': 'var(--color-background)',
          'primary-text': 'var(--color-primary-text)',
          'accent-1': 'var(--color-accent-1)',
          'accent-2': 'var(--color-accent-2)',
          'buttoncolor': 'var(--color-button)',
        },
      },
    },
    plugins: [],
  };