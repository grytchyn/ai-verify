/**
 * auto-detect.js — Auto-fill company info from URL via /analyze-url
 *
 * Public API:
 *   AutoDetect.init({
 *     urlInputName,         // Form field name to watch (default 'url')
 *     fieldMap,             // { company: 'company', sector: 'sector', hq_location: 'hq_location' }
 *     debounceMs,           // (default 800)
 *     choicesInstances,     // Choices.js instances to update (for styled selects)
 *     onFill,               // optional callback (data) => void
 *   })
 *
 * Listens to 'input' and 'change' on the URL field, debounces,
 * calls /analyze-url?url=... and fills the mapped fields. Skips fields
 * that are already user-edited (won't overwrite manual input).
 */
(function(global) {
  'use strict';

  let cfg = null;
  let timer = null;

  function init(opts) {
    cfg = Object.assign({
      urlInputName: 'url',
      fieldMap: { company: 'company', sector: 'sector', hq_location: 'hq_location' },
      debounceMs: 800,
      choicesInstances: null,  // deprecated — use getChoices
      getChoices: null,         // () => ChoicesInstance[]
      onFill: null,
    }, opts);

    // Normalize: if getChoices provided, use it; else fall back to static array
    if (!cfg.getChoices && cfg.choicesInstances) {
      cfg.getChoices = () => cfg.choicesInstances || [];
    }
    if (!cfg.getChoices) cfg.getChoices = () => [];

    // Initial run if URL already filled (e.g. restored from cache)
    setTimeout(trigger, 300);

    // Listen for changes
    document.addEventListener('input', function(e) {
      if (e.target && e.target.name === cfg.urlInputName) trigger();
    });
    document.addEventListener('change', function(e) {
      if (e.target && e.target.name === cfg.urlInputName) trigger();
    });
  }

  function trigger() {
    clearTimeout(timer);
    const urlInput = document.querySelector('[name="' + cfg.urlInputName + '"]');
    const url = urlInput ? urlInput.value.trim() : '';
    if (!url) return;
    timer = setTimeout(() => detect(url), cfg.debounceMs);
  }

  async function detect(url) {
    const spinner = document.getElementById('urlDetectSpinner');
    if (spinner) spinner.style.display = 'block';

    // Don't overwrite if company already filled manually
    const companyInput = document.querySelector('[name="' + cfg.fieldMap.company + '"]');
    if (companyInput && companyInput.value.trim()) {
      if (spinner) spinner.style.display = 'none';
      return;
    }

    try {
      const resp = await fetch('/analyze-url?url=' + encodeURIComponent(url));
      if (!resp.ok) throw new Error('HTTP ' + resp.status);
      const data = await resp.json();

      fillField(cfg.fieldMap.company, data.company_name, { text: true });
      fillField(cfg.fieldMap.sector, data.sector, { match: 'text-or-value' });
      fillField(cfg.fieldMap.hq_location, data.hq_location, { match: 'text-or-value' });

      if (cfg.onFill) cfg.onFill(data);
      // Trigger form cache to persist auto-filled values
      if (typeof cacheFormData === 'function') cacheFormData();
    } catch (e) {
      // Silent fail — form still works manually
      console.warn('[AutoDetect] failed:', e.message);
    } finally {
      if (spinner) spinner.style.display = 'none';
    }
  }

  function fillField(name, value, opts) {
    if (!value) return;
    const el = document.querySelector('[name="' + name + '"]');
    if (!el) return;

    if (opts.text) {
      el.value = value;
      flashSuccess(el);
      return;
    }

    if (opts.match === 'text-or-value') {
      const needle = String(value).toLowerCase();
      const matchedOpt = Array.from(el.options || []).find(opt =>
        opt.value.toLowerCase() === needle ||
        opt.text.toLowerCase().includes(needle)
      );
      if (matchedOpt) {
        el.value = matchedOpt.value;
        // Update Choices.js display if styled
        (cfg.getChoices() || []).forEach(c => {
          try { c.setChoiceByValue(matchedOpt.value); } catch(e) {}
        });
        flashSuccess(el);
      }
    }
  }

  function flashSuccess(el) {
    el.classList.add('auto-detect-success');
    setTimeout(() => el.classList.remove('auto-detect-success'), 2000);
  }

  global.AutoDetect = { init, detect };
})(window);
