(() => {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Header state on scroll */
  const header = document.querySelector("[data-header]");
  if (header) {
    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* Mobile navigation */
  const menuBtn = document.querySelector("[data-menu-btn]");
  const mobileNav = document.querySelector("[data-mobile-nav]");
  if (menuBtn && mobileNav) {
    const setOpen = (open) => {
      document.body.classList.toggle("nav-open", open);
      mobileNav.classList.toggle("is-open", open);
      menuBtn.setAttribute("aria-expanded", String(open));
    };
    menuBtn.addEventListener("click", () => {
      setOpen(!mobileNav.classList.contains("is-open"));
    });
    mobileNav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => setOpen(false));
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") setOpen(false);
    });
  }

  /* Scroll reveal */
  const revealEls = document.querySelectorAll("[data-reveal]");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealEls.forEach((el) => el.classList.add("is-in"));
  } else {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.16, rootMargin: "0px 0px -8% 0px" }
    );
    revealEls.forEach((el) => observer.observe(el));
  }

  /* Hero slideshow */
  const hero = document.querySelector("[data-hero]");
  if (hero) {
    const slides = Array.from(hero.querySelectorAll("[data-slide]"));
    const dots = Array.from(hero.querySelectorAll("[data-hero-dot]"));
    let index = 0;
    let timer = null;

    const show = (next) => {
      index = next;
      slides.forEach((slide, i) => slide.classList.toggle("is-active", i === next));
      dots.forEach((dot, i) => dot.classList.toggle("is-active", i === next));

      const image = slides[next].querySelector("img");
      if (image && !reduceMotion) {
        image.style.animation = "none";
        void image.offsetWidth;
        image.style.animation = "";
      }
    };

    const start = () => {
      if (reduceMotion || slides.length < 2 || timer) return;
      timer = window.setInterval(() => show((index + 1) % slides.length), 7000);
    };
    const stop = () => {
      window.clearInterval(timer);
      timer = null;
    };

    dots.forEach((dot, i) => {
      dot.addEventListener("click", () => {
        stop();
        show(i);
        start();
      });
    });

    hero.addEventListener("mouseenter", stop);
    hero.addEventListener("mouseleave", start);
    start();
  }

  /* Click-to-zoom with pan on the look page */
  document.querySelectorAll("[data-zoom]").forEach((stage) => {
    const image = stage.querySelector("img");
    if (!image) return;

    const toggle = () => {
      const zoomed = stage.classList.toggle("is-zoomed");
      stage.setAttribute("aria-pressed", String(zoomed));
      const hint = stage.querySelector(".zoom-hint");
      if (hint) hint.classList.toggle("is-hidden", zoomed);
      if (!zoomed) image.style.transformOrigin = "";
    };

    let startX = 0;
    let startY = 0;
    let moved = false;

    stage.addEventListener("click", () => {
      if (moved) {
        moved = false;
        return;
      }
      toggle();
    });
    stage.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        toggle();
      }
    });

    const pan = (event) => {
      if (!stage.classList.contains("is-zoomed")) return;
      const rect = stage.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width) * 100;
      const y = ((event.clientY - rect.top) / rect.height) * 100;
      image.style.transformOrigin = `${x}% ${y}%`;
    };

    let dragging = false;
    stage.addEventListener("pointerdown", (event) => {
      startX = event.clientX;
      startY = event.clientY;
      moved = false;
      if (event.pointerType === "mouse" || !stage.classList.contains("is-zoomed")) return;
      dragging = true;
      try {
        stage.setPointerCapture(event.pointerId);
      } catch (error) {
        /* pointer already released */
      }
    });
    stage.addEventListener("pointerup", () => {
      dragging = false;
    });
    stage.addEventListener("pointercancel", () => {
      dragging = false;
    });
    stage.addEventListener("pointermove", (event) => {
      if (event.pointerType === "mouse") {
        pan(event);
        return;
      }
      if (!dragging) return;
      if (Math.abs(event.clientX - startX) + Math.abs(event.clientY - startY) > 6) {
        moved = true;
      }
      if (moved) {
        event.preventDefault();
        pan(event);
      }
    });
  });

  /* Subtle parallax on the atelier image */
  const parallaxEls = document.querySelectorAll("[data-parallax]");
  if (parallaxEls.length && !reduceMotion) {
    let ticking = false;
    const update = () => {
      parallaxEls.forEach((el) => {
        const rect = el.parentElement.getBoundingClientRect();
        const offset = (rect.top + rect.height / 2 - window.innerHeight / 2) * -0.05;
        el.style.transform = `translateY(${offset.toFixed(2)}px) scale(1.06)`;
      });
      ticking = false;
    };
    const request = () => {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(update);
      }
    };
    update();
    window.addEventListener("scroll", request, { passive: true });
    window.addEventListener("resize", request);
  }
})();
