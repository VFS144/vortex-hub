/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0A0614",
        foreground: "#FFFFFF",
        card: "#151022",
        primary: {
          DEFAULT: "#9D5CFF",
          dark: "#6E36D9",
          light: "#B87CFF",
        },
        secondary: {
          DEFAULT: "#6E36D9",
          light: "#C8B8FF",
        },
        accent: "#B87CFF",
        destructive: "#FF5757",
        border: "#2D1F45",
        input: "#151022",
        muted: {
          DEFAULT: "#C8B8FF",
          foreground: "#8B7BA8",
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        glow: "0 0 20px rgba(157, 92, 255, 0.3)",
        "glow-lg": "0 0 30px rgba(157, 92, 255, 0.4)",
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
      },
    },
  },
  plugins: [
    require("tailwindcss/plugin")(function ({ addBase, addComponents, addUtilities }) {
      addBase({
        html: {
          colorScheme: "dark",
        },
      });
    }),
  ],
}
