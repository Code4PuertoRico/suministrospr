const displayOfflineHeader = () => {
  const template = document.getElementById("offline-header-template");
  if (template) {
    document.body.prepend(template.content.cloneNode(true));
  }
};

window.addEventListener("load", function() {
  if (!navigator.onLine) {
    displayOfflineHeader();
  }

  window.addEventListener("offline", event => {
    displayOfflineHeader();
  });

  window.addEventListener("online", event => {
    const offlineHeader = document.getElementById("offline-header");
    if (offlineHeader) {
      document.body.removeChild(offlineHeader);
    }
  });
});
