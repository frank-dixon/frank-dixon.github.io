/** scroll-progress: 9/28 portfolio house style (Michroma + IBM Plex, turquoise #0B8A8F on cream). */
module.exports = {
  content: ["./index.html"],
  corePlugins: { preflight: false },
  theme: {
    extend: {
      colors: {
        ink: "#243836",
        mute: "#5F6A65",
        teal: { DEFAULT: "#0B8A8F", deep: "#087075" },
      },
      fontFamily: {
        sans: ['"IBM Plex Sans"', 'system-ui', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'ui-monospace', 'monospace'],
        display: ['Michroma', '"IBM Plex Sans"', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
