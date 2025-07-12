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

//close the error box when the user clicks the cross-icon
const crossIcon = document.querySelector(".error-box-wrapper .cross-icon");

if (crossIcon) {
  crossIcon.addEventListener("click", () => {
    document.querySelector(".error-box-wrapper").style.display = "none";
  });
}

const clearinput = () => {
  document.getElementById("search").value = "";
};

window.addEventListener("pageshow", clearinput);
