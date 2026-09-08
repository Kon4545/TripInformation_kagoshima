// MOTO TOURS JAPAN 旅のしおり ── オフライン対応用 Service Worker
// キャッシュバージョンを上げると、古いキャッシュは activate 時に自動削除される
const CACHE_NAME = 'mtj-shiori-v40';

const PRECACHE_URLS = [
  'index.html',
  'route.html',
  'caution.html',
  'company_information.html',
  'post_tour.html',
  'itinerary_day1.html',
  'itinerary_day2.html',
  'itinerary_day3.html',
  'itinerary_day4.html',
  'itinerary_day5.html',
  'itinerary_day6.html',
  'itinerary_day7.html',
  'print.html',
  'style.css',
  'i18n.js',
  'tour-data.js',
  'pwa.js',
  'manifest.json',
  'MTJ_logo_color_RGB.jpg',
  'images/hero-bg.jpg',
  'images/hotel-1.jpg',
  'images/hotel-2.jpg',
  'images/icon-192.png',
  'images/icon-512.png',
  'images/icon-512-maskable.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return Promise.all(
        PRECACHE_URLS.map(url =>
          cache.add(new Request(url, { cache: 'reload' })).catch(() => {})
        )
      );
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(names =>
      Promise.all(names.filter(n => n !== CACHE_NAME).map(n => caches.delete(n)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return; // 外部CDN等は素通し（ブラウザ標準のキャッシュに任せる）
  if (url.pathname.endsWith('/admin.html')) return; // 管理画面は常に最新版を取得する（キャッシュ・オフライン対応の対象外）

  event.respondWith(
    caches.match(req).then(cached => {
      const network = fetch(req).then(res => {
        if (res && res.ok) {
          const clone = res.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(req, clone));
        }
        return res;
      }).catch(err => {
        if (cached) return cached;
        throw err; // キャッシュも無ければ通常のネットワークエラーとして扱う
      });
      // キャッシュがあれば即返しつつ、裏で最新版を取得してキャッシュ更新（stale-while-revalidate）
      return cached || network;
    })
  );
});
