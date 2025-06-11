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

//close the error box when the user clicks the cross-icon
document
  .querySelector(".error-box-wrapper .cross-icon")
  .addEventListener("click", () => {
    document.querySelector(".error-box-wrapper").style.display = "none";
  });

// //close the error box when the user clicks the cross-icon
// document
//   .querySelector(".wrapper_error_fields_are_not_completed .cross-icon")
//   .addEventListener("click", () => {
//     document.querySelector(
//       ".wrapper_error_fields_are_not_completed"
//     ).style.display = "none";
//   });
