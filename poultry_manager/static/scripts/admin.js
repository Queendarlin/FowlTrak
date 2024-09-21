// Sidebar toggle event listener
const sidebarToggle = document.querySelector('#sidebar-toggle');
sidebarToggle.addEventListener('click', function () {
  document.querySelector('#sidebar').classList.toggle('collapsed');
  document.querySelector('.main').classList.toggle('collapsed');
});

// Sidebar active state for clicked items
document.querySelectorAll('.sidebar-link').forEach((link) => {
  link.addEventListener('click', function () {
    document.querySelectorAll('.sidebar-item').forEach((item) => {
      item.classList.remove('active');
    });
    this.parentElement.classList.add('active');
  });
});

// Theme toggle event listener
document.querySelector('.theme-toggle').addEventListener('click', () => {
  toggleRootClass();
  toggleLocalStorage();
});

function toggleRootClass() {
  const currentTheme = document.documentElement.getAttribute('data-bs-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-bs-theme', newTheme);
}

function toggleLocalStorage() {
  const currentTheme = document.documentElement.getAttribute('data-bs-theme');
  localStorage.setItem('theme', currentTheme);
}

// Load the theme from localStorage
(function loadThemeFromLocalStorage() {
  const storedTheme = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-bs-theme', storedTheme);
})();
