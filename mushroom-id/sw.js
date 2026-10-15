/* Fungi guide service worker. Version c6a8752b1e44.
 * Shell assets: cache first. Pages: network first, the last copy kept for
 * offline use. Sign-in pages, admin, exports, and anything that is not a
 * GET are never cached. */
const VERSION = "c6a8752b1e44";
const SHELL = "pf-shell-" + VERSION;
const PAGES = "pf-pages";
const BASE = "/mushroom\u002Did/";
const OFFLINE_URL = BASE + "offline/";
const SHELL_URLS = [OFFLINE_URL, BASE + "catalog.json", BASE + "manifest.webmanifest", "/mushroom\u002Did/static/css/app.e5cfbfddd25e.css", "/mushroom\u002Did/static/js/app.5fb1647e93ca.js", "/mushroom\u002Did/static/icons/icon\u002D192.207b616ec075.png", "/mushroom\u002Did/static/icons/apple\u002Dtouch\u002Dicon.a3e603007d23.png", "/mushroom\u002Did/static/fonts/instrument\u002Dsans\u002Dlatin\u002Dvar.fa41c43a3d8e.woff2", "/mushroom\u002Did/static/fonts/source\u002Dserif\u002D4\u002Dlatin\u002Dopsz\u002Dnormal.e9192c2fe0a3.woff2", "/mushroom\u002Did/static/fonts/source\u002Dserif\u002D4\u002Dlatin\u002Dopsz\u002Ditalic.66c33f6b248f.woff2", "/mushroom\u002Did/static/fonts/dm\u002Dmono\u002Dlatin\u002D400\u002Dnormal.e1ed461ac183.woff2", "/mushroom\u002Did/static/fonts/dm\u002Dmono\u002Dlatin\u002D500\u002Dnormal.c4598219c4b8.woff2"];
const MAX_PAGES = 40;
// Plant photos: small copies at install, larger ones as they are opened.
const PHOTOS = "pf-photos";
const PHOTO_URLS = ["/mushroom\u002Did/static/fungi/artists\u002Dconk.2bc0c4566e9f.webp", "/mushroom\u002Did/static/fungi/birch\u002Dpolypore.da5adff7cfe4.webp", "/mushroom\u002Did/static/fungi/bitter\u002Dbolete.1a88161795ce.webp", "/mushroom\u002Did/static/fungi/black\u002Dtrumpet.b53d04e55c68.webp", "/mushroom\u002Did/static/fungi/bleeding\u002Dtooth.18d6bd2ebade.webp", "/mushroom\u002Did/static/fungi/chaga.9674d24a17d1.webp", "/mushroom\u002Did/static/fungi/chanterelle.7fc5fcd8ac1a.webp", "/mushroom\u002Did/static/fungi/chicken\u002Dof\u002Dthe\u002Dwoods.eed87dd8cfb7.webp", "/mushroom\u002Did/static/fungi/common\u002Dink\u002Dcap.4c8bee83e191.webp", "/mushroom\u002Did/static/fungi/deadly\u002Dgalerina.24f1bfb2c6d6.webp", "/mushroom\u002Did/static/fungi/death\u002Dcap.d33d4df2512a.webp", "/mushroom\u002Did/static/fungi/destroying\u002Dangel.2bfa37ac84b3.webp", "/mushroom\u002Did/static/fungi/dryads\u002Dsaddle.28be835c60ef.webp", "/mushroom\u002Did/static/fungi/fairy\u002Dring\u002Dmushroom.d5dd835b9469.webp", "/mushroom\u002Did/static/fungi/false\u002Dmorel.3e2fa226aa67.webp", "/mushroom\u002Did/static/fungi/fly\u002Dagaric.48dc4742e2fd.webp", "/mushroom\u002Did/static/fungi/gem\u002Dstudded\u002Dpuffball.766233ac4003.webp", "/mushroom\u002Did/static/fungi/giant\u002Dpuffball.65841f4eec09.webp", "/mushroom\u002Did/static/fungi/green\u002Dspored\u002Dparasol.135bc7ebff82.webp", "/mushroom\u002Did/static/fungi/hemlock\u002Dvarnish\u002Dshelf.49d776293459.webp", "/mushroom\u002Did/static/fungi/hen\u002Dof\u002Dthe\u002Dwoods.b873119c8d3c.webp", "/mushroom\u002Did/static/fungi/honey\u002Dmushroom.9baf03b43d21.webp", "/mushroom\u002Did/static/fungi/jack\u002Do\u002Dlantern.f7dbb7b9f0fd.webp", "/mushroom\u002Did/static/fungi/king\u002Dbolete.220d31e6917e.webp", "/mushroom\u002Did/static/fungi/lions\u002Dmane.773a33709fea.webp", "/mushroom\u002Did/static/fungi/lobster\u002Dmushroom.2cdbec7c9ff5.webp", "/mushroom\u002Did/static/fungi/meadow\u002Dmushroom.5275ae326f72.webp", "/mushroom\u002Did/static/fungi/morel.7d6f9d76a728.webp", "/mushroom\u002Did/static/fungi/old\u002Dman\u002Dof\u002Dthe\u002Dwoods.e279687a1d87.webp", "/mushroom\u002Did/static/fungi/oyster\u002Dmushroom.31a97adfe9f3.webp", "/mushroom\u002Did/static/fungi/pigskin\u002Dpoison\u002Dpuffball.66283362fa71.webp", "/mushroom\u002Did/static/fungi/shaggy\u002Dmane.b164ec69e0b5.webp", "/mushroom\u002Did/static/fungi/dog\u002Dstinkhorn.dcce589cd25d.webp", "/mushroom\u002Did/static/fungi/sulfur\u002Dtuft.d6ea6573b1fc.webp", "/mushroom\u002Did/static/fungi/turkey\u002Dtail.a163c00ac695.webp", "/mushroom\u002Did/static/fungi/velvet\u002Dfoot.0d0001ed00a4.webp", "/mushroom\u002Did/static/fungi/wine\u002Dcap.4216757d0b13.webp", "/mushroom\u002Did/static/fungi/witchs\u002Dbutter.48d6f6117e53.webp", "/mushroom\u002Did/static/fungi/wood\u002Dear.7850d2dc65dd.webp"];
const MAX_PHOTOS = 900;

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(SHELL)
      .then((cache) => cache.addAll(SHELL_URLS))
      .then(() => caches.open(PHOTOS))
      // One missing photo must not block the install.
      .then((cache) => Promise.allSettled(PHOTO_URLS.map((url) => cache.match(url).then((hit) => hit || cache.add(url)))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((key) => key.startsWith("pf-shell-") && key !== SHELL).map((key) => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("message", (event) => {
  if (event.data === "clear-private") {
    event.waitUntil(caches.delete(PAGES));
  }
});

async function trim(name, max) {
  const cache = await caches.open(name);
  const keys = await cache.keys();
  await Promise.all(keys.slice(0, Math.max(keys.length - max, 0)).map((key) => cache.delete(key)));
}

function local(url) {
  return url.pathname.startsWith(BASE) ? "/" + url.pathname.slice(BASE.length) : url.pathname;
}

function cacheable(url) {
  const path = local(url);
  return !/^\/(accounts|admin|export|api)\//.test(path)
    && path !== "/sw.js"
    && path !== "/export.json";
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
    const saved = await caches.match(request, { cacheName: PAGES });
    return saved || (await caches.match(OFFLINE_URL));
  }
}

async function photo(request) {
  const cache = await caches.open(PHOTOS);
  const saved = await cache.match(request);
  if (saved) return saved;
  try {
    const response = await fetch(request);
    if (response.ok) {
      await cache.put(request, response.clone());
      trim(PHOTOS, MAX_PHOTOS);
    }
    return response;
  } catch (error) {
    return new Response("", { status: 504, statusText: "Offline" });
  }
}

self.addEventListener("fetch", (event) => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== "GET" || url.origin !== self.location.origin || !cacheable(url)) {
    return;
  }
  const accept = request.headers.get("accept") || "";
  if (request.mode === "navigate" || accept.includes("text/html")) {
    event.respondWith(page(request));
  } else if (local(url) === "/catalog.json" || local(url).startsWith("/static/") || local(url) === "/manifest.webmanifest") {
    event.respondWith(caches.match(request).then((saved) => saved || fetch(request)));
  }
});

