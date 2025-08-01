window.addEventListener("DOMContentLoaded", () => {
  const themeStorageKey = "preferredTheme";
  const themes = ["dark", "light", "sunset"];

  function setTheme(themeName) {
    const link = document.getElementById("theme-css");
    if (!link.dataset[themeName]) return;
    link.setAttribute("href", link.dataset[themeName] + "?v=" + new Date().getTime());
    localStorage.setItem(themeStorageKey, themeName);
  }

  function applyStoredTheme() {
    const saved = localStorage.getItem(themeStorageKey);
    if (themes.includes(saved)) {
      setTheme(saved);
    } else {
      setTheme("dark");
    }
  }

  applyStoredTheme();

  // الزر اللي بيبدل بين الثيمات
  const toggleButton = document.getElementById("theme-toggle");
  if (toggleButton) {
    toggleButton.addEventListener("click", () => {
      const current = localStorage.getItem(themeStorageKey) || "dark";
      const next = themes[(themes.indexOf(current) + 1) % themes.length];
      setTheme(next);
    });
  }

  // الأزرار الثلاثة المنفصلة (لو موجودة في sides.html)
  const btnDark = document.getElementById("set-dark");
  const btnLight = document.getElementById("set-light");
  const btnSunset = document.getElementById("set-sunset");

  if (btnDark) btnDark.addEventListener("click", () => setTheme("dark"));
  if (btnLight) btnLight.addEventListener("click", () => setTheme("light"));
  if (btnSunset) btnSunset.addEventListener("click", () => setTheme("sunset"));
});
