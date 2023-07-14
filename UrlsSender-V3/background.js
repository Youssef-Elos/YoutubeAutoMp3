// Event listener for tab update
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  if (changeInfo.status === 'complete') {
    // Retrieve the URL from the active tab
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      var url = tabs[0].url;
      console.log('Tab URL:', url);

      // Send the URL to your Flask app
      sendUrlToFlaskApp(url);
    });
  }
});

// Function to send the URL to your Flask app
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
