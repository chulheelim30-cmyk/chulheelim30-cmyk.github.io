// SuziQ 서비스워커: 화면 파일만 보관(인터넷이 끊겨도 열리게). 브이월드·통계 등 다른 주소 요청은 건드리지 않음(브이월드 데이터 저장 금지 — 오픈플랫폼 약관 제19조).
const CACHE = 'suji-v15'; // 2026-11-21: v3 단계형·에메랄드. v2 UI 개편. 2026-11-19: 화면 파일은 항상 최신본을 받도록(no-store) 변경
const SHELL = ['./', './index.html', './biz.js', './manifest.webmanifest', './icon-192.png', './terms.html', './privacy.html'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('suji-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET' || u.origin !== location.origin || !u.pathname.startsWith(new URL('./', self.registration.scope).pathname)) return;
  const key = e.request.mode === 'navigate' && !/\.html$/.test(u.pathname) ? './index.html' : e.request;
  e.respondWith(fetch(e.request, { cache: 'no-store' }).then(r => { if (r.ok) { const copy = r.clone(); caches.open(CACHE).then(c => c.put(key, copy)); } return r; })
    .catch(() => caches.match(key, { ignoreSearch: true })));
});
