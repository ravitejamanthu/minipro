(function () {
  try {
    if (location.pathname === '/') {
      var container = document.getElementById('back-to-home-container');
      if (container) container.style.display = 'none';
    }
  } catch (e) {}
})();

