// Javascript file for to handle the messages such as error, warnings, etc...
const AlertBoxWrapper = document.querySelector(".alert-box-wrapper");

export const showAlertMessages = (alertType, alertMessage) => {
  const AlertBox = document.createElement("div");
  AlertBox.classList.add("alert-box", `${alertType}-alert-box`);

  const alertMessageTxt = document.createElement("p");
  alertMessageTxt.classList.add("alert-message-text");
  alertMessageTxt.innerText = alertMessage;

  AlertBox.appendChild(alertMessageTxt);
  AlertBoxWrapper.appendChild(AlertBox);

  setTimeout(() => {
    AlertBox.style.opacity = "1";
    AlertBox.style.transform = "translateX(0)";
  }, 400); // Match transition duration

  // Slide-out after 4 seconds
  setTimeout(() => {
    AlertBox.style.opacity = "0";
    AlertBox.style.transform = "translateX(100%)"; // Slide back to right

    // Remove after animation
    setTimeout(() => {
      AlertBox.remove();
    }, 400); // Match transition duration
  }, 4000);
};
