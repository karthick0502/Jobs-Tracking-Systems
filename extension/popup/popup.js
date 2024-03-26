document.addEventListener('DOMContentLoaded', function () {
    var loginForm = document.getElementById('loginForm');
    var btnTracker = document.getElementById('btn-tracker');
    var loggedInMessage = document.getElementById('loggedInMessage');
  
    // Check if the user is already logged in
    chrome.storage.sync.get(['username', 'password'], function (result) {
      if (result.username && result.password) {
        // User is already logged in, hide the login form and show the logged-in message
        loginForm.style.display = 'none';
        loggedInMessage.style.display = 'block';
      }
    });
  
    btnTracker.addEventListener('click', function () {
      var username = document.getElementById('username').value;
      var password = document.getElementById('password').value;
  
      // Store the credentials securely using Chrome storage
      chrome.storage.sync.set({ username: username, password: password }, function () {
        console.log('Credentials stored successfully.');
        loginForm.style.display = 'none';
        loggedInMessage.style.display = 'block';
      });
    });
  
    function closePopup() {
      window.close();
    }
  
    window.closePopup = closePopup;
  });