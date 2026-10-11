// VALTINSU homepage v3 prototype: nav menus, EM-5 model switcher, review notes toggle.
(function () {
  var nav = document.querySelector('.nav');
  var burger = document.querySelector('.nav__burger');
  var mobile = window.matchMedia('(max-width: 1024px)');

  burger.addEventListener('click', function () {
    var open = nav.classList.toggle('menu-open');
    burger.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });

  // Top-level items: on mobile, tap expands the submenu instead of following the link.
  document.querySelectorAll('.has-mega > .nav__top, .has-drop > .nav__top').forEach(function (a) {
    a.addEventListener('click', function (e) {
      if (!mobile.matches) return;
      e.preventDefault();
      a.parentElement.classList.toggle('open');
    });
  });

  // Language menu
  var lang = document.querySelector('.lang');
  var langBtn = lang.querySelector('.lang__btn');
  langBtn.addEventListener('click', function (e) {
    e.stopPropagation();
    langBtn.setAttribute('aria-expanded', lang.classList.toggle('open'));
  });
  document.addEventListener('click', function () {
    lang.classList.remove('open');
    langBtn.setAttribute('aria-expanded', 'false');
  });

  // EM-5 series tabs (instant spec switch, arrow keys move between models)
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.stab'));
  function select(tab) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on);
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
  }
  tabs.forEach(function (t, i) {
    t.tabIndex = t.getAttribute('aria-selected') === 'true' ? 0 : -1;
    t.addEventListener('click', function () { select(t); });
    t.addEventListener('keydown', function (e) {
      var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      var next = tabs[(i + d + tabs.length) % tabs.length];
      select(next); next.focus();
    });
  });

  // Review layer: module numbers match the homepage copy doc; blue dashed = waiting on client.
  var toggle = document.querySelector('.notes-toggle');
  function setNotes(on) {
    document.body.classList.toggle('notes', on);
    toggle.setAttribute('aria-pressed', on);
    toggle.textContent = on ? '隐藏标注' : '显示标注';
  }
  toggle.addEventListener('click', function () { setNotes(!document.body.classList.contains('notes')); });
  if (/[?&]notes=1/.test(location.search)) setNotes(true);
})();
