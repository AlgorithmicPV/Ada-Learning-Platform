// Javascript codes for the Signup page

const hide_password_img = document.querySelector(".closed-eye-img-pass");
const show_password_img = document.querySelector(".eye-img-pass");

const hide_confirm_password_img = document.querySelector(
  ".closed-eye-img-confirm-pass"
);
const open_confirm_password_img = document.querySelector(
  ".eye-img-confirm-pass"
);

// Hides the password
hide_password_img.addEventListener("click", () => {
  hide_password_img.style.display = "none";
  show_password_img.style.display = "flex";
  document.getElementById("password").type = "password";
});

// Shows the password
show_password_img.addEventListener("click", () => {
  hide_password_img.style.display = "flex";
  show_password_img.style.display = "none";
  document.getElementById("password").type = "text";
});

// Hides the confirm password
hide_confirm_password_img.addEventListener("click", () => {
  hide_confirm_password_img.style.display = "none";
  open_confirm_password_img.style.display = "flex";
  document.getElementById("confirm-password").type = "password";
});

// Shows the confirm password
open_confirm_password_img.addEventListener("click", () => {
  hide_confirm_password_img.style.display = "flex";
  open_confirm_password_img.style.display = "none";
  document.getElementById("confirm-password").type = "text";
});

const clearinput = () => {
  document.getElementById("search").value = "";
};

window.addEventListener("pageshow", clearinput);
