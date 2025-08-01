// Javascript codes for the Login page

const hide_password_img = document.querySelector(".closed-eye-img-pass");
const show_password_img = document.querySelector(".eye-img-pass");

// Hides the password
hide_password_img.addEventListener("click", () => {
  hide_password_img.style.display = "none";
  show_password_img.style.display = "flex";
  document.getElementById("password").type = "password";
});

// Shows the password
show_password_img.addEventListener("click", () => {
  console.log("clicked");
  hide_password_img.style.display = "flex";
  show_password_img.style.display = "none";
  document.getElementById("password").type = "text";
});

const clearinput = () => {
  document.getElementById("search").value = "";
};

window.addEventListener("pageshow", clearinput);
