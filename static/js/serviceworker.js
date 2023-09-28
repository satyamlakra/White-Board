// var staticCacheName = 'djangopwa-v1';

 
// self.addEventListener("install", function (e) {
//   e.waitUntil(
//     caches.open(staticCacheName).then(function (cache) {
//       return cache.addAll(["/"]);
//     })
//   );
// });
 
// self.addEventListener("fetch", function (event) {
//   console.log(event.request.url);
 
//   event.respondWith(
//     caches.match(event.request).then(function (response) {
//       return response || fetch(event.request);
//     })
//   );
// });



var staticCacheName = "djangopwa-v1" + new Date().getTime();
var filesToCache = [
    '/offline/',
    '/static/css/django-pwa-app.css',
    '/static/AppImages/android/android-launchericon-72-72.png',
    '/static/AppImages/android/android-launchericon-96-96.png',
    '/static/AppImages/ios/128.png',
    '/static/AppImages/ios/144.png',
    '/static/AppImages/ios/152.png',
    '/static/wifi-disconnected.png',
    '/static/images/icons/pexels-zhang-kaiyv-1138369.jpg',
    '/static/AppImages/ios/512.png',
    
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(async cache => {
                return await cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

self.addEventListener("fetch", event => {
  event.respondWith(
      caches.match(event.request)
          .then(response => {
              return response || fetch(event.request);
          })
          .catch(() => {
              return caches.match('/offline/');
          })
  )
});
// self.addEventListener("fetch", function (event) {
//   console.log(event.request.url);
 
//   event.respondWith(
//     caches.match(event.request).then(function (response) {
//       return response || fetch(event.request);
//     })
//   );
// });


// This is the "Offline page" service worker

// importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

importScripts("https://storage.googleapis.com/workbox-cdn/releases/6.0.2/workbox-sw.js");
	            if(workbox.googleAnalytics){
                  try{
                    workbox.googleAnalytics.initialize();
                  } catch (e){ console.log(e.message); }
                }