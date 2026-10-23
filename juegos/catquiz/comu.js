/* CatQuiz · codi comú a la portada i a tots els jocs
   - Consentiment de galetes: Google Analytics només es carrega si s'accepta
   - Repte del dia (?repte): preguntes iguals per a tothom, resultat per compartir
   - Mode escola (?escola[&nivell=N]): sense límit de temps i nivell d'inici triat
   - Ratxa de dies jugats, darrer joc i rècords per a la portada
   - Ajustos globals: música, efectes de so i mode daltònic
   - Aplicació instal·lable (service worker) */
(function () {
  'use strict';
  var Q = new URLSearchParams(location.search);
  var ESPECT = Q.has('espectador') || Q.has('demo') || Q.has('video');
  var ls = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v === null ? d : v; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  function dataISO(d) { d = d || new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  var m = location.pathname.match(/jocs\/([a-z]+)\.html/);
  var JOC = m ? m[1] : '';
  var NOMS = { motle: 'Motle', penjat: 'Penjat 3D', anagrama: 'Anagrama', perdudes: 'Lletres perdudes', sopa: 'Sopa de lletres', roda: 'Roda de paraules',
    accents: 'Accents!', catala: 'Com es diu en català?', barbarismes: 'Barbarismes', pronoms: 'Pronoms febles', intrus: "L'intrús", futbol: 'Quiz de futbol', esportistes: "Quiz d'esportistes", castells: 'Quiz de castells', party: 'CatQuiz Party' };
  var AMB_REPTE = ['accents', 'catala', 'barbarismes', 'pronoms', 'intrus', 'perdudes', 'motle'];
  var WEB = 'https://www.catquiz.cat';

  // ---- llavor del repte del dia: mateixa seqüència per a tothom el mateix dia
  function hash(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function mulberry(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

  var AMB_NENS = ['futbol', 'esportistes', 'castells'];
  var REPTE = Q.has('repte') && !ESPECT && AMB_REPTE.indexOf(JOC) > -1;
  var ESCOLA = Q.has('escola') && !ESPECT;
  var CQ = window.CQ = {
    joc: JOC, nom: NOMS[JOC] || 'CatQuiz', noms: NOMS, ambRepte: AMB_REPTE,
    repte: REPTE, escola: ESCOLA, espectador: ESPECT,
    nivellInici: ESCOLA ? Math.max(0, Math.min(9, (parseInt(Q.get('nivell'), 10) || 1) - 1)) : 0,
    rng: mulberry(hash('catquiz|' + JOC + '|' + dataISO())),
    res: [], files: [],
    efectes: ls.get('catquiz-efectes', '1') !== '0',
    daltonic: ls.get('catquiz-daltonic', '0') === '1',
    // mode nens (quizzes de preguntes): sense rellotge, preguntes més fàcils i pistes més lentes
    nens: AMB_NENS.indexOf(JOC) > -1 && !ESPECT && !REPTE && ls.get('catquiz-nens', '0') === '1',
    avui: dataISO, ls: ls,
    marca: function (ok) { if (this.res.length < 10) this.res.push(!!ok); },
    // tria amb la llavor del dia (repte) o a l'atzar
    tria: function (a) { return a[Math.floor((REPTE ? CQ.rng() : Math.random()) * a.length)]; }
  };
  if (CQ.daltonic) document.documentElement.classList.add('daltonic');
  if (CQ.nens) document.documentElement.classList.add('cq-nens');
  if (JOC) document.documentElement.classList.add('cq-' + JOC);
  // ---- mode daltònic: encert en blau i error en taronja (en lloc de verd i vermell), i ✓/✕ als botons
  // (el Motle té els seus colors propis: taronja = lletra al seu lloc, blau = lletra en un altre lloc)
  CQ.col = CQ.daltonic ? { ok: '#2F6BFF', okT: '#FFFFFF', ko: '#FF8A1F', koT: '#FFFFFF', gris: '#6E7BB5' }
                       : { ok: '#7CE800', okT: '#1D2B64', ko: '#FF3E9A', koT: '#FFFFFF', gris: '#6E7BB5' };
  if (CQ.daltonic && JOC !== 'motle') {
    var OKS = ['.tecla.be', '.fr.be', '.op.be', '.ll.be', '#word.ok', '.frase .veredicte.v', '.targeta .ok', '#vf .si', '.llista span.trobada', '.llista span.ok'],
        KOS = ['.fr.malament', '.op.ko', '#word.bad', '.frase .veredicte.f', '.targeta .ko', '#vf .no'],
        pre = function (l, extra) { return l.map(function (x) { return 'html.daltonic ' + x + (extra || ''); }).join(','); };
    var css = pre(OKS) + '{background:linear-gradient(180deg,#5AA2FF,#1F6FE0)!important;box-shadow:0 4px 0 #124A9E,0 0 18px rgba(80,150,255,.6)!important;color:#fff!important}' +
      pre(KOS) + '{background:linear-gradient(180deg,#FFB24A,#F0781A)!important;box-shadow:0 4px 0 #A64E0E,0 0 18px rgba(255,160,60,.6)!important;color:#fff!important}' +
      'html.daltonic .frase .ok{color:#8FC2FF!important}html.daltonic .op.be .l{color:#1F6FE0!important}html.daltonic .op.ko .l{color:#F0781A!important}' +
      pre(['.fr.be', '.op.be .t'], '::before') + "{content:'✓ '}" + pre(['.fr.malament', '.op.ko .t'], '::before') + "{content:'✕ '}";
    var st = document.createElement('style'); st.id = 'cq-daltonic'; st.textContent = css;
    (document.head || document.documentElement).appendChild(st);
    // es torna a posar al final del <head> perquè guanyi els estils del joc
    document.addEventListener('DOMContentLoaded', function () { document.head.appendChild(st); });
  }
  // títols de les pantalles d'inici: si no caben (mòbils estrets o amb la lletra ampliada), s'encongeixen fins que hi caben
  function ajustaTitols() {
    document.querySelectorAll('.carta h1, .capa h1, .overlay h1, #inici h1').forEach(function (h) {
      h.style.fontSize = ''; var cs = parseFloat(getComputedStyle(h).fontSize), lim = (h.parentElement || h).clientWidth || innerWidth, n = 0;
      if (lim > innerWidth - 16) lim = innerWidth - 16;
      while (h.scrollWidth > lim + 1 && cs > 14 && n++ < 40) { cs *= .94; h.style.fontSize = cs + 'px'; }
    });
  }
  document.addEventListener('DOMContentLoaded', function () { ajustaTitols(); setTimeout(ajustaTitols, 400); if (document.fonts) document.fonts.ready.then(ajustaTitols); });
  addEventListener('resize', ajustaTitols);
  // interruptor del mode daltònic a la pantalla d'inici de cada joc (també s'activa des dels ajustos de la portada)
  document.addEventListener('DOMContentLoaded', function () {
    var cx = document.querySelector('#inici .caixa, #startOv .caixa, .carta#inici > div'); if (!cx || ESPECT) return;
    var dest = cx;
    if (AMB_NENS.indexOf(JOC) > -1 && !REPTE) {
      // fila d'opcions: mode nens + mode daltònic
      dest = document.createElement('div'); dest.className = 'cq-opcions';
      dest.style.cssText = 'display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:6px 18px;margin-top:14px';
      var k = document.createElement('label'); k.className = 'cq-nens-tog';
      k.style.cssText = 'display:inline-flex;align-items:center;gap:10px;min-height:44px;font:700 14px Roboto,sans-serif;color:#fff;cursor:pointer;white-space:nowrap';
      k.innerHTML = '<input type="checkbox" style="width:20px;height:20px;accent-color:#FFD24A;margin:0"><span>🧒 Mode nens <span style="font-weight:500;color:#D9D6FF">(sense rellotge)</span></span>';
      k.title = 'Sense límit de temps, preguntes més fàcils i pistes més lentes';
      var kc = k.querySelector('input'); kc.checked = CQ.nens;
      kc.addEventListener('change', function () { CQ.nens = kc.checked; ls.set('catquiz-nens', kc.checked ? '1' : '0'); document.documentElement.classList.toggle('cq-nens', kc.checked); });
      dest.appendChild(k); cx.appendChild(dest);
    }
    var l = document.createElement('label'); l.className = 'cq-dalt';
    l.style.cssText = (dest === cx ? 'display:flex;margin-top:14px;' : 'display:inline-flex;white-space:nowrap;') + 'align-items:center;justify-content:center;gap:10px;min-height:44px;font:500 14px Roboto,sans-serif;color:#D9D6FF;cursor:pointer';
    l.innerHTML = '<input type="checkbox" style="width:20px;height:20px;accent-color:#3D8EFF;margin:0"> 👁️ Mode daltònic';
    var c = l.querySelector('input'); c.checked = CQ.daltonic;
    c.addEventListener('change', function () { ls.set('catquiz-daltonic', c.checked ? '1' : '0'); location.reload(); });
    dest.appendChild(l);
  });
  if (ESCOLA) document.documentElement.classList.add('cq-escola');
  if (REPTE) document.documentElement.classList.add('cq-repte');

  // ---- dies jugats i ratxa
  function marcaJugat() {
    if (ESPECT || !JOC) return;
    var dies = []; try { dies = JSON.parse(ls.get('catquiz-dies', '[]')); } catch (e) {}
    var d = dataISO(); if (dies.indexOf(d) < 0) dies.push(d);
    ls.set('catquiz-dies', JSON.stringify(dies.slice(-400)));
    ls.set('catquiz-darrer', JOC);
  }
  CQ.ratxa = function () {
    var dies = []; try { dies = JSON.parse(ls.get('catquiz-dies', '[]')); } catch (e) {}
    var set = {}; dies.forEach(function (x) { set[x] = 1; });
    var d = new Date(), n = 0;
    if (!set[dataISO(d)]) d.setDate(d.getDate() - 1); // si avui encara no has jugat, la ratxa d'ahir encara compta
    while (set[dataISO(d)]) { n++; d.setDate(d.getDate() - 1); }
    return { dies: n, avui: !!set[dataISO()], total: dies.length };
  };
  CQ.estat = function () { try { return JSON.parse(ls.get('catquiz-stats', '{}')); } catch (e) { return {}; } };
  function desaPartida(punts) {
    if (ESPECT || !JOC) return;
    var s = CQ.estat(), j = s[JOC] || { partides: 0, millor: 0 };
    j.partides++; if (punts > j.millor) j.millor = punts; j.data = dataISO();
    s[JOC] = j; ls.set('catquiz-stats', JSON.stringify(s));
  }
  document.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('#btn-inici, #btn-reinici, #btn-diari, .cats .gros, #playBtn, #nextBtn')) marcaJugat();
  }, true);

  // ---- repte del dia: un sol intent per joc i dia (compta el primer)
  CQ.repteFet = function (joc) { var v = ls.get('catquiz-repte-' + (joc || JOC), '').split('|'); return v[0] === dataISO() ? v : null; };
  function compteEnrere(el) {
    function pinta() { var d = new Date(), m = new Date(d); m.setHours(24, 0, 0, 0); var t = Math.max(0, Math.floor((m - d) / 1000));
      el.textContent = String(Math.floor(t / 3600)).padStart(2, '0') + ':' + String(Math.floor(t % 3600 / 60)).padStart(2, '0') + ':' + String(t % 60).padStart(2, '0');
      if (!t) location.reload(); }
    pinta(); setInterval(pinta, 1000);
  }
  function pantallaRepteFet(v) {
    var txt = ''; try { txt = decodeURIComponent(v[2] || ''); } catch (e) {}
    var linies = txt.split('\n'), quadres = linies.slice(1).join('\n').replace(/\s+\d+\/10.*$/, '');
    var pendents = AMB_REPTE.filter(function (j) { return j !== JOC && !CQ.repteFet(j); });
    var d = document.createElement('div'); d.className = 'cq-fet'; d.setAttribute('role', 'dialog'); d.setAttribute('aria-label', "Repte d'avui fet");
    d.innerHTML = '<div class="cq-fet-caixa"><p class="cq-fet-eti">Repte del dia · ' + NOMS[JOC] + '</p><h1>Ja l\'has fet avui!</h1>' +
      (v[1] ? '<p class="cq-fet-nota">' + (JOC === 'motle' ? (v[1] === 'X' ? 'Avui no l\'has encertada' : 'Encertada en ' + v[1] + ' intents') : v[1] + ' de 10') + '</p>' : '') +
      (quadres ? '<pre class="cq-fet-res">' + quadres.replace(/[<&]/g, '') + '</pre>' : '') +
      '<p class="cq-fet-txt">El repte nou surt d\'aquí a <b class="cq-fet-compte"></b></p>' +
      '<div class="cq-fet-bot">' + (txt ? '<button type="button" class="cq-fet-comp">📤 Comparteix</button>' : '') + '<a class="cq-fet-lliure" href="' + JOC + '.html">▶ Juga lliure</a></div>' +
      (pendents.length ? '<p class="cq-fet-txt">Encara et ' + (pendents.length === 1 ? 'queda 1 repte' : 'queden ' + pendents.length + ' reptes') + ' d\'avui:</p><div class="cq-fet-altres">' +
        pendents.map(function (j) { return '<a href="' + j + '.html?repte">' + NOMS[j] + '</a>'; }).join('') + '</div>'
        : '<p class="cq-fet-txt">🔥 Has fet tots els reptes d\'avui!</p>') +
      '<a class="cq-fet-tornar" href="../index.html">← Tots els jocs</a></div>';
    document.body.appendChild(d);
    compteEnrere(d.querySelector('.cq-fet-compte'));
    var bc = d.querySelector('.cq-fet-comp');
    if (bc) bc.onclick = function () { CQ.comparteix(txt, WEB + '/jocs/' + JOC + '.html?repte'); try { gtag('event', 'comparteix', { joc: JOC, repte: 1, fet: 1 }); } catch (er) {} };
    if (!CASA) d.querySelectorAll('.cq-fet-tornar').forEach(function (a) { a.href = '../../../#sec-catquiz'; a.target = '_top'; });
  }

  // ---- compartir
  function avisCurt(t) {
    var a = document.createElement('div'); a.className = 'cq-avis'; a.textContent = t; document.body.appendChild(a);
    setTimeout(function () { a.classList.add('fora'); }, 1600); setTimeout(function () { a.remove(); }, 2200);
  }
  CQ.comparteix = function (text, url) {
    var tot = text + '\n' + url;
    if (navigator.share) { navigator.share({ text: text, url: url }).catch(function () {}); return; }
    try { navigator.clipboard.writeText(tot).then(function () { avisCurt('Copiat! Enganxa-ho on vulguis 📋'); }); }
    catch (e) { prompt('Copia el teu resultat:', tot); }
  };
  function textResultat(punts) {
    var d = new Date(), dm = d.getDate() + '/' + (d.getMonth() + 1);
    if (JOC === 'motle' && CQ.files.length) {
      var em = CQ.daltonic ? { be: '🟧', quasi: '🟦', no: '⬛' } : { be: '🟩', quasi: '🟨', no: '⬛' };
      var guanyat = CQ.files[CQ.files.length - 1].every(function (x) { return x === 'be'; });
      return { text: 'Motle ' + (REPTE || CQ.motleDiari ? 'del ' + dm + ' ' : '') + (guanyat ? CQ.files.length : 'X') + '/6\n' +
        CQ.files.map(function (f) { return f.map(function (x) { return em[x]; }).join(''); }).join('\n'),
        url: WEB + '/jocs/motle.html' + (REPTE || CQ.motleDiari ? '?repte' : '') };
    }
    if (REPTE && CQ.res.length) {
      var enc = CQ.res.filter(Boolean).length;
      return { text: 'CatQuiz · ' + CQ.nom + ' · Repte del ' + dm + '\n' + CQ.res.map(function (x) { return x ? (CQ.daltonic ? '🟦' : '🟩') : (CQ.daltonic ? '🟧' : '🟥'); }).join('') + '  ' + enc + '/10' + (punts ? ' · ' + punts + ' punts' : ''),
        url: WEB + '/jocs/' + JOC + '.html?repte' };
    }
    return { text: (punts ? 'He fet ' + punts + ' punts' : 'He jugat') + ' a ' + CQ.nom + ' de CatQuiz 🎮 Em superes?', url: WEB + '/jocs/' + JOC + '.html' };
  }
  function puntsFinals() {
    var el = document.getElementById('punts-final') || document.getElementById('finalPunts');
    var n = el ? parseInt((el.textContent || '').replace(/\D/g, ''), 10) : 0;
    return isNaN(n) ? 0 : n;
  }
  function enFinal(fin) {
    var punts = puntsFinals();
    desaPartida(punts);
    if (REPTE && !CQ.repteFet()) { var tr = textResultat(punts); ls.set('catquiz-repte-' + JOC, dataISO() + '|' + (JOC === 'motle' ? (tr.text.match(/ (\d|X)\/6/) || ['', '?'])[1] : CQ.res.filter(Boolean).length) + '|' + encodeURIComponent(tr.text)); }
    var caixa = fin.querySelector('.caixa') || fin.firstElementChild || fin;
    var b = caixa.querySelector('.cq-comparteix');
    if (!b) {
      b = document.createElement('button'); b.className = 'cq-comparteix acc gros'; b.type = 'button';
      b.innerHTML = '📤 Comparteix';
      caixa.appendChild(b);
      if (REPTE) { var r = document.createElement('p'); r.className = 'cq-res'; var primer = caixa.querySelector('button:not(.cq-comparteix)'); caixa.insertBefore(r, primer || b); }
    }
    var rr = caixa.querySelector('.cq-res');
    if (rr) rr.textContent = CQ.res.map(function (x) { return x ? (CQ.daltonic ? '🟦' : '🟩') : (CQ.daltonic ? '🟧' : '🟥'); }).join('');
    b.onclick = function (e) { e.stopPropagation(); var t = textResultat(punts); CQ.comparteix(t.text, t.url); try { gtag('event', 'comparteix', { joc: JOC, repte: REPTE ? 1 : 0 }); } catch (er) {} };
  }

  // ---- galetes (consentiment) i Google Analytics
  // A catquiz.cat (i en local) hi ha analítica, bàner de galetes i app instal·lable. Quan els jocs s'allotgen en una altra web
  // (p. ex. el Salón Recreativo d'Alica Games Studio), no: allà manen la seva política i el seu propi botó per tornar.
  var CASA = /(^|\.)catquiz\.cat$/.test(location.hostname) || /^(localhost|127\.0\.0\.1|)$/.test(location.hostname);
  CQ.casa = CASA;
  var GA_ID = 'G-SDE8LXDNP9';
  function carregaGA() {
    if (window.__cqGA || !CASA) return; window.__cqGA = 1;
    var s = document.createElement('script'); s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID; document.head.appendChild(s);
  }
  var arrel = JOC ? '../' : (location.pathname.split('/').filter(Boolean).length > 0 && !/\.html$/.test(location.pathname) ? '../' : '');
  CQ.galetes = function () {
    var vell = document.querySelector('.cq-galetes'); if (vell) vell.remove();
    var d = document.createElement('div'); d.className = 'cq-galetes'; d.setAttribute('role', 'dialog'); d.setAttribute('aria-label', 'Galetes');
    d.innerHTML = '<p>🍪 Fem servir galetes d\'analítica (Google Analytics) només per saber quins jocs agraden més. No hi ha publicitat. <a href="' + arrel + 'privacitat/">Més informació</a></p>' +
      '<div><button type="button" class="cq-si">Accepta</button><button type="button" class="cq-no">Rebutja</button></div>';
    document.body.appendChild(d);
    d.querySelector('.cq-si').onclick = function (e) { e.stopPropagation(); ls.set('catquiz-galetes', 'si'); carregaGA(); d.remove(); };
    d.querySelector('.cq-no').onclick = function (e) { e.stopPropagation(); ls.set('catquiz-galetes', 'no'); d.remove(); };
  };
  var consent = ls.get('catquiz-galetes', '');
  if (consent === 'si') carregaGA();

  // ---- estils comuns (avís, botó de compartir, bàner de galetes, mode escola)
  var css = '.cq-galetes{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom,0px));z-index:9999;max-width:560px;margin:0 auto;display:flex;gap:12px;align-items:center;flex-wrap:wrap;padding:14px 16px;border-radius:20px;background:rgba(26,22,80,.96);border:1.5px solid rgba(150,170,255,.5);box-shadow:0 0 30px rgba(120,160,255,.4),0 10px 30px rgba(0,0,0,.5);color:#fff;font:500 14px/1.45 Roboto,system-ui,sans-serif}' +
    '.cq-galetes p{flex:1 1 260px;margin:0;color:#D9D6FF}.cq-galetes a{color:#5CF0FF}.cq-galetes div{display:flex;gap:8px}' +
    '.cq-galetes button{min-height:44px;padding:0 18px;border-radius:999px;font:700 14px Roboto,system-ui,sans-serif;letter-spacing:.04em;text-transform:uppercase;cursor:pointer;color:#fff;border:2px solid rgba(255,255,255,.5)}' +
    '.cq-galetes .cq-si{background:linear-gradient(180deg,#6CEB5A,#2FB03C);box-shadow:0 4px 0 #1E7F2C}.cq-galetes .cq-no{background:rgba(255,255,255,.08);box-shadow:none}' +
    '.cq-avis{position:fixed;left:50%;top:18%;transform:translateX(-50%);z-index:9999;padding:10px 18px;border-radius:999px;background:rgba(24,20,70,.95);border:1.5px solid rgba(150,170,255,.5);color:#fff;font:700 15px Roboto,system-ui,sans-serif;transition:opacity .5s}.cq-avis.fora{opacity:0}' +
    '.cq-comparteix{margin-top:12px!important}.cq-res{font-size:22px!important;letter-spacing:2px;margin:6px 0 0!important}' +
    'html.cq-escola #barra,html.cq-escola .barra,html.cq-nens #barra{display:none!important}' +
    '.cq-fet{position:fixed;inset:0;z-index:9998;display:grid;place-items:center;padding:16px;overflow:auto;background:radial-gradient(circle at 50% 25%,rgba(120,90,255,.45),transparent 60%),linear-gradient(170deg,#4A2FB5,#2E2080 45%,#1A1650);font:500 15px/1.45 Roboto,system-ui,sans-serif;color:#fff;text-align:center}' +
    '.cq-fet-caixa{width:min(440px,100%);padding:26px 22px;border-radius:28px;background:linear-gradient(180deg,rgba(60,44,140,.92),rgba(26,22,80,.95));border:1.5px solid rgba(150,170,255,.45);box-shadow:0 0 40px rgba(110,140,255,.3),0 18px 40px rgba(0,0,0,.35)}' +
    '.cq-fet-eti{display:inline-block;margin:0 0 10px;padding:4px 12px;border-radius:999px;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#C9C4FF;background:rgba(24,20,70,.6);border:1.5px solid rgba(150,170,255,.45)}' +
    '.cq-fet h1{margin:0;font:900 clamp(28px,8vw,40px)/1.05 Roboto,sans-serif;color:#FFD24A;text-shadow:0 0 20px rgba(255,210,74,.45),0 3px 0 rgba(0,0,0,.35)}' +
    '.cq-fet-nota{margin:10px 0 0;font-size:20px;font-weight:900}.cq-fet-res{margin:10px 0 0;font:22px/1.25 system-ui,sans-serif;letter-spacing:2px;white-space:pre-wrap}' +
    '.cq-fet-txt{margin:16px 0 0;color:#D9D6FF}.cq-fet-compte{color:#5CF0FF;font-variant-numeric:tabular-nums}' +
    '.cq-fet-bot{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:18px}' +
    '.cq-fet-bot button,.cq-fet-bot a{display:inline-flex;align-items:center;min-height:48px;padding:0 20px;border-radius:999px;font:700 15px Roboto,sans-serif;letter-spacing:.03em;color:#fff;text-decoration:none;cursor:pointer;border:2px solid rgba(255,255,255,.55)}' +
    '.cq-fet .cq-fet-comp{background:linear-gradient(180deg,#FFB24A,#F0781A)!important;box-shadow:0 4px 0 #A64E0E!important;text-transform:none!important;font:700 15px Roboto,sans-serif!important;width:auto!important;margin:0!important}.cq-fet .cq-fet-lliure{background:linear-gradient(180deg,#6CEB5A,#2FB03C)!important;box-shadow:0 4px 0 #1E7F2C!important}' +
    '.cq-fet-altres{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:10px}.cq-fet-altres a{min-height:44px;display:inline-flex;align-items:center;padding:0 14px;border-radius:999px;color:#fff;text-decoration:none;font-weight:700;font-size:14px;background:rgba(24,20,70,.6);border:1.5px solid rgba(150,170,255,.45)}' +
    '.cq-fet-altres a:hover{border-color:#fff}.cq-fet-tornar{display:inline-block;margin-top:18px;color:#C9C4FF;min-height:44px;line-height:44px}';
  var st = document.createElement('style'); st.textContent = css; (document.head || document.documentElement).appendChild(st);

  document.addEventListener('DOMContentLoaded', function () {
    if (REPTE && CQ.repteFet()) pantallaRepteFet(CQ.repteFet());
    if (!consent && !ESPECT && CASA) CQ.galetes();
    // fora de catquiz.cat, «← CatQuiz» torna a la secció CatQuiz de la web que acull els jocs
    if (!CASA) document.querySelectorAll('a[href="../index.html"]').forEach(function (a) { a.href = '../../../#sec-catquiz'; a.target = '_top'; });
    // pantalla final → desa la partida i mostra «Comparteix»
    var fin = document.getElementById('final');
    if (fin && !ESPECT) new MutationObserver(function () { if (!fin.hidden) enFinal(fin); }).observe(fin, { attributes: true, attributeFilter: ['hidden'] });
    // textos de la pantalla d'inici en repte o escola
    var ini = document.querySelector('#inici .caixa p, #inici p');
    if (ini && REPTE) ini.insertAdjacentHTML('afterbegin', '<b>Repte del dia</b> · ' + (JOC === 'motle' ? 'la mateixa paraula per a tothom avui.' : '10 preguntes, les mateixes per a tothom avui, de més fàcil a més difícil.') + ' En acabar, comparteix el teu resultat!<br>');
    if (ini && ESCOLA) ini.insertAdjacentHTML('afterbegin', '<b>Mode escola</b> · sense límit de temps' + (CQ.nivellInici ? ', comença al nivell ' + (CQ.nivellInici + 1) : '') + '. ');
    // portada i jocs: aplicació instal·lable
    if (CASA && 'serviceWorker' in navigator && location.protocol === 'https:') navigator.serviceWorker.register('/sw.js').catch(function () {});
  });
})();
