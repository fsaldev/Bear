

(chrome as any).action.onClicked.addListener((tab: any) => {
  setupWebSocket(tab)
});

// chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
//   setupWebSocket(tab)
// });

// (chrome as any).action.onClicked.addListener((tab: any) => {
//   chrome.tabs.sendMessage(tab.id, { action: 'websocket', data: {} });
// });

let reconnectAttempts = 0;
let lastMessageReceivedTime = Date.now();

async function setupWebSocket(tab: any) {
  console.log(tab.url)
  let socket: any;
  let checkInterval: NodeJS.Timeout | undefined;
  try {
    socket = new WebSocket('ws://localhost:9002');
    console.log("creating socket");
  } catch (error) {
    console.error('Failed to create WebSocket:', error);
    scheduleReconnect(tab);
    return;
  }

  socket.onopen = () => {
    console.log('WebSocket connection established');
    //socket.send('connected');
    reconnectAttempts = 0;

    if (checkInterval) {
      clearInterval(checkInterval);
    }
    checkInterval = setInterval(() => {
      // If it's been more than 10 seconds since the last message, send a ping
      if (Date.now() - lastMessageReceivedTime > 10000 && socket.readyState === WebSocket.OPEN) {
        socket.send('ping');
      }
    }, 1000); // Checking every second
  };

  socket.onmessage = (event: any) => {
    lastMessageReceivedTime = Date.now();
    console.log(`Received message from server: ${event.data}`);
    const data = JSON.parse(event.data);


    if (data.action === "ack") {
      console.log("send connected");
      //socket.send("connected");
    } else {
      chrome.tabs.sendMessage(tab.id, { action: data.action, data: data.payload });
    }

  };

  socket.onclose = (event: any) => {
    console.log(`WebSocket connection closed with code ${event.code}`);
    if (checkInterval) {
      clearInterval(checkInterval);
      checkInterval = undefined;
    }
    //scheduleReconnect(tab);
  };

  socket.onerror = (error: any) => {
    console.error('WebSocket error:', error);
    if (checkInterval) {
      clearInterval(checkInterval);
      checkInterval = undefined;
    }
    scheduleReconnect(tab);
  };

  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'sendMessage') {
      console.log('Message received:', request.action);
      try {
        socket.send(request.message);
      } catch (error) {
        console.error('Failed to send message:', error);
      }
    }
  });

  return socket;
}

function scheduleReconnect(tab: any) {
  const delay = Math.pow(2, reconnectAttempts) * 100;
  console.log(`Scheduling reconnection in ${delay} ms...`);
  setTimeout(() => setupWebSocket(tab), delay);
  reconnectAttempts++;
}



const intervalInSeconds = 10;

chrome.alarms.create('keepTabActive', { periodInMinutes: intervalInSeconds / 60 });

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'keepTabActive') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        const activeTab = tabs[0];
        if (activeTab.id) {
          chrome.tabs.update(activeTab.id, { active: true });
        }
      }
    });
  }
});


chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === 'MakeCurrentTab') {
    
    console.log('hello from background script');
    setTimeout(function () {
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const currentTabId = tabs[0]?.id;

        if (currentTabId) {
          chrome.tabs.reload(currentTabId, {}, function () {
            console.log('Tab refreshed');
            sendResponse(); 
          });
        } else {
          console.log('Tab is not present');
        }
      });
    }, 5000);
  }
});

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === 'CloseTab') {
    
    console.log('hello from background script');
    setTimeout(function () {
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const currentTabId = tabs[0]?.id;

        if (currentTabId) {
          chrome.tabs.remove(currentTabId, function () {
            console.log('Tab closed');
            sendResponse(); 
          });
        }
        console.log('Tab is not present');
      });
    }, 5000); 
  }
});

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === 'OpenURLInCurrentTab') {
    const tabId = sender.tab?.id;
    if (tabId) {
      chrome.tabs.update(tabId, { url: message.url });
    }
  }
});

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === 'clearCookies') {
    // Query all cookies
    chrome.cookies.getAll({}, function (cookies) {
      // Iterate through cookies and remove each one
      for (const cookie of cookies) {
        console.log(cookie)
        chrome.cookies.remove({
          url: `https://${cookie.domain}${cookie.path}`,
          name: cookie.name,
        });
      }

      // Send a message to the content script to confirm that cookies are cleared
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        if (tabs.length > 0 && tabs[0].id) {
          chrome.tabs.sendMessage(tabs[0].id, { action: 'sendMessage', message: 'Cookies cleared' });
          console.log('Cookies cleared')
        }
      });
    });
  }
});

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === 'clearAllSiteData') {
    const removalOptions = {
      "since": 0 // Clear all data
    };

    // Remove browsing history, cache, images, and files for all URLs
    chrome.browsingData.remove(removalOptions, {
      "history": true, // Clear browsing history
      "cache": true, // Clear cache
      "downloads": true, // Clear download history
      "formData": true, // Clear saved form data
      "passwords": true, // Clear saved passwords
      "pluginData": true, // Clear plugin data
      "cookies": true, // Clear cookies
      "indexedDB": true, // Clear IndexedDB data
      "fileSystems": true, // Clear File System data
      "serviceWorkers": true, // Clear Service Worker data
      "appcache": true // Clear AppCache data
      // You can include or exclude other data types as needed
    }, function () {
      // Send a message to the content script to confirm that all site data is cleared
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        if (tabs.length > 0 && tabs[0].id) {
          chrome.tabs.sendMessage(tabs[0].id, { action: 'sendMessage', message: 'All site data cleared' });
          console.log('All site data cleared');
        }
      });
    });
  }
});

















