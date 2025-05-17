document.addEventListener("DOMContentLoaded", function() {
    var images   = window.interestImages;
    var captions = window.interestCaptions;
    var idx      = 0;
    var slide    = document.getElementById("slide");
    var caption  = document.getElementById("caption");
  
    function show(i) {
      idx = (i + images.length) % images.length;
      slide.src    = images[idx];
      caption.textContent = captions[idx];
    }
  
    document.getElementById("next").onclick = function() { show(idx + 1); };
    document.getElementById("prev").onclick = function() { show(idx - 1); };
  
    var interval = setInterval(function() { show(idx + 1); }, 4000);
  
    // pause auto on hover, and show caption
    slide.addEventListener("mouseenter", function() {
      clearInterval(interval);
      caption.style.opacity = "1";
    });
    slide.addEventListener("mouseleave", function() {
      interval = setInterval(function() { show(idx + 1); }, 4000);
      caption.style.opacity = "0";
    });
  });
  