const toggleButton = document.getElementById("theme-toggle");
const themeStorageKey = "preferredTheme";

// Apply saved theme on load
function applyStoredTheme() {
  const saved = localStorage.getItem(themeStorageKey);
  if (saved === "light") {
    setLightTheme();
  } else {
    setDarkTheme(); // default
  }
}

function setLightTheme() {
  const link = document.getElementById("theme-css");
  link.setAttribute("href", link.dataset.light);
  localStorage.setItem(themeStorageKey, "light");
  toggleButton.innerText = "🌙 Switch to Dark";
}

function setDarkTheme() {
  const link = document.getElementById("theme-css");
  link.setAttribute("href", link.dataset.dark);
  localStorage.setItem(themeStorageKey, "dark");
  toggleButton.innerText = "☀️ Switch to Light";
}

if (toggleButton) {
  toggleButton.addEventListener("click", () => {
    const current = localStorage.getItem(themeStorageKey);
    if (current === "light") {
      setDarkTheme();
    } else {
      setLightTheme();
    }
  });

  applyStoredTheme();
}
