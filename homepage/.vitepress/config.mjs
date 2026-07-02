import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  lang: "en-US",
  title: "Pseudovirus deep mutational scanning of H5 HA for MHC-II interaction analysis",
  description:
    "Data, figures, and analysis for H5 HA deep mutational scanning",
  base: "/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS/",
  appearance: false,
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: "Home", link: "/" },
      { text: "Appendix", link: "/appendix", target: "_self" },
    ],
    socialLinks: [{ icon: "github", link: "https://github.com/dms-vep/Flu-H5N1-American-Wigeon-2021-HA-tufted-duck-MHCII-DMS" }],
    footer: {
      message: "Copyright © 2026-present Bernadeta Dadonaite and Jesse Bloom",
    },
  },
});
