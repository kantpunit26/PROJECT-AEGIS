/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        slate: {
          950: '#070A11',
          900: '#0B0F19',
          850: '#111827',
          800: '#1E293B',
          700: '#334155',
          600: '#475569',
        },
        crimson: {
          900: '#4C0505',
          800: '#7F1D1D',
          700: '#8B0000',
          600: '#B91C1C',
          500: '#DC2626',
          400: '#EF4444',
        },
        amr: {
          carbapenem: '#DC2626',
          colistin: '#9333EA',
          esbl: '#EA580C',
          fluoroquinolone: '#D97706',
          aminoglycoside: '#2563EB',
          susceptible: '#059669',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
      }
    },
  },
  plugins: [],
}

