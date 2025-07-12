// Javascript code for the settings page

// This part of the code is for the give tha ability
// to edit the username and email input boc
const editButtons = document.querySelectorAll(".edit");
const userName = document.querySelector(".username");
const email = document.querySelector(".email");

// Intially set the editablity to false
let editable = false;

// As there are two edit buttons,
// I used forEach to add the event listener to both of them
editButtons.forEach((editButton) => {
  editButton.addEventListener("click", () => {
    if (editable == false) {
      userName.removeAttribute("readonly");
      email.removeAttribute("readonly");
      editable = true;
    } else {
      userName.setAttribute("readonly", true);
      email.setAttribute("readonly", true);
      editable = false;
    }
  });
});

// Function that shows the password
// Basically it changes the type of the input box
// and hides and shows relvant icons
const showPassword = (hideicon, showIcon, passwordBox) => {
  hideicon.style.display = "none";
  showIcon.style.display = "flex";
  passwordBox.type = "text";
};

// Function that shows the password
const HidePassword = (hideicon, showIcon, passwordBox) => {
  hideicon.style.display = "none";
  showIcon.style.display = "flex";
  passwordBox.type = "password";
};

// Call the above functions according to the icons
const HideCurrentPasswordIcon = document.querySelector(
  ".current-password-entry-wrapper .closed-eye-img-pass"
);
const ShowCurrentPasswordIcon = document.querySelector(
  ".current-password-entry-wrapper .eye-img-pass"
);
const currentPasswordBox = document.getElementById("currentPassword");

ShowCurrentPasswordIcon.addEventListener("click", () => {
  showPassword(
    ShowCurrentPasswordIcon,
    HideCurrentPasswordIcon,
    currentPasswordBox
  );
});

HideCurrentPasswordIcon.addEventListener("click", () => {
  HidePassword(
    HideCurrentPasswordIcon,
    ShowCurrentPasswordIcon,
    currentPasswordBox
  );
});

const HideNewPasswordIcon = document.querySelector(
  ".new-passwords-wrapper .closed-eye-img-pass"
);

const ShowNewPasswordIcon = document.querySelector(
  ".new-passwords-wrapper .eye-img-pass"
);

const newPasswordBox = document.getElementById("new-password");

ShowNewPasswordIcon.addEventListener("click", () => {
  showPassword(ShowNewPasswordIcon, HideNewPasswordIcon, newPasswordBox);
});

HideNewPasswordIcon.addEventListener("click", () => {
  HidePassword(HideNewPasswordIcon, ShowNewPasswordIcon, newPasswordBox);
});

const hideConfirmNewPasswordIcon = document.querySelector(
  ".confirm-new-password-entry-wrapper .closed-eye-img-pass"
);

const showConfirmNewPasswordIcon = document.querySelector(
  ".confirm-new-password-entry-wrapper .eye-img-pass"
);

const confirmNewPasswordBox = document.getElementById("confirm-new-password");

showConfirmNewPasswordIcon.addEventListener("click", () => {
  showPassword(
    showConfirmNewPasswordIcon,
    hideConfirmNewPasswordIcon,
    confirmNewPasswordBox
  );
});

hideConfirmNewPasswordIcon.addEventListener("click", () => {
  HidePassword(
    hideConfirmNewPasswordIcon,
    showConfirmNewPasswordIcon,
    confirmNewPasswordBox
  );
});

// This part gives the preview of what user has selected as his/her profile picture
// before updating the profile picture
const fileInput = document.getElementById("file");
const preview = document.getElementById("profilePreview");

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = () => {
      preview.src = reader.result;
    };
    reader.readAsDataURL(file);
  }
});

// This part is to count the number of stars user has selected
const starButtons = document.querySelectorAll(".star");

// An array to store clicked buttons
// I am using this array to count the number of stars user has selected
let clickedStarButtons = [];

