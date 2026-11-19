// 旅のしおり：楽しいUIアニメーション（スクロール登場・進捗バイク・波紋・火花・紙吹雪・トップへ戻る）
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) return;

  var hasIO = 'IntersectionObserver' in window;

  /* ── ヒーロー登場 ── */
  var hero = document.querySelector('.hero');
  if (hero) hero.classList.add('anim-hero');

  /* ── スクロール連動の登場 ── */
  var REVEAL = [
    ['.section-head, .section-title, .page-banner h1, .page-banner p', ''],
    ['.card, .hl-card, .hotel-card, .goods-card, .quick-link-card, .info-card, .sns-card, .spot-card, .emg-card, .guide-contact-card, .vehicle-card', 'anim-zoom'],
    ['.pt-photo-card, .pt-video-card, .pt-nexttour-card, .include-box, .checklist-box, .step-item, .cl-item, .shuttle-block', 'anim-zoom'],
    ['.ticket-card, .customer-banner, .greeting-box, .progress-panel, .alert, .company-table, .map-wrap, .meeting-map-block', ''],
    ['.day-strip, .acc-item, #faqList > div, .pt-album-btn', ''],
    ['.tl-item', 'anim-left']
  ];
  var io = hasIO ? new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('anim-in');
      io.unobserve(e.target);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }) : null;

  function prepare(root) {
    if (!io) return;
    REVEAL.forEach(function (pair) {
      var els;
      try { els = root.querySelectorAll(pair[0]); } catch (e) { return; }
      Array.prototype.forEach.call(els, function (el) {
        if (el.dataset.animDone || el.closest('.ticket-modal, .anim-top, header, .site-header, .mobile-nav, .hero')) return;
        el.dataset.animDone = '1';
        var rect = el.getBoundingClientRect();
        // 兄弟要素の順番で時間差（最大6つ目まで）
        var idx = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
        el.style.setProperty('--anim-delay', Math.min(idx, 6) * 80 + 'ms');
        if (pair[1]) el.classList.add(pair[1]);
        el.classList.add('anim-pre');
        if (rect.top < window.innerHeight && rect.bottom > 0) {
          setTimeout(function () { el.classList.add('anim-in'); }, 40);
        } else {
          io.observe(el);
        }
      });
    });
  }
  prepare(document);
  // JSで後から描画される内容（言語切替・データ描画）にも適用
  var mo = new MutationObserver(function (muts) {
    var need = false;
    muts.forEach(function (m) { if (m.addedNodes.length) need = true; });
    if (need) { clearTimeout(mo._t); mo._t = setTimeout(function () { prepare(document); }, 60); }
  });
  mo.observe(document.body, { childList: true, subtree: true });

  /* ── スクロール進捗バー（バイクが走る） ── */
  var prog = document.createElement('div');
  prog.className = 'anim-progress';
  prog.innerHTML = '<div class="anim-progress-bar"></div><i class="fa-solid fa-motorcycle anim-progress-rider"></i>';
  document.body.appendChild(prog);
  var bar = prog.firstChild, rider = prog.lastChild;

  /* ── トップへ戻るボタン ── */
  var top = document.createElement('button');
  top.type = 'button';
  top.className = 'anim-top';
  top.setAttribute('aria-label', 'Top');
  top.innerHTML = '<i class="fa-solid fa-chevron-up"></i>';
  top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  document.body.appendChild(top);

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    setTimeout(function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var p = h > 0 ? Math.min(100, Math.max(0, (window.scrollY / h) * 100)) : 0;
      bar.style.width = p + '%';
      rider.style.left = p + '%';
      top.classList.toggle('show', window.scrollY > 500);
      ticking = false;
    }, 16);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ── クリック：波紋（ボタン）＋火花（どこでも） ── */
  var RIPPLE_SEL = '.btn-nav, .pt-album-btn, .hotel-official-btn, .tl-streetview-btn, .lang-switch-btn, .pt-nexttour-btn, .print-save-btn';
  var COLORS = ['#ed1b23', '#ff8a3d', '#ffd23f', '#ffffff', '#9e1016'];
  document.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest(RIPPLE_SEL);
    if (btn) {
      var r = btn.getBoundingClientRect();
      var s = document.createElement('span');
      s.className = 'anim-ripple';
      s.style.left = (e.clientX - r.left) + 'px';
      s.style.top = (e.clientY - r.top) + 'px';
      btn.appendChild(s);
      setTimeout(function () { s.remove(); }, 650);
    }
    for (var i = 0; i < 8; i++) {
      var sp = document.createElement('span');
      sp.className = 'anim-spark';
      var a = (Math.PI * 2 * i) / 8 + Math.random() * 0.5, d = 26 + Math.random() * 22;
      sp.style.left = e.clientX + 'px';
      sp.style.top = e.clientY + 'px';
      sp.style.background = COLORS[i % COLORS.length];
      sp.style.setProperty('--sx', Math.cos(a) * d + 'px');
      sp.style.setProperty('--sy', Math.sin(a) * d + 'px');
      document.body.appendChild(sp);
      setTimeout((function (n) { return function () { n.remove(); }; })(sp), 700);
    }
  }, true);

  /* ── 紙吹雪（window.animConfetti() で呼び出し可） ── */
  window.animConfetti = function () {
    for (var i = 0; i < 70; i++) {
      var c = document.createElement('span');
      c.className = 'anim-confetti';
      c.style.left = Math.random() * 100 + 'vw';
      c.style.background = COLORS[i % COLORS.length];
      c.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
      c.style.setProperty('--cx', (Math.random() * 200 - 100) + 'px');
      c.style.setProperty('--cr', (Math.random() * 900 - 450) + 'deg');
      c.style.setProperty('--cd', (2.2 + Math.random() * 1.8) + 's');
      c.style.animationDelay = Math.random() * 0.6 + 's';
      document.body.appendChild(c);
      setTimeout((function (n) { return function () { n.remove(); }; })(c), 4800);
    }
  };

  // チェックリストが100%になったとき（caution.html）にお祝い
  var ring = document.getElementById('ringPercent');
  if (ring) {
    var done = false;
    new MutationObserver(function () {
      var v = parseInt(ring.textContent, 10);
      if (v === 100 && !done) { done = true; window.animConfetti(); }
      if (v < 100) done = false;
    }).observe(ring, { childList: true, characterData: true, subtree: true });
  }

  /* ── ヒーローのパララックス風の軽い傾き（PCのみ） ── */
  var tilt = document.querySelector('.ticket-card:not(.ticket-card-lg)');
  if (tilt && window.matchMedia('(hover: hover)').matches) {
    tilt.addEventListener('mousemove', function (e) {
      var r = tilt.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
      tilt.style.transform = 'perspective(800px) rotateY(' + x * 7 + 'deg) rotateX(' + -y * 7 + 'deg) translateY(-3px)';
    });
    tilt.addEventListener('mouseleave', function () { tilt.style.transform = ''; });
  }

  /* ════════════ 第2弾 ════════════ */
  var tick = function (ms, fn) { // rAFに依存しないタイマー駆動のトゥイーン
    var t0 = Date.now();
    var h = setInterval(function () {
      var p = Math.min(1, (Date.now() - t0) / ms);
      fn(1 - Math.pow(1 - p, 3));
      if (p >= 1) clearInterval(h);
    }, 16);
  };

  /* 1・4. ヒーロー：バイクが走り抜ける＋ふわふわ装飾 */
  if (hero) {
    var pass = document.createElement('i');
    pass.className = 'fa-solid fa-motorcycle anim-rider-pass';
    hero.appendChild(pass);
    setTimeout(function () { pass.remove(); }, 5000);

    var deco = document.createElement('div');
    deco.className = 'anim-deco';
    var ICONS = ['fa-star', 'fa-cloud', 'fa-leaf', 'fa-sun', 'fa-star', 'fa-heart'];
    for (var i = 0; i < 14; i++) {
      var ic = document.createElement('i');
      ic.className = 'fa-solid ' + ICONS[i % ICONS.length];
      ic.style.left = (4 + (i * 97) % 92) + '%';
      ic.style.setProperty('--ds', (10 + (i * 7) % 18) + 'px');
      ic.style.setProperty('--dd', (9 + (i * 5) % 9) + 's');
      ic.style.setProperty('--dl', (-(i * 1.7)) + 's');
      ic.style.setProperty('--dx', ((i % 2 ? 1 : -1) * (20 + (i * 11) % 50)) + 'px');
      ic.style.setProperty('--do', (0.25 + (i % 4) * 0.1).toFixed(2));
      deco.appendChild(ic);
    }
    hero.insertBefore(deco, hero.firstChild.nextSibling);

    /* 3. タイトルを1文字ずつ跳ねさせる */
    var h1 = hero.querySelector('h1');
    if (h1 && !h1.querySelector('.anim-char')) {
      var n = 0;
      var splitNode = function (node) {
        Array.prototype.slice.call(node.childNodes).forEach(function (c) {
          if (c.nodeType === 3) {
            var frag = document.createDocumentFragment();
            c.textContent.split(/(\s+)/).forEach(function (w) {
              if (!w) return;
              if (/^\s+$/.test(w)) { frag.appendChild(document.createTextNode(' ')); return; }
              var word = document.createElement('span');
              word.className = 'anim-word';
              Array.from(w).forEach(function (ch) {
                var s = document.createElement('span');
                s.className = 'anim-char';
                s.style.setProperty('--ci', n++);
                s.textContent = ch;
                word.appendChild(s);
              });
              frag.appendChild(word);
            });
            node.replaceChild(frag, c);
          } else if (c.nodeType === 1) { splitNode(c); }
        });
      };
      var titleText = h1.textContent;
      splitNode(h1);
      h1.setAttribute('aria-label', titleText);
      h1.classList.add('anim-split');
    }
  }

  /* 2. 数字のカウントアップ（出発までの日数・グッズ価格） */
  var counted = [];
  function countUp(el) {
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    var node;
    while ((node = walker.nextNode())) {
      var m = /\d[\d,]*/.exec(node.nodeValue);
      if (!m) continue;
      var target = parseInt(m[0].replace(/,/g, ''), 10);
      if (!target) return;
      var comma = m[0].indexOf(',') >= 0;
      var before = node.nodeValue.slice(0, m.index);
      var after = node.nodeValue.slice(m.index + m[0].length);
      tick(1400, function (p) {
        var v = Math.round(target * p);
        node.nodeValue = before + (comma ? v.toLocaleString('en-US') : v) + after;
      });
      return;
    }
  }
  window.animCountUp = countUp;
  var cio = hasIO ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { cio.unobserve(e.target); countUp(e.target); } });
  }, { threshold: 0.6 }) : null;
  function scanCounts() {
    if (!cio) return;
    Array.prototype.forEach.call(document.querySelectorAll('.countdown-badge, .goods-price'), function (el) {
      if (counted.indexOf(el) >= 0) return;
      counted.push(el);
      cio.observe(el);
    });
  }
  scanCounts();
  new MutationObserver(function () { clearTimeout(scanCounts._t); scanCounts._t = setTimeout(scanCounts, 80); }).observe(document.body, { childList: true, subtree: true });

  /* 5. タイムラインの線が伸びる */
  var lio = hasIO ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('anim-line-in'); lio.unobserve(e.target); } });
  }, { threshold: 0.05 }) : null;
  function scanLines() {
    if (!lio) return;
    Array.prototype.forEach.call(document.querySelectorAll('.timeline:not(.anim-line)'), function (el) {
      el.classList.add('anim-line');
      lio.observe(el);
    });
  }
  scanLines();
  new MutationObserver(function () { clearTimeout(scanLines._t); scanLines._t = setTimeout(scanLines, 80); }).observe(document.body, { childList: true, subtree: true });

  /* 6. チェックを入れたときの演出（星が飛び散る） */
  document.addEventListener('click', function (e) {
    var li = e.target.closest && e.target.closest('.cl-item[data-ci]');
    if (!li) return;
    var ci = li.getAttribute('data-ci'), ii = li.getAttribute('data-ii');
    setTimeout(function () {
      var cur = document.querySelector('.cl-item[data-ci="' + ci + '"][data-ii="' + ii + '"]');
      if (!cur || !cur.classList.contains('checked')) return;
      cur.classList.remove('anim-just-checked');
      void cur.offsetWidth;
      cur.classList.add('anim-just-checked');
      var chk = cur.querySelector('.cl-check');
      var r = (chk || cur).getBoundingClientRect();
      for (var i = 0; i < 7; i++) {
        var s = document.createElement('i');
        s.className = 'fa-solid fa-star anim-star';
        var a = (Math.PI * 2 * i) / 7, d = 30 + Math.random() * 18;
        s.style.left = (r.left + r.width / 2) + 'px';
        s.style.top = (r.top + r.height / 2) + 'px';
        s.style.setProperty('--sx', Math.cos(a) * d + 'px');
        s.style.setProperty('--sy', Math.sin(a) * d + 'px');
        document.body.appendChild(s);
        setTimeout((function (x) { return function () { x.remove(); }; })(s), 850);
      }
    }, 40);
  });

  /* 7・9. ページ移動／言語切替のトランジション */
  window.addEventListener('pageshow', function () { document.body.classList.remove('anim-leave', 'anim-lang-out'); });
  try {
    if (sessionStorage.getItem('animLang')) {
      sessionStorage.removeItem('animLang');
      document.body.classList.add('anim-lang-in');
      setTimeout(function () { document.body.classList.remove('anim-lang-in'); }, 1200);
    }
  } catch (err) {}
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var lb = e.target.closest && e.target.closest('.lang-switch-btn[data-lang]');
    if (lb) {
      if (lb.classList.contains('active')) return;
      e.stopPropagation();
      e.preventDefault();
      try { sessionStorage.setItem('animLang', '1'); } catch (err) {}
      document.body.classList.add('anim-lang-out');
      var code = lb.getAttribute('data-lang');
      setTimeout(function () { if (typeof setLang === 'function') setLang(code); }, 220);
      return;
    }
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || a.target === '_blank' || a.hasAttribute('download')) return;
    var href = a.getAttribute('href');
    if (!href || href.charAt(0) === '#' || /^(mailto:|tel:|javascript:)/i.test(href)) return;
    var url;
    try { url = new URL(a.href, location.href); } catch (err) { return; }
    if (url.origin !== location.origin || url.pathname === location.pathname) return;
    e.preventDefault();
    document.body.classList.add('anim-leave');
    setTimeout(function () { location.href = url.href; }, 260);
  }, true);
})();
