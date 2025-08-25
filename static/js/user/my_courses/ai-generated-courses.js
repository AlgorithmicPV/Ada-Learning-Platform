// JavaScript code for the AI generated courses page (Page that allows users to generate new courses using AI and shows the generated courses)
import { showAlertMessages } from "./../../../js/message-handler.js";

const BtnAddnewAi = document.querySelector(".add-ai-generated-courses-btn");
const newCourseInputWrapper = document.querySelector(
  ".new-course-input-wrapper"
);

let newCourseInputWrapperShowing = false;

const hideCourseInputWrapper = () => {
  newCourseInputWrapperShowing = false;
  newCourseInputWrapper.style.visibility = "hidden";
  BtnAddnewAi.style.transform = "rotate(0)";
  newCourseInputWrapper.style.opacity = 0;
};
BtnAddnewAi.addEventListener("click", () => {
  if (!newCourseInputWrapperShowing) {
    newCourseInputWrapper.style.visibility = "visible";
    BtnAddnewAi.style.transform = "rotate(-45deg)";
    newCourseInputWrapper.style.opacity = 1;
    newCourseInputWrapperShowing = true;
  } else {
    hideCourseInputWrapper();
  }
});

const WarningBox = document.querySelector(".warning-wrapper");
const WarningCloseBtn = document.querySelector(".warning-wrapper button");

// If user clicks the close button on the warning box, hide the box and set in session storage that the user has seen the message
// This is to prevent the box from showing up again when the user refreshes the page
WarningCloseBtn.addEventListener("click", () => {
  WarningBox.style.display = "none";
  WarningBox.style.opacity = 0;
  sessionStorage.setItem("usersawmsg", "yes");
});

const sendButton = document.querySelector(
  ".new-course-input-wrapper .send-btn"
);
const userInputBox = document.querySelector(".user-input");
const loader = document.querySelector(".loader");
const newAiCoursesForm = document.querySelector(".new-ai-courses-form");

// Function that passes the user input to the backend to generate a course
// and redirects the user to the page that shows all generated courses (same page)
const generatingCourse = async () => {
  if (userInputBox.value != "" && userInputBox.value != " ") {
    let userInput = userInputBox.value;

    // Clear the user input box after getting the input
    userInputBox.value = "";

    // Show the loader, to indicate that the request is being processed
    loader.style.opacity = 1;
    loader.style.visibility = "visible";

    // Hide the user input box, to prevent multiple clicks
    newAiCoursesForm.style.opacity = 0;
    newAiCoursesForm.style.visibility = "hidden";

    // Hide the add new AI button, to prevent multiple clicks
    BtnAddnewAi.style.opacity = 0;
    BtnAddnewAi.style.visibility = "hidden";

    const sendUserInput = {
      userInput: userInput,
    };
    try {
      const response = await fetch(ai_course_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(sendUserInput),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      if (result.error) {
        hideCourseInputWrapper()
        BtnAddnewAi.style.opacity = 1;
        BtnAddnewAi.style.visibility = "visible";
        newAiCoursesForm.style.opacity = 1;
        newAiCoursesForm.style.visibility = "visible";
        loader.style.opacity = 0;
        loader.style.visibility = "hidden";
        showAlertMessages("error", result.error)
      }
      if (result.redirect_url) {
        window.location.href = result.redirect_url;
      }
    } catch (error) {
      console.error(error);
    }
  }
};

// Add event listener to the send button to call the generatingCourse function
sendButton.addEventListener("click", () => {
  generatingCourse();
});
