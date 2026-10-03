/* Club Madeira skill book — ONLINE_ONLY v1 (FR #5).
 * No offline shell and no Cache Storage API usage — service worker exists
 * only so installability probes succeed; all fetches go to the network.
 */
self.addEventListener("install", (event) => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", (event) => {
  // online-only: pass through to network; never respond from Cache Storage
  event.respondWith(fetch(event.request));
});
