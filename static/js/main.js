document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav-links");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.textContent = open ? "×" : "☰";
    });
    nav.querySelectorAll("a").forEach(link => link.addEventListener("click", () => nav.classList.remove("open")));
  }

  const themeButton = document.querySelector(".theme-toggle");
  const savedTheme = localStorage.getItem("pjp-theme");
  if (savedTheme === "light") document.body.classList.add("light-theme");
  if (themeButton) themeButton.addEventListener("click", () => {
    document.body.classList.toggle("light-theme");
    localStorage.setItem("pjp-theme", document.body.classList.contains("light-theme") ? "light" : "dark");
  });

  const words = ["web applications", "useful software", "data-driven tools", "better experiences"];
  const target = document.getElementById("typed-word");
  if (target) {
    let wordIndex = 0, charIndex = 0, deleting = false;
    const type = () => {
      const word = words[wordIndex];
      target.textContent = word.substring(0, charIndex);
      if (!deleting && charIndex < word.length) { charIndex++; setTimeout(type, 75); }
      else if (deleting && charIndex > 0) { charIndex--; setTimeout(type, 35); }
      else { deleting = !deleting; if (!deleting) wordIndex = (wordIndex + 1) % words.length; setTimeout(type, 850); }
    };
    type();
  }

  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add("visible"); revealObserver.unobserve(entry.target); }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal, .skill-card").forEach(el => revealObserver.observe(el));

  document.querySelectorAll(".flash").forEach(el => setTimeout(() => el.classList.add("fade-out"), 4500));
});
