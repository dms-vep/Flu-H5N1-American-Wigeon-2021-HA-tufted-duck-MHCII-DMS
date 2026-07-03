import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  lang: "en-US",
  title: "How mutations to an H5 HA affect its interaction with tufted duck MHC-II",
  description:
    "Pseudovirus deep mutational scanning of how mutations to HA from A/American Wigeon/South Carolina/USDA-000345-001/2021 (H5N1) affects its interaction with tufted duck MHC-II",
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
