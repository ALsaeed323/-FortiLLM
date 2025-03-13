// Smooth scroll for in-page links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });
  
  // Typing Effect
  const text = "Fortifying LLMs Against Prompt Injections";
  const typingElement = document.getElementById("typing-text");
  let index = 0;
  
  function type() {
    if (index < text.length) {
      typingElement.innerHTML += text.charAt(index);
      index++;
      setTimeout(type, 100); // Adjust speed (milliseconds) here
    }
  }
  
  // Start typing effect after page load
  window.onload = function() {
    type();
  };

// Existing smooth scroll and typing effect code...

// Password visibility toggle
document.addEventListener('DOMContentLoaded', function() {
    const passwordInputs = document.querySelectorAll('.input-group input[type="password"]');
    const eyeIcons = document.querySelectorAll('.input-group .bi-eye-slash');
  
    eyeIcons.forEach((icon, index) => {
      icon.addEventListener('click', function() {
        const input = passwordInputs[index];
        if (input.type === 'password') {
          input.type = 'text';
          icon.classList.remove('bi-eye-slash');
          icon.classList.add('bi-eye');
        } else {
          input.type = 'password';
          icon.classList.remove('bi-eye');
          icon.classList.add('bi-eye-slash');
        }
      });
    });
  });