/* ============================================================
   MYIND SOUND — GHL Course Custom JavaScript
   Course: Suno Writer Neural Engine
   Paste into: Course → Details → Advanced → Custom Javascript
   ============================================================
   Light enhancements only — no destructive DOM rewriting.
   ============================================================ */

(function () {
  'use strict';

  // 1. Inject Inter font (Google Fonts is more reliable inside GHL than @import)
  if (!document.querySelector('link[href*="fonts.googleapis.com"][href*="Inter"]')) {
    var preconnect1 = document.createElement('link');
    preconnect1.rel = 'preconnect';
    preconnect1.href = 'https://fonts.googleapis.com';
    document.head.appendChild(preconnect1);

    var preconnect2 = document.createElement('link');
    preconnect2.rel = 'preconnect';
    preconnect2.href = 'https://fonts.gstatic.com';
    preconnect2.crossOrigin = 'anonymous';
    document.head.appendChild(preconnect2);

    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap';
    document.head.appendChild(link);
  }

  // 2. Tag the body so the CSS can scope brand overrides safely
  document.body.classList.add('myind-sound-course');

  // 3. Set the browser tab title to brand format
  function brandTitle() {
    var current = document.title || '';
    if (current.indexOf('Myind Sound') === -1) {
      document.title = current + ' — Myind Sound';
    }
  }
  brandTitle();

  // 4. Smooth-scroll to top when switching lessons
  function hookLessonClicks() {
    var items = document.querySelectorAll(
      '.lesson-item, .lesson-list-item, [class*="lesson-link"]'
    );
    items.forEach(function (el) {
      if (el.dataset.msHooked) return;
      el.dataset.msHooked = '1';
      el.addEventListener('click', function () {
        setTimeout(function () {
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }, 100);
      });
    });
  }

  // 5. Auto-uppercase main course title for brand voice
  function styleCourseTitle() {
    var title = document.querySelector(
      '.course-title, h1.course-name, h1[class*="course"]'
    );
    if (title && !title.dataset.msStyled) {
      title.dataset.msStyled = '1';
      title.style.textTransform = 'uppercase';
      title.style.letterSpacing = '0.5px';
    }
  }

  // 6. Re-run hooks when GHL injects content dynamically (SPA-style nav)
  var observer = new MutationObserver(function () {
    hookLessonClicks();
    styleCourseTitle();
    brandTitle();
  });

  function start() {
    hookLessonClicks();
    styleCourseTitle();
    observer.observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
