import { defineConfig, fontProviders } from "astro/config";
export default defineConfig({
  site: "https://jakknaj.github.io",
  base: process.env.ASTRO_BASE ?? "/",
  output: "static",
  devToolbar: { enabled: false },
  fonts: [
    {
      name: "Inter",
      cssVariable: "--font-inter",
      provider: fontProviders.local(),
      options: {
        variants: [
          {
            weight: "100 900",
            style: "normal",
            src: ["./public/fonts/InterVariable.woff2"],
          },
        ],
      },
    },
  ],
});
