// Javascript codes for the Signup page

function setupPasswordToggle(showSelector, hideSelector, inputId) {
  const showIcon = document.querySelector(showSelector);
  const hideIcon = document.querySelector(hideSelector);
  const input = document.getElementById(inputId);

  // Hide password (switch to dots)
  hideIcon.addEventListener("click", () => {
    hideIcon.style.display = "none";
    showIcon.style.display = "flex";
    input.type = "password";
  });

  // Show password (switch to text)
  showIcon.addEventListener("click", () => {
    hideIcon.style.display = "flex";
    showIcon.style.display = "none";
    input.type = "text";
  });
}

// Call the function for each password input field
setupPasswordToggle(".eye-img-pass", ".closed-eye-img-pass", "password");
setupPasswordToggle(
  ".eye-img-confirm-pass",
  ".closed-eye-img-confirm-pass",
  "confirm-password"
);
