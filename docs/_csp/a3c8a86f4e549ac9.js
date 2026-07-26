
      (function() {
        const themeToggle = document.getElementById('themeToggle');
        function setTheme(theme) {
          document.documentElement.setAttribute('data-theme', theme);
          localStorage.setItem('theme', theme);
          themeToggle.textContent = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
        }
        const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        setTheme(savedTheme);
        themeToggle.addEventListener('click', function() {
          const current = document.documentElement.getAttribute('data-theme');
          setTheme(current === 'dark' ? 'light' : 'dark');
        });
      })();
    