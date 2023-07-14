document.addEventListener('DOMContentLoaded', function() {
  // Get the current URL and display it
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    var url = tabs[0].url;
    document.getElementById('urlContainer').textContent = url;
    console.log(url);
  });

  // Auto send toggle switch
  var autoSendToggle = document.getElementById('autoSendToggle');
  autoSendToggle.addEventListener('change', function() {
    var status = autoSendToggle.checked ? 'ON' : 'OFF';
    document.getElementById('switchStatus').textContent = status;
  });

  // Send URL button click event
  var sendButton = document.getElementById('sendButton');
  sendButton.addEventListener('click', sendUrl);
});

function sendUrl() {
  // Get the current URL
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    var url = tabs[0].url;
    console.log(url);

    // Send the URL to the Flask app
    sendUrlToFlaskApp(url);
  });
}

function sendUrlToFlaskApp(url) {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://localhost:5000/download', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
      console.log('URL sent successfully to Flask app');
    }
  };
  var formData = 'url=' + encodeURIComponent(url);
  xhr.send(formData);
}
