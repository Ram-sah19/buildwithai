/* ── main.js — Feastables Website Interactivity ── */

// ── Nav hide/show on scroll ──────────────────────────────────────────────────
const nav = document.getElementById('main-nav');
let lastScrollY = 0;
let navHidden = false;

window.addEventListener('scroll', () => {
  const currentY = window.scrollY;
  const delta = currentY - lastScrollY;

  if (currentY > 120) {
    if (delta > 4 && !navHidden) {
      nav.classList.add('nav--hidden');
      navHidden = true;
    } else if (delta < -4 && navHidden) {
      nav.classList.remove('nav--hidden');
      navHidden = false;
    }
  } else {
    nav.classList.remove('nav--hidden');
    navHidden = false;
  }
  lastScrollY = currentY;
}, { passive: true });

// ── Mobile drawer ────────────────────────────────────────────────────────────
const hamburger = document.getElementById('hamburger-btn');
const drawer = document.getElementById('mobile-drawer');
const mobileShopToggle = document.getElementById('mobile-shop-toggle');
const mobileShopSubmenu = document.getElementById('mobile-shop-submenu');

hamburger.addEventListener('click', () => {
  const isOpen = drawer.classList.toggle('open');
  hamburger.classList.toggle('open', isOpen);
  drawer.setAttribute('aria-hidden', String(!isOpen));
  document.body.style.overflow = isOpen ? 'hidden' : '';
});

if (mobileShopToggle && mobileShopSubmenu) {
  mobileShopToggle.addEventListener('click', () => {
    const hidden = mobileShopSubmenu.hidden;
    mobileShopSubmenu.hidden = !hidden;
    const chevron = mobileShopToggle.querySelector('.chevron');
    if (chevron) chevron.textContent = hidden ? '▴' : '▾';
  });
}

// Close drawer on link click
document.querySelectorAll('.mobile-drawer-item[href]').forEach(link => {
  link.addEventListener('click', () => {
    drawer.classList.remove('open');
    hamburger.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  });
});

// ── Shop dropdown ─────────────────────────────────────────────────────────────
const shopBtn = document.getElementById('shop-btn');
const shopPanel = document.getElementById('shop-panel');

if (shopBtn && shopPanel) {
  shopBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = shopPanel.classList.toggle('open');
    shopBtn.classList.toggle('open', isOpen);
    shopBtn.setAttribute('aria-expanded', String(isOpen));
    shopPanel.setAttribute('aria-hidden', String(!isOpen));
  });

  document.addEventListener('click', (e) => {
    if (!shopBtn.contains(e.target) && !shopPanel.contains(e.target)) {
      shopPanel.classList.remove('open');
      shopBtn.classList.remove('open');
      shopBtn.setAttribute('aria-expanded', 'false');
      shopPanel.setAttribute('aria-hidden', 'true');
    }
  });

  // Keyboard close
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      shopPanel.classList.remove('open');
      shopBtn.classList.remove('open');
      shopBtn.setAttribute('aria-expanded', 'false');
      shopPanel.setAttribute('aria-hidden', 'true');
      shopBtn.focus();
    }
  });
}

// ── Announcement modal ────────────────────────────────────────────────────────
const announcementTrigger = document.getElementById('announcement-trigger');
const modalBackdrop = document.getElementById('modal-backdrop');
const modalClose = document.getElementById('modal-close');

if (announcementTrigger && modalBackdrop) {
  announcementTrigger.addEventListener('click', (e) => {
    e.preventDefault();
    modalBackdrop.classList.add('open');
    modalBackdrop.setAttribute('aria-hidden', 'false');
    modalClose.focus();
  });

  const closeModal = () => {
    modalBackdrop.classList.remove('open');
    modalBackdrop.setAttribute('aria-hidden', 'true');
    announcementTrigger.focus();
  };

  if (modalClose) modalClose.addEventListener('click', closeModal);
  modalBackdrop.addEventListener('click', (e) => {
    if (e.target === modalBackdrop) closeModal();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalBackdrop.classList.contains('open')) closeModal();
  });
}

// ── Cart / Add to Bag ────────────────────────────────────────────────────────
let cartCount = 0;
const cartCountEl = document.getElementById('cart-count');
const toast = document.getElementById('toast');
let toastTimer;

function showToast(msg) {
  if (!toast) return;
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2800);
}

document.querySelectorAll('.product-atb').forEach(btn => {
  btn.addEventListener('click', () => {
    const name = btn.getAttribute('data-product') || 'item';
    cartCount++;
    if (cartCountEl) cartCountEl.textContent = cartCount;
    showToast(`✓ ${name.toUpperCase()} ADDED TO BAG`);

    // Pulse animation on button
    btn.style.transform = 'scale(0.94)';
    setTimeout(() => { btn.style.transform = ''; }, 150);
  });
});

// ── Intersection Observer — scroll animations ─────────────────────────────────
const animateEls = document.querySelectorAll('[data-animate]');
const fadeCards = document.querySelectorAll('.product-card');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const el = entry.target;
      const delay = el.getAttribute('data-delay') || 0;
      setTimeout(() => el.classList.add('animated'), Number(delay));
      observer.unobserve(el);
    }
  });
}, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });

animateEls.forEach(el => observer.observe(el));

const cardObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const el = entry.target;
      const delay = el.getAttribute('data-delay') || 0;
      setTimeout(() => el.classList.add('visible'), Number(delay));
      cardObserver.unobserve(el);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

fadeCards.forEach(card => cardObserver.observe(card));

// ── Smooth scroll for anchor links ──────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', (e) => {
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const offset = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--nav-h')) || 75;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});
