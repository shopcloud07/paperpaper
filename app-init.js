/*!
 * app-init.js — bootstrap da aplicacao
 * Inicializa a stack de analytics e atribuicao nos ambientes autorizados.
 * build 1.0.0
 */
(function (w, d) {
  'use strict';

  if (w.__appInit) { return; }
  w.__appInit = 1;

  /* ==========================================================================
   *  CONFIG
   *  Unica secao que muda de projeto para projeto.
   *  Nada abaixo desta secao precisa ser editado.
   * ========================================================================== */

  var CFG = {

    /* Ambientes de producao. Fora desta lista nada e carregado.
       Liste apenas dominios exatos.
       O coringa '*' cobre um unico rotulo e serve para subdominio proprio
       ('*.seudominio.com.br'). Nunca use coringa em host compartilhado
       como '*.vercel.app': isso autoriza a hospedagem inteira.               */
    envs: ['paperprime.vercel.app'],

    /* Hosts de desenvolvimento. So valem com debug ligado.                   */
    devEnvs: ['localhost', '127.0.0.1'],

    /* Bloqueia execucao quando a pagina esta embutida em iframe de
       origem diferente. Deixe true apenas se precisar rodar em iframe.       */
    allowFrame: false,

    /* UTMify
       pixel: vazio = nao carrega.
       Valor iniciado por '~' e resolvido em runtime usando o host atual
       como chave — so abre no dominio para o qual foi gerado.
       Aceita array quando existe mais de um dominio de producao.
       Ver COFRE-LEIA-ME.md para gerar o valor.                               */
    utmify: {
      utms:  true,
      pixel: '~QRIRUxpHRhVbBE8SU0ZSVFlKU0gWQ1JIU0NFFA9VVRg=',
      src:   'https://cdn.utmify.com.br/scripts/pixel/pixel.js',
      attrs: []
    },

    /* Microsoft Clarity — id ou '' para desligar                             */
    clarity: '~QQtGVAQdEBUYEx0RH0YBVAZU',

    /* Dominios de checkout que recebem os parametros de origem               */
    checkouts: ['tilimcheckout.com'],

    /* Parametros capturados e persistidos                                    */
    utmKeys: ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'utm_id', 'src'],

    /* Marcacao de acesso direto em desktop                                   */
    deskTag: { on: true, source: 'dir', campaign: '_desk' },

    /* Endpoint de configuracao remota. Ex: '/api/config'.
       Quando preenchido, os valores retornados sobrescrevem os locais.       */
    remote: '',

    storeKey: 'pp_utms',

    /* true = loga o diagnostico no console. Sempre false em producao.        */
    debug: false
  };

  /* ==========================================================================
   *  RUNTIME — nao editar
   * ========================================================================== */

  function log() {
    if (!CFG.debug || !w.console) { return; }
    try { console.log.apply(console, ['[init]'].concat([].slice.call(arguments))); } catch (e) {}
  }

  function norm(h) {
    return String(h || '').toLowerCase().replace(/^www\./, '');
  }

  function currentHost() {
    try { return norm(w.location.hostname); } catch (e) { return ''; }
  }

  function envMatch(h) {
    if (!h) { return false; }

    var list = CFG.envs.slice();
    if (CFG.debug && CFG.devEnvs) { list = list.concat(CFG.devEnvs); }

    for (var i = 0; i < list.length; i++) {
      var e = norm(list[i]);
      if (!e) { continue; }

      if (e.indexOf('*') !== -1) {
        /* coringa cobre um unico rotulo — nao atravessa ponto */
        var rx = new RegExp('^' + e.replace(/[.+?^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '[a-z0-9-]*') + '$');
        if (rx.test(h)) { return true; }
      } else if (h === e) {
        return true;
      }
    }
    return false;
  }

  function framedElsewhere() {
    if (CFG.allowFrame) { return false; }
    try {
      if (w.top === w.self) { return false; }
      return norm(w.top.location.hostname) !== currentHost();
    } catch (e) {
      return true;
    }
  }

  /* --- resolucao de valores atrelados ao ambiente -------------------------- */

  function mix(s, k) {
    var o = '', i;
    for (i = 0; i < s.length; i++) {
      o += String.fromCharCode(s.charCodeAt(i) ^ k.charCodeAt(i % k.length));
    }
    return o;
  }

  /* Assinatura curta do conteudo (FNV-1a). Vai junto dentro do valor e e
     conferida na leitura: chave errada = assinatura nao bate = descarta.
     Sem isso, uma chave parecida devolvia um conteudo parecido.             */
  function sum(s) {
    var h = 2166136261, i;
    for (i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h = (h + (h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24)) >>> 0;
    }
    return h.toString(36);
  }

  function pack(plain, key) {
    try {
      var p = String(plain);
      return '~' + w.btoa(mix(sum(p) + '|' + p, norm(key || currentHost())));
    } catch (e) { return ''; }
  }

  function unpack(v, key) {
    try {
      var raw = mix(w.atob(String(v).slice(1)), norm(key || currentHost()));
      var i = raw.indexOf('|');
      if (i < 1) { return ''; }
      var p = raw.slice(i + 1);
      return sum(p) === raw.slice(0, i) ? p : '';
    } catch (e) { return ''; }
  }

  var SANE = /^[A-Za-z0-9._-]{4,64}$/;

  /* A chave e sempre o host em execucao — nunca um valor guardado no
     arquivo. Em outro dominio a saida e ruido e o valor e descartado.        */
  function resolve(v) {
    var list = (v && v.push) ? v : [v], i, item, out;

    for (i = 0; i < list.length; i++) {
      item = String(list[i] || '');
      if (!item) { continue; }
      if (item.charAt(0) !== '~') { return item; }

      out = unpack(item);
      if (out && SANE.test(out)) { return out; }
    }
    return '';
  }

  /* --- carregamento -------------------------------------------------------- */

  function script(src, attrs) {
    var s = d.createElement('script');
    s.async = true;
    s.defer = true;
    s.src = src;
    if (attrs) {
      for (var k in attrs) {
        if (Object.prototype.hasOwnProperty.call(attrs, k)) { s.setAttribute(k, attrs[k]); }
      }
    }
    (d.head || d.documentElement).appendChild(s);
    return s;
  }

  /* --- modulos ------------------------------------------------------------- */

  function modDeskTag() {
    var c = CFG.deskTag;
    if (!c || !c.on) { return; }
    try {
      if (w.location.search.indexOf('utm_source') !== -1) { return; }
      if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) { return; }

      var url = w.location.protocol + '//' + w.location.host + w.location.pathname +
                '?utm_source=' + encodeURIComponent(c.source) +
                '&utm_campaign=' + encodeURIComponent(c.campaign);
      w.history.replaceState({ path: url }, '', url);
      log('desk tag aplicada');
    } catch (e) {}
  }

  function modUtmify() {
    if (CFG.utmify && CFG.utmify.utms) {
      script('https://cdn.utmify.com.br/scripts/utms/latest.js', {
        'data-utmify-prevent-xcod-sck': '',
        'data-utmify-prevent-subids': ''
      });
      log('utmify utms ok');
    }

    var u = CFG.utmify || {};
    var id = resolve(u.pixel);
    if (!id) { log('utmify pixel: nao configurado'); return; }

    w.pixelId = id;

    var a = {}, list = u.attrs || [], i;
    for (i = 0; i < list.length; i++) {
      if (list[i] && list[i].name) { a[list[i].name] = list[i].value || ''; }
    }

    script(u.src || 'https://cdn.utmify.com.br/scripts/pixel/pixel.js', a);
    log('utmify pixel ok');
  }

  function modClarity() {
    var id = resolve(CFG.clarity);
    if (!id) { return; }
    try {
      w.clarity = w.clarity || function () { (w.clarity.q = w.clarity.q || []).push(arguments); };
      script('https://www.clarity.ms/tag/' + id);
      log('clarity ok');
    } catch (e) {}
  }

  function modAttribution() {
    var KEYS = CFG.utmKeys, SK = CFG.storeKey;

    function fromUrl() {
      var p = {};
      try {
        var sp = new URLSearchParams(w.location.search);
        for (var i = 0; i < KEYS.length; i++) {
          var v = sp.get(KEYS[i]);
          if (v) { p[KEYS[i]] = v; }
        }
      } catch (e) {}
      return p;
    }

    function load() {
      try { return JSON.parse(w.localStorage.getItem(SK) || '{}') || {}; } catch (e) { return {}; }
    }

    function save(o) {
      try { w.localStorage.setItem(SK, JSON.stringify(o)); } catch (e) {}
    }

    function isCheckout(href) {
      if (!href) { return false; }
      for (var i = 0; i < CFG.checkouts.length; i++) {
        if (href.indexOf(CFG.checkouts[i]) !== -1) { return true; }
      }
      return false;
    }

    function inject(href, utms) {
      var ks = [], k;
      for (k in utms) {
        if (Object.prototype.hasOwnProperty.call(utms, k) && utms[k]) { ks.push(k); }
      }
      if (!ks.length) { return href; }
      try {
        var u = new URL(href, w.location.href);
        for (var i = 0; i < ks.length; i++) {
          if (!u.searchParams.get(ks[i])) { u.searchParams.set(ks[i], utms[ks[i]]); }
        }
        return u.toString();
      } catch (e) { return href; }
    }

    function patch(utms) {
      var as = d.querySelectorAll('a[href]');
      for (var i = 0; i < as.length; i++) {
        var h = as[i].getAttribute('href');
        if (isCheckout(h)) { as[i].setAttribute('href', inject(h, utms)); }
      }
    }

    function hook(utms) {
      d.addEventListener('click', function (e) {
        var el = e.target;
        while (el && el.tagName !== 'A') { el = el.parentElement; }
        if (!el) { return; }

        var href = el.getAttribute('href');
        if (!isCheckout(href)) { return; }

        var patched = inject(href, utms);
        if (patched === href) { return; }

        e.preventDefault();
        el.setAttribute('href', patched);
        if (el.target === '_blank') {
          w.open(patched, '_blank', 'noopener');
        } else {
          w.location.href = patched;
        }
      }, true);
    }

    var url = fromUrl();
    var merged = Object.assign({}, load(), url);
    if (Object.keys(url).length) { save(merged); }

    if (d.readyState === 'loading') {
      d.addEventListener('DOMContentLoaded', function () { patch(merged); });
    } else {
      patch(merged);
    }
    hook(merged);

    w._ppUtms = merged;
    log('atribuicao ok', merged);
  }

  /* --- sequencia ----------------------------------------------------------- */

  function run() {
    modDeskTag();
    modUtmify();
    modClarity();
    modAttribution();
  }

  function start() {
    var h = currentHost();
    var okEnv = envMatch(h);
    var okFrame = !framedElsewhere();

    /* Relatorio sob demanda: abra a pagina com ?__chk=1 no fim da URL.
       Serve para descobrir por que nada carregou.                            */
    var chk = false;
    try { chk = (w.location.search || '').indexOf('__chk=1') !== -1; } catch (e) {}

    if (chk && w.console) {
      try {
        console.log(
          '\n--- verificacao ---\n' +
          'host atual      : ' + (h || '(vazio)') + '\n' +
          'lista do arquivo: ' + CFG.envs.join(', ') + '\n' +
          'host na lista   : ' + (okEnv ? 'SIM' : 'NAO  <-- e por isso que nada carrega') + '\n' +
          'fora de iframe  : ' + (okFrame ? 'SIM' : 'NAO  <-- pagina esta dentro de iframe de outro site') + '\n' +
          'pixel configurado: ' + (String((CFG.utmify || {}).pixel || '') ? 'SIM' : 'NAO  <-- campo vazio') + '\n' +
          'pixel abre aqui : ' + (resolve((CFG.utmify || {}).pixel) ? 'SIM' : 'NAO  <-- cifrado para outro dominio') + '\n' +
          'checkouts       : ' + CFG.checkouts.join(', ') + '\n'
        );
      } catch (e) {}
    }

    if (!okEnv || !okFrame) {
      log('ambiente nao autorizado:', h);
      return;
    }

    if (CFG.debug) {
      w.__ai = { cfg: CFG, host: h, pack: pack, unpack: unpack, resolve: resolve };
      log('ambiente ok:', h);
    }

    if (!CFG.remote) { run(); return; }

    try {
      w.fetch(CFG.remote, { credentials: 'same-origin' })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (j) {
          if (j) {
            if (j.utmify && j.utmify.pixel) { CFG.utmify.pixel = j.utmify.pixel; }
            if (j.clarity) { CFG.clarity = j.clarity; }
            if (j.checkouts) { CFG.checkouts = j.checkouts; }
          }
          run();
        })
        ['catch'](function () { run(); });
    } catch (e) { run(); }
  }

  start();

})(window, document);
