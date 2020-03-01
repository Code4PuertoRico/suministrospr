const version = "{{ app_version }}";
const cacheName = `suministrospr-cache-${version}`;
// For now only root and offline since it will dynamically add the other urls
let filesToCache = ["/", "/offline/"];

/**
 * Deletes all caches except the ones in cacheName
 */
const deleteCaches = () => {
  return caches
    .keys()
    .then(keys => keys.filter(key => key !== cacheName))
    .then(keys => keys.map(key => caches.delete(key)))
    .then(delArray => Promise.all(delArray));
};

/**
 * Add response to cache
 * @param {Request} request
 * @param {Response} response
 */
const cacheResponse = (request, response) => {
  const clonedResponse = response.clone();
  caches.open(cacheName).then(cache => {
    cache.put(request, clonedResponse);
  });
  return response;
};

/**
 * Fetch and update cache
 * @param {Request} request
 */
const fetchAndCache = request => {
  return fetch(request)
    .then(response => {
      return cacheResponse(request, response);
    })
    .catch(err => console.log(err));
};

/**
 * Check if response is valid
 * @param {Response} response
 * @param {Request} request
 */
const isValidResponse = (response, request) => {
  return (
    response &&
    (response.ok ||
      response.type === "opaque" ||
      (response.status === 404 && request.mode === "navigate"))
  );
};

/**
 * Delete previous caches if any and claim
 */
self.addEventListener("activate", event => {
  deleteCaches();
  return event.waitUntil(clients.claim());
});

self.addEventListener("install", event => {
  return event.waitUntil(
    caches
      .open(cacheName)
      .then(cache => {
        return cache.addAll(filesToCache);
      })
      .then(skipWaiting())
  );
});

self.addEventListener("fetch", event => {
  const request = event.request;
  if (request.method === "GET") {
    return event.respondWith(
      fetchAndCache(request)
        .then(response =>
          isValidResponse(response, request) ? response : caches.match(request)
        )
        .then(response => (response ? response : caches.match("/offline/")))
    );
  }
});
