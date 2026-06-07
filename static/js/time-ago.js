/**
 * time-ago.js — Live "X ago" indicator (trust signal on result page)
 *
 * Public API:
 *   TimeAgo.start(targetElId, createdAtIso, { lang, locale, onTick })
 *   TimeAgo.stop()
 *
 * Updates the target element's text content with a " · X ago" suffix that
 * re-renders every 30 seconds. Uses translations[lang].age* keys.
 */
(function(global) {
  'use strict';

  let intervalId = null;
  let currentEl = null;

  function t(lang, key, fallback) {
    return (global.translations || {})[lang]?.[key] || fallback;
  }

  function fmtAge(secs, lang) {
    if (secs < 60) return t(lang, 'ageSeconds', 'just now');
    const mins = Math.floor(secs / 60);
    if (mins < 60) return t(lang, 'ageMinutes', mins + ' min ago').replace('{n}', mins);
    const hours = Math.floor(mins / 60);
    if (hours < 24) return t(lang, 'ageHours', hours + 'h ago').replace('{n}', hours);
    const days = Math.floor(hours / 24);
    return t(lang, 'ageDays', days + 'd ago').replace('{n}', days);
  }

  function start(elId, createdAtIso, opts) {
    opts = opts || {};
    stop();
    const el = document.getElementById(elId);
    if (!el) return;
    currentEl = el;

    // Backend may return ISO with or without 'Z' suffix
    const iso = createdAtIso.endsWith('Z') ? createdAtIso : createdAtIso + 'Z';
    const createdAt = new Date(iso);
    if (isNaN(createdAt.getTime())) return;

    const lang = opts.lang || 'en';

    function update() {
      const secs = Math.floor((Date.now() - createdAt.getTime()) / 1000);
      el.textContent = ' · ' + fmtAge(secs, lang);
      if (opts.onTick) opts.onTick(secs);
    }
    update();
    // 30s tick — sufficient for human-perceived freshness, no battery drain
    intervalId = setInterval(update, 30000);
  }

  function stop() {
    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }
    currentEl = null;
  }

  // Clean up on page unload to prevent memory leaks
  if (global.addEventListener) {
    global.addEventListener('beforeunload', stop);
  }

  global.TimeAgo = { start, stop, fmtAge };
})(window);
