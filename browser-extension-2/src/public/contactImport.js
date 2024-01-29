/* eslint-disable no-undef */
/* eslint-disable no-prototype-builtins */
window.cloudsponge.init({
  skipContactsDisplay: false,
  skipSourceMenu: true,
  rootNodeSelector: '#cloudsponge-widget-container',
  beforeDisplayContacts: function (contacts, source, owner) {
    // eslint-disable-next-line no-undef
    // let appState = JSON.parse(localStorage.getItem("state"));
    let message = JSON.stringify({
      message: "contact-import",
      success: true,
      source,
      contacts: contacts,
    });
    
    window.top.postMessage(message, "*");
    window.parent.document.body.removeChild(window.frameElement);
  },
  afterImport: function (source, success) {
    // let messageAfterImport = 'some-message-after-import'
    // if (!success) {
      let message = JSON.stringify({
        message: "contact-after-import",
        success: false,
        source,
        contacts: [],
      });
      window.top.postMessage(message, "*");
      // window.parent.document.body.removeChild(window.frameElement);
    // }
  },
  beforeClosing: function () {
    let message = JSON.stringify({
      message: "contact-import",
      success: false,
      source: null,
      contacts: [],
    });
    window.top.postMessage(message, "*");
    window.parent.document.body.removeChild(window.frameElement);
  },
});

setTimeout(() => {
  cloudsponge.launch(localStorage.getItem("contact-import-source") || "gmail");
}, 100);
