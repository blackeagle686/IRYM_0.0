  const themeStorageKey = 'preferredTheme';

  function setTheme(themeName) {
    const root = document.documentElement;

    // Remove all theme classes
    root.classList.remove('theme-dark', 'theme-light', 'theme-sunset', 'theme-berry');

    // Add the selected theme class
    root.classList.add(`theme-${themeName}`);

    // Save preference
    localStorage.setItem(themeStorageKey, themeName);
  }

  // Load theme on page load
  window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem(themeStorageKey) || 'dark';
    setTheme(savedTheme);
  });