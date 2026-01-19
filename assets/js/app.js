const { createApp } = Vue;

createApp({
  data() {
    return {
      theme: "dark" // dark = tech, light = engagements
    };
  },

  computed: {
    themeLabel() {
      return this.theme === "dark"
        ? "Engagements"
        : "Tech / Hacking";
    },
    themeIcon() {
      return this.theme === "dark" ? "☀" : "☾";
    },
    terminalText() {
      return [
        "$ whoami",
        "Raphael",
        "",
        "$ cat skills.txt",
        "- web",
        "- reverse",
        "- linux",
        "- ctf",
        "",
        "$ _"
      ].join("\n");
    },
    engagementText() {
      return [
        "> engagements.log",
        "- secourisme",
        "- scoutisme",
        "- BAFA",
        "",
        "> _"
      ].join("\n");
    }
  },

  methods: {
    applyTheme(theme) {
      this.theme = theme;
      document.documentElement.setAttribute("data-theme", theme);
      localStorage.setItem("theme", theme);
    },

    toggleTheme() {
      this.applyTheme(this.theme === "dark" ? "light" : "dark");
    }
  },
  applyTheme(theme) {
  this.theme = theme;
  document.documentElement.setAttribute("data-theme", theme); // <html>
  localStorage.setItem("theme", theme);
},
  mounted() {
    const saved = localStorage.getItem("theme");
    this.applyTheme(saved === "light" ? "light" : "dark");
  }
}).mount("#app");
