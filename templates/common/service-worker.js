let cacheName = "suministrospr-cache";
let dynamicCacheName = "dynamic-cache";
// For now only root and offline since it will dynamically add the other urls
let filesToCache = ["/", "/offline/"];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(cacheName).then(cache => {
      return cache.addAll(filesToCache);
    })
  );
});

// If request is not in cache fetch the url and dynamically add the response to the cache
self.addEventListener("fetch", event => {
  event.respondWith(
    caches
      .match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request).then(response => {
          const clonedResponse = response.clone();
          caches.open(dynamicCacheName).then(cache => {
            cache.put(event.request.url, clonedResponse);
          });
          return response;
        });
      })
      .catch(() => {
        return caches.match("/offline/"); // WIP - update template indicating user is offline
      })
  );
});
