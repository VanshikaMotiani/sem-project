// Accessibility & interactive UI helpers for Nagar Nigam Portal
(function () {
  let fontScale = parseFloat(localStorage.getItem("nn_font_scale") || "1");
  document.documentElement.style.setProperty("--font-scale", fontScale);

  if (localStorage.getItem("nn_contrast") === "dark") {
    document.body.classList.add("high-contrast");
  }

  window.adjustFont = function (delta) {
    if (delta === 0) {
      fontScale = 1;
    } else {
      fontScale = Math.min(1.25, Math.max(0.85, +(fontScale + delta).toFixed(2)));
    }
    localStorage.setItem("nn_font_scale", fontScale);
    document.documentElement.style.setProperty("--font-scale", fontScale);
  };

  window.setThemeMode = function (mode) {
    if (mode === "dark") {
      document.body.classList.add("high-contrast");
      localStorage.setItem("nn_contrast", "dark");
    } else {
      document.body.classList.remove("high-contrast");
      localStorage.setItem("nn_contrast", "light");
    }
  };

  const scrollBtn = document.getElementById("scrollTopBtn");
  if (scrollBtn) {
    window.addEventListener("scroll", function () {
      scrollBtn.style.display = window.scrollY > 260 ? "flex" : "none";
    });
    scrollBtn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }
})();
