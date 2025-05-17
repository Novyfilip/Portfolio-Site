// static/js/script.js

document.addEventListener("DOMContentLoaded", function() {
    const toggleBtn = document.getElementById("dark-toggle");
  
    // set initial icon based on current mode
    toggleBtn.textContent = 
      document.body.classList.contains("dark-mode") ? "☀️" : "🌙";
  
    toggleBtn.addEventListener("click", function() {
      document.body.classList.toggle("dark-mode");
  
      // swap icon
      if (document.body.classList.contains("dark-mode")) {
        toggleBtn.textContent = "☀️";
      } else {
        toggleBtn.textContent = "🌙";
      }
    });
  });
  
  // simple form validation 
  function validateForm() {
    const name = document.getElementById("name").value;
    const msg  = document.getElementById("message").value;
    if (!name || !msg) {
      alert("Please fill out both fields!");
      return false;
    }
    return true;
  }
  