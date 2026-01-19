const { createApp } = Vue;

createApp({
  data() {
    return {
      universe: "tech", // "tech" | "life"
      terminalTitle: "session@portfolio:~",
    };
  },
  computed: {
    universeLabel() {
      return this.universe === "tech" ? "Vie / Engagements" : "Tech / Hacking";
    },
    universeIcon() {
      return this.universe === "tech" ? "☀" : "☾";
    },
    nowLine() {
      const d = new Date();
      return d.toLocaleString("fr-FR", { dateStyle: "medium", timeStyle: "short" });
    },
    terminalText() {
      return [
        "$ whoami",
        "raphael",
        "",
        "$ cat skills.txt",
        "- pentest web",
        "- scripting (python/bash)",
        "- linux & réseau",
        "- ctf / writeups",
        "",
        "$ _"
      ].join("\n");
    },
    lifeText() {
      return [
        "> engagement.log",
        "- secourisme: formation / gestes / checklists",
        "- scouts: encadrement / camp / logistique",
        "- terrain: calme, organisation, esprit d'équipe",
        "",
        "> _"
      ].join("\n");
    }
  },
  methods: {
    applyUniverse(universe) {
      this.universe = universe;

      const theme = (universe === "tech") ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", theme);

      localStorage.setItem("universe", universe);
      localStorage.setItem("theme", theme); // optionnel, si tu veux compat
    },
    toggleUniverse() {
      this.applyUniverse(this.universe === "tech" ? "life" : "tech");
    },
    handleKeydown(e) {
      // U = switch univers
      if (e.key && e.key.toLowerCase() === "u") this.toggleUniverse();
    }
  },
  mounted() {
    const saved = localStorage.getItem("universe");
    if (saved === "tech" || saved === "life") this.applyUniverse(saved);
    else this.applyUniverse("tech");

    window.addEventListener("keydown", this.handleKeydown);
  },
  beforeUnmount() {
    window.removeEventListener("keydown", this.handleKeydown);
  }
}).mount("#app");
