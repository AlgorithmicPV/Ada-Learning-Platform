// Javascript code for community base page

const addaQuestionBtn = document.querySelector(".add-a-question-btn");
const postingQuestionWrapper = document.querySelector(
  ".posting-question-wrapper"
);
const closeBtnForPostingQuestionWrapper = document.querySelector(
  ".close-btn-posting-question-wrapper"
);

let isPostingQuestionShowing = false;

addaQuestionBtn.addEventListener("click", () => {
  if (!isPostingQuestionShowing) {
    postingQuestionWrapper.style.display = "flex";
    postingQuestionWrapper.style.opacity = 1;
    isPostingQuestionShowing = true;
  } else {
    postingQuestionWrapper.style.opacity = 0;
    postingQuestionWrapper.style.display = "none";
    isPostingQuestionShowing = false;
  }
});

closeBtnForPostingQuestionWrapper.addEventListener("click", () => {
  if (!isPostingQuestionShowing) {
    postingQuestionWrapper.style.display = "flex";
    postingQuestionWrapper.style.opacity = 1;
    isPostingQuestionShowing = true;
  } else {
    postingQuestionWrapper.style.opacity = 0;
    postingQuestionWrapper.style.display = "none";
    isPostingQuestionShowing = false;
  }
});
