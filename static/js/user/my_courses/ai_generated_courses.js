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

const WarrningBox = document.querySelector(".warning-wrapper");
const WarningCloseBtn = document.querySelector(".warning-wrapper button");

WarningCloseBtn.addEventListener("click", () => {
  WarrningBox.style.display = "none";
  WarrningBox.style.opacity = 0;
  sessionStorage.setItem("usersawmsg", "yes");
});

const sendButton = document.querySelector(
  ".new-course-input-wrapper .send-btn"
);
const userInputBox = document.querySelector(".user-input");
const loader = document.querySelector(".loader");
const newAiCoursesForm = document.querySelector(".new-ai-courses-form");

const generatingCourse = async () => {
  if (userInputBox.value != "" && userInputBox.value != " ") {
    let userInput = userInputBox.value;
    userInputBox.value = "";
    loader.style.opacity = 1;
    loader.style.visibility = "visible";

    newAiCoursesForm.style.opacity = 0;
    newAiCoursesForm.style.visibility = "hidden";

    BtnAddnewAi.style.opacity = 1;
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
      console.log("loading...");
      console.log(result);
      if (result.redirect_url) {
        console.log("done");
        window.location.href = result.redirect_url;
      }
    } catch (error) {
      console.error(error);
    }
  }
};

sendButton.addEventListener("click", () => {
  generatingCourse();
});
