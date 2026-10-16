/* Optional progressive enhancement; all content remains readable without JS. */
(() => {
  const meter = document.getElementById('read-progress');
  const update = () => {
    if (!meter) return;
    const range = document.documentElement.scrollHeight - window.innerHeight;
    const fraction = range > 0 ? window.scrollY / range : 1;
    meter.style.width = Math.max(0, Math.min(100, fraction * 100)).toFixed(1) + '%';
  };
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update, { passive: true });
  update();
  for (const button of document.querySelectorAll('[data-action="print"]')) {
    button.addEventListener('click', () => window.print());
  }
})();