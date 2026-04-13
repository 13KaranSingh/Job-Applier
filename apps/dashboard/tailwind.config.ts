import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#171717",
        sand: "#f5efe4",
        ember: "#ba4a1b",
        steel: "#39556b",
      },
    },
  },
  plugins: [],
};

export default config;

