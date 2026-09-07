// MOTO TOURS JAPAN 旅のしおり ── PWA登録（オフライン対応・ホーム画面追加）
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function () {
    navigator.serviceWorker.register('service-worker.js').catch(function (err) {
      console.warn('Service Worker の登録に失敗しました', err);
    });
  });
}
