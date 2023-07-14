// Function to extract the video URL
function extractVideoUrl() {
    var videoElement = document.querySelector('video');
    if (videoElement) {
      var videoUrl = videoElement.src;
      chrome.runtime.sendMessage({ action: 'videoUrl', url: videoUrl });
    }
  }
  
  // Call the function when the DOM is ready
  document.addEventListener('DOMContentLoaded', extractVideoUrl);
  