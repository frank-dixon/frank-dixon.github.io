/* Frank Dixon site service worker. Version 782d40d12672.
 * Shell assets: cache first. Pages and images: network first, the last copy
 * kept so visited pages read offline. Admin and non-GET requests are never
 * cached. */
const VERSION = "782d40d12672";
const SHELL = "fd-shell-" + VERSION;
const PAGES = "fd-pages";
const BASE = "/";
const OFFLINE_URL = "/offline/";
const SHELL_URLS = [BASE, OFFLINE_URL, "/notes/", "/manifest.webmanifest", "/static/css/app.d9861060ded7.css", "/static/vendor/htmx.min.19a573773be4.js", "/static/icons/icon.278160a8b048.svg", "/static/icons/icon\u002D192.836425a88f77.png"];
const MAX_PAGES = 80;
/* The static site shares its origin (frank-dixon.github.io) with other apps at
   /rabbit/, /shellwork/, /gallery/ and so on. Only handle this site's own
   paths so the worker never caches or intercepts another app. */
const OWN_PATHS = ["", "projects/", "notes/", "tag/", "offline/", "static/", "media/", "manifest.webmanifest"];
const own = (path) => path.startsWith(BASE) && OWN_PATHS.some((p) => p === "" ? path === BASE : path.slice(BASE.length).startsWith(p));

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(SHELL).then((cache) => cache.addAll(SHELL_URLS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith("fd-shell-") && k !== SHELL).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

async function trim() {
  const cache = await caches.open(PAGES);
  const keys = await cache.keys();
  await Promise.all(keys.slice(0, Math.max(keys.length - MAX_PAGES, 0)).map((k) => cache.delete(k)));
}

async function networkFirst(request) {
  try {
    const response = await fetch(request);
    if (response.ok && !response.redirected) {
      const cache = await caches.open(PAGES);
      await cache.put(request, response.clone());
      trim();
    }
    return response;
  } catch (error) {
    const saved = await caches.match(request);
    if (saved) return saved;
    if (request.mode === "navigate") return caches.match(OFFLINE_URL);
    return Response.error();
  }
}

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET" || url.origin !== location.origin) return;
  if (!own(url.pathname)) return;  // admin, sw.js and other apps
  if (url.pathname.startsWith(BASE + "static/")) {
    event.respondWith(caches.match(event.request).then((hit) => hit || fetch(event.request)));
    return;
  }
  event.respondWith(networkFirst(event.request));
});

