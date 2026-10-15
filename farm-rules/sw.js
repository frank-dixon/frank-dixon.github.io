/* Livestock Rules service worker. Version 199699c8edee.
 * Shell assets: cache first. Pages: network first, and the last copy is kept
 * so a lookup you already opened can be read offline. Anything that is not a
 * GET, and the admin, are never cached. */
const VERSION = "199699c8edee";
const SHELL = "lr-shell-" + VERSION;
const PAGES = "lr-pages";
const BASE = "/farm\u002Drules/";
const STATIC_PREFIX = "/farm\u002Drules/static/";
const OFFLINE_URL = "/farm\u002Drules/offline/";
const MANIFEST_URL = "/farm\u002Drules/manifest.webmanifest";
const STATIC_SITE = true;
const SHELL_URLS = [OFFLINE_URL, MANIFEST_URL, "/farm\u002Drules/", "/farm\u002Drules/lookup/", "/farm\u002Drules/saved/", "/farm\u002Drules/about/", "/farm\u002Drules/terms/", "/farm\u002Drules/data/rules.json", "/farm\u002Drules/static/css/app.f15c4b63841e.css", "/farm\u002Drules/static/js/app.2ae503fe0bad.js", "/farm\u002Drules/static/icons/icon\u002D192.1d2de48ab387.png", "/farm\u002Drules/static/icons/apple\u002Dtouch\u002Dicon.11ca77ad0f64.png", "/farm\u002Drules/static/fonts/instrument\u002Dsans\u002Dlatin\u002Dvar.fa41c43a3d8e.woff2", "/farm\u002Drules/static/fonts/dm\u002Dmono\u002Dlatin\u002D400\u002Dnormal.e1ed461ac183.woff2", "/farm\u002Drules/static/fonts/dm\u002Dmono\u002Dlatin\u002D500\u002Dnormal.c4598219c4b8.woff2", "/farm\u002Drules/static/fonts/source\u002Dserif\u002D4\u002Dlatin\u002Dopsz\u002Dnormal.e9192c2fe0a3.woff2", "/farm\u002Drules/static/fonts/source\u002Dserif\u002D4\u002Dlatin\u002Dopsz\u002Ditalic.66c33f6b248f.woff2", "/farm\u002Drules/static/img/photos/barn\u002D800.50ce8c6d7fe1.webp", "/farm\u002Drules/static/img/photos/rabbit\u002D400.645e1745ba15.webp"];
const MAX_PAGES = 40;

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(SHELL).then((cache) => cache.addAll(SHELL_URLS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((key) => key.startsWith("lr-shell-") && key !== SHELL).map((key) => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

async function trim(name, max) {
  const cache = await caches.open(name);
  const keys = await cache.keys();
  await Promise.all(keys.slice(0, Math.max(keys.length - max, 0)).map((key) => cache.delete(key)));
}

function cacheable(url) {
  return url.pathname.startsWith(BASE) && !url.pathname.startsWith(BASE + "admin/") && url.pathname !== BASE + "sw.js";
}

async function page(request) {
  try {
    const response = await fetch(request);
    if (response.ok && !response.redirected && (response.headers.get("content-type") || "").includes("text/html")) {
      const cache = await caches.open(PAGES);
      await cache.delete(request);
      await cache.put(request, response.clone());
      trim(PAGES, MAX_PAGES);
    }
    return response;
  } catch (error) {
    let saved = await caches.match(request, { cacheName: PAGES });
    // The frozen copy renders lookups in the browser, so one cached lookup page serves any query.
    if (!saved && STATIC_SITE) saved = await caches.match(request, { cacheName: PAGES, ignoreSearch: true }) || await caches.match(request, { ignoreSearch: true });
    return saved || (await caches.match(OFFLINE_URL));
  }
}

self.addEventListener("fetch", (event) => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== "GET" || url.origin !== self.location.origin || !cacheable(url)) {
    return;
  }
  if (request.mode === "navigate") {
    event.respondWith(page(request));
  } else if (url.pathname.startsWith(STATIC_PREFIX) || url.pathname === MANIFEST_URL || (STATIC_SITE && url.pathname.startsWith(BASE + "data/"))) {
    event.respondWith(caches.match(request).then((saved) => saved || fetch(request)));
  }
});

