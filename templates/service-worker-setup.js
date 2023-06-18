/**
 * Manage service worker setup
 *
 * @constructor
 */
function ServiceWorkerSetup() {
    this.init();
}

/**
 * Initialise Service Worker
 */
/* eslint no-console: ["error", { allow: ["warn", "error"] }] */
ServiceWorkerSetup.prototype.init = function () {
    // Register the service worker
    if ("serviceWorker" in navigator) {
        navigator.serviceWorker.register("/service-worker.js")
            .then(function (registration) {
                // Registration was successful
                console.warn("ServiceWorker registration successful with scope: ", registration.scope);
            }).catch(function (err) {
                // registration failed :(
                console.error("ServiceWorker registration failed: ", err);
            });
    }
};

window.ServiceWorkerSetup = new ServiceWorkerSetup();
