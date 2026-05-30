/* ── dashboard.js ── */

// ── Sidebar active link on scroll ────────────────────────────────────────────
const sections = document.querySelectorAll('.dash-section');
const sidebarLinks = document.querySelectorAll('.sidebar-link');

const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.getAttribute('id');
      sidebarLinks.forEach(link => {
        link.classList.toggle('sidebar-link--active', link.getAttribute('href') === `#${id}`);
      });
    }
  });
}, { rootMargin: '-30% 0px -60% 0px', threshold: 0 });

sections.forEach(s => sectionObserver.observe(s));

// ── Color swatch copy ────────────────────────────────────────────────────────
const copyToast = document.getElementById('copy-toast');
let toastTimer;

document.querySelectorAll('.color-swatch').forEach(swatch => {
  swatch.addEventListener('click', () => {
    const hex = swatch.getAttribute('data-copy');
    if (!hex) return;

    navigator.clipboard.writeText(hex).then(() => {
      if (copyToast) {
        copyToast.textContent = `Copied ${hex}!`;
        copyToast.classList.add('show');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => copyToast.classList.remove('show'), 2000);
      }
    }).catch(() => {
      // Fallback
      const el = document.createElement('textarea');
      el.value = hex;
      el.style.position = 'fixed';
      el.style.opacity = '0';
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);

      if (copyToast) {
        copyToast.textContent = `Copied ${hex}!`;
        copyToast.classList.add('show');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => copyToast.classList.remove('show'), 2000);
      }
    });
  });

  // Keyboard support
  swatch.setAttribute('tabindex', '0');
  swatch.setAttribute('role', 'button');
  swatch.setAttribute('aria-label', `Copy color ${swatch.getAttribute('data-copy')}`);
  swatch.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      swatch.click();
    }
  });
});

// ── CSS copy button ──────────────────────────────────────────────────────────
const cssCopyBtn = document.getElementById('css-copy-btn');
const cssCode = document.getElementById('css-code');

if (cssCopyBtn && cssCode) {
  cssCopyBtn.addEventListener('click', () => {
    const text = cssCode.textContent;
    navigator.clipboard.writeText(text).then(() => {
      cssCopyBtn.textContent = 'COPIED!';
      cssCopyBtn.style.background = '#000';
      cssCopyBtn.style.color = '#15CCFF';
      setTimeout(() => {
        cssCopyBtn.textContent = 'COPY';
        cssCopyBtn.style.background = '';
        cssCopyBtn.style.color = '';
      }, 2000);
    }).catch(() => {
      cssCopyBtn.textContent = 'COPY FAILED';
      setTimeout(() => { cssCopyBtn.textContent = 'COPY'; }, 2000);
    });
  });
}

// ── Smooth scroll for sidebar links ──────────────────────────────────────────
document.querySelectorAll('.sidebar-link').forEach(link => {
  link.addEventListener('click', (e) => {
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
