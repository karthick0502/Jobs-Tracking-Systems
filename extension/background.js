// ...

// Send a message to the content script to start tracking job applications
function startTracking() {
    chrome.storage.sync.get(['username', 'password'], function (result) {
      if (result.username && result.password) {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          const activeTab = tabs[0];
          chrome.tabs.sendMessage(activeTab.id, {
            action: 'startTracking',
            username: result.username,
            password: result.password
          });
        });
      } else {
        console.log('Credentials not found. Please log in.');
      }
    });
  }
  
  // ...