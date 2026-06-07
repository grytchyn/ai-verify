/**
 * draft.js — LocalStorage form cache + draft restore banner + toast notifications
 *
 * Public API:
 *   Draft.init({ formId, cacheKey, bannerId, saveBtnId, restoreBtnId, discardBtnId, getData, setData, getLang })
 *
 * Call Draft.init() once at page load after the form + banner HTML exist.
 *
 * The form data is read/written via the getData/setData callbacks (so the
 * caller can choose which fields to persist, e.g. exclude sensitive PII).
 */
(function(global) {
  'use strict';

  // ── TOAST ──
  let toastEl = null, toastTimer = null;
  function showToast(msg, type) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'toast';
      toastEl.setAttribute('role', 'status');
      toastEl.setAttribute('aria-live', 'polite');
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    toastEl.className = 'toast ' + (type || 'success');
    requestAnimationFrame(() => toastEl.classList.add('show'));
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.classList.remove('show'), 2400);
  }

  // ── MODULE STATE ──
  let cfg = null;

  function cache() {
    if (!cfg) return false;
    try {
      const data = cfg.getData();
      localStorage.setItem(cfg.cacheKey, JSON.stringify(data));
      return true;
    } catch(e) {
      console.warn('Draft.cache: storage failed', e);
      return false;
    }
  }

  function restore() {
    if (!cfg) return false;
    try {
      const raw = localStorage.getItem(cfg.cacheKey);
      if (!raw) return false;
      const data = JSON.parse(raw);
      cfg.setData(data);
      return true;
    } catch(e) {
      console.warn('Draft.restore: parse failed', e);
      return false;
    }
  }

  function clear() {
    if (!cfg) return;
    try { localStorage.removeItem(cfg.cacheKey); } catch(e) {}
  }

  function checkBanner() {
    if (!cfg) return;
    const banner = document.getElementById(cfg.bannerId);
    if (!banner) return;
    try {
      const raw = localStorage.getItem(cfg.cacheKey);
      if (!raw) return;
      const data = JSON.parse(raw);
      // Count filled fields — only show banner if there's meaningful data
      const filled = Object.values(data).filter(v =>
        v !== '' && v !== null && v !== undefined &&
        !(Array.isArray(v) && v.length === 0)
      ).length;
      if (filled < 2) return;

      // Update desc with field count
      const descEl = document.getElementById(cfg.bannerDescId);
      if (descEl) {
        const lang = cfg.getLang ? cfg.getLang() : 'en';
        const t = (global.translations || {})[lang] || {};
        const baseText = t.draftBannerDesc || 'We saved your form data from last time';
        const countText = (t.draftBannerCount || '{n} fields saved').replace('{n}', filled);
        descEl.textContent = baseText + ' (' + countText + ').';
      }
      banner.style.display = '';
    } catch(e) { /* ignore */ }
  }

  function hideBanner() {
    if (!cfg) return;
    const banner = document.getElementById(cfg.bannerId);
    if (banner) banner.style.display = 'none';
  }

  function t(key, fallback) {
    const lang = cfg && cfg.getLang ? cfg.getLang() : 'en';
    return (global.translations || {})[lang]?.[key] || fallback;
  }

  // ── INIT ──
  function init(opts) {
    cfg = Object.assign({
      formId: 'complianceForm',
      cacheKey: 'aiverify_form_data',
      bannerId: 'draftBanner',
      bannerDescId: 'draftBannerDesc',
      saveBtnId: 'saveDraftBtn',
      restoreBtnId: 'draftRestoreBtn',
      discardBtnId: 'draftDiscardBtn',
      getData: () => ({}),
      setData: () => {},
      getLang: () => 'en',
    }, opts);

    // Wire save button
    const saveBtn = document.getElementById(cfg.saveBtnId);
    if (saveBtn) {
      saveBtn.addEventListener('click', function() {
        if (cache()) showToast(t('toastDraftSaved', '✓ Draft saved'), 'success');
      });
    }

    // Wire restore button
    const restoreBtn = document.getElementById(cfg.restoreBtnId);
    if (restoreBtn) {
      restoreBtn.addEventListener('click', function() {
        if (restore()) {
          hideBanner();
          showToast(t('toastDraftRestored', '✓ Draft restored'), 'success');
        }
      });
    }

    // Wire discard button
    const discardBtn = document.getElementById(cfg.discardBtnId);
    if (discardBtn) {
      discardBtn.addEventListener('click', function() {
        clear();
        hideBanner();
        showToast(t('toastDraftDiscarded', '✕ Draft discarded'), 'error');
      });
    }

    // Show banner on load
    checkBanner();
  }

  global.Draft = { init, cache, restore, clear, checkBanner, showToast };
})(window);
