/* SabahWebs - header, parallax hero, scroll reveal, mobile nav */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Sticky header state ---------- */
  var header = document.getElementById('header');
  function onScrollHeader() {
    if (window.scrollY > 24) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
  }

  /* ---------- Mobile nav ---------- */
  var toggle = document.getElementById('navToggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('menu-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    header.querySelectorAll('.nav-links a').forEach(function (a) {
      a.addEventListener('click', function () {
        header.classList.remove('menu-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- Parallax hero ---------- */
  var heroBg = document.getElementById('heroBg');
  var heroInner = document.getElementById('heroInner');
  var hero = document.getElementById('top');
  var ticking = false;

  function applyParallax() {
    var y = window.scrollY;
    var h = hero ? hero.offsetHeight : window.innerHeight;
    if (y <= h) {
      // background drifts slower than scroll (depth)
      if (heroBg) heroBg.style.transform = 'translate3d(0,' + (y * 0.4) + 'px,0)';
      // foreground copy lifts away + fades as you leave the hero
      if (heroInner) {
        heroInner.style.transform = 'translate3d(0,' + (y * 0.18) + 'px,0)';
        heroInner.style.opacity = Math.max(0, 1 - (y / (h * 0.7)));
      }
    }
    ticking = false;
  }

  function onScroll() {
    onScrollHeader();
    if (!reduceMotion && !ticking) {
      window.requestAnimationFrame(applyParallax);
      ticking = true;
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScrollHeader();
  if (!reduceMotion) applyParallax();

  /* ---------- Scroll reveal ---------- */
  var reveals = document.querySelectorAll('.reveal');
  if (reduceMotion || !('IntersectionObserver' in window)) {
    reveals.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  }
})();
