const { createApp } = Vue;

createApp({
  data() {
    return {
      theme: "dark",
      terminalTitle: "session@portfolio:~",
    };
  },
  computed: {
    themeLabel() {
      return this.theme === "dark" ? "Nuit" : "Jour";
    },
    themeIcon() {
      return this.theme === "dark" ? "☾" : "☀";
    },
    nowLine() {
      const d = new Date();
      return d.toLocaleString("fr-FR", { dateStyle: "medium", timeStyle: "short" });
    },
    terminalText() {
      const lines = [
        "$ whoami",
        "raphael",
        "",
        "$ cat skills.txt",
        "- pentest web",
        "- scripting (python/bash)",
        "- linux & réseau",
        "- ctf / writeups",
        "",
        "$ echo \"Bienvenue sur mon portfolio\"",
        "Bienvenue sur mon portfolio",
        "",
        "$ _"
      ];
      return lines.join("\n");
    }
  },
  methods: {
    applyThemeToHtml(theme) {
      // on applique sur <html> pour être robuste même si #app change
      document.documentElement.setAttribute("data-theme", theme);
    },
    loadTheme() {
      const saved = localStorage.getItem("theme");
      if (saved === "dark" || saved === "light") this.theme = saved;
      this.applyThemeToHtml(this.theme);
    },
    toggleTheme() {
      this.theme = this.theme === "dark" ? "light" : "dark";
      localStorage.setItem("theme", this.theme);
      this.applyThemeToHtml(this.theme);
    },
    handleKeydown(e) {
      // T = toggle thème
      if (e.key && e.key.toLowerCase() === "t") this.toggleTheme();
    }
  },
  mounted() {
    this.loadTheme();
    window.addEventListener("keydown", this.handleKeydown);
  },
  beforeUnmount() {
    window.removeEventListener("keydown", this.handleKeydown);
  }
}).mount("#app");