// Icons for star buttons to change when user clicks on them
let colouredStarIcon = `<svg xmlns="http://www.w3.org/2000/svg" id="Filled" viewBox="0 0 24 24" width="512" height="512"><path d="M1.327,12.4,4.887,15,3.535,19.187A3.178,3.178,0,0,0,4.719,22.8a3.177,3.177,0,0,0,3.8-.019L12,20.219l3.482,2.559a3.227,3.227,0,0,0,4.983-3.591L19.113,15l3.56-2.6a3.227,3.227,0,0,0-1.9-5.832H16.4L15.073,2.432a3.227,3.227,0,0,0-6.146,0L7.6,6.568H3.231a3.227,3.227,0,0,0-1.9,5.832Z"/></svg>`;
let normalStarIcon = `<svg xmlns="http://www.w3.org/2000/svg" id="Outline" viewBox="0 0 24 24" width="512" height="512"><path d="M23.836,8.794a3.179,3.179,0,0,0-3.067-2.226H16.4L15.073,2.432a3.227,3.227,0,0,0-6.146,0L7.6,6.568H3.231a3.227,3.227,0,0,0-1.9,5.832L4.887,15,3.535,19.187A3.178,3.178,0,0,0,4.719,22.8a3.177,3.177,0,0,0,3.8-.019L12,20.219l3.482,2.559a3.227,3.227,0,0,0,4.983-3.591L19.113,15l3.56-2.6A3.177,3.177,0,0,0,23.836,8.794Zm-2.343,1.991-4.144,3.029a1,1,0,0,0-.362,1.116L18.562,19.8a1.227,1.227,0,0,1-1.895,1.365l-4.075-3a1,1,0,0,0-1.184,0l-4.075,3a1.227,1.227,0,0,1-1.9-1.365L7.013,14.93a1,1,0,0,0-.362-1.116L2.507,10.785a1.227,1.227,0,0,1,.724-2.217h5.1a1,1,0,0,0,.952-.694l1.55-4.831a1.227,1.227,0,0,1,2.336,0l1.55,4.831a1,1,0,0,0,.952.694h5.1a1.227,1.227,0,0,1,.724,2.217Z"/></svg>`;

// Gets  all the star buttons and add the function to change theeir icons and
// appends to the above array
// When user clicks the button, first it checks if the that button is in clickedStarButtons array
// If it is, it removes it from the array and changes the icon to normal star icon
// If it is not, it adds it to the array and changes the icon to filled star icon
starButtons.forEach((starButton) => {
  starButton.addEventListener("click", () => {
    if (clickedStarButtons.includes(starButton)) {
      clickedStarButtons.splice(clickedStarButtons.indexOf(starButton), 1);
      starButton.innerHTML = normalStarIcon;
    } else {
      clickedStarButtons.push(starButton);
      starButton.innerHTML = colouredStarIcon;
    }
  });
});

// Function to show the messages that comes from the server
// When the user fills the feedback form, the server sends a message to the client to inform if there are any errors or not
function showMessage(message, type = "info") {
  // Remove any existing box
  const existingBox = document.querySelector(".message-box");
  if (existingBox) existingBox.remove();

  // Create box
  const box = document.createElement("div");
  box.className = `message-box ${type}`;
  box.textContent = message;
  document.body.appendChild(box);

  // Fade out after 3 seconds
  setTimeout(() => {
    box.classList.add("fade-out");
    box.addEventListener("transitionend", () => box.remove());
  }, 3000);
}

// This part sends the users' feedback to the server
const feedBackForm = document.querySelector(".post-comment-section form");

feedBackForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const formData = new FormData(feedBackForm);
  formData.append("star", clickedStarButtons.length);

  fetch(sendFeedback, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      showMessage(data["message"]);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});

//close the error box when the user clicks the cross-icon
const crossIcon = document.querySelector(".error-box-wrapper .cross-icon");

if (crossIcon) {
  crossIcon.addEventListener("click", () => {
    document.querySelector(".error-box-wrapper").style.display = "none";
  });
}
