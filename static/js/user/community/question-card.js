// Javascript code for the creating question cards in the community page
// put this code in question_card.js file to reduce the code repetition
// as I have to use this code in multiple pages

const discussionsContainer = document.querySelector(".discs-cont");

const questionIcon = `<svg xmlns="http://www.w3.org/2000/svg" id="Layer_1" data-name="Layer 1" viewBox="0 0 24 24" width="512" height="512"><path d="M12.85,.03C9.38-.21,5.97,1.06,3.51,3.52,1.06,5.97-.21,9.38,.03,12.85c.43,6.25,5.84,11.15,12.31,11.15h6.66c2.94,0,5-2.4,5-5.85v-5.82C24,5.87,19.1,.46,12.85,.03Zm9.15,18.12c0,2.3-1.21,3.85-3,3.85h-6.66c-5.42,0-9.95-4.08-10.31-9.28-.2-2.9,.86-5.74,2.9-7.79,1.88-1.88,4.43-2.93,7.09-2.93,.23,0,.47,0,.7,.02,5.21,.36,9.28,4.89,9.28,10.31v5.82Z"/></svg>`;
const hasSavedIcon = `<svg xmlns="http://www.w3.org/2000/svg" id="Filled" viewBox="0 0 24 24" width="512" height="512"><path d="M2.849,23.55a2.954,2.954,0,0,0,3.266-.644L12,17.053l5.885,5.853a2.956,2.956,0,0,0,2.1.881,3.05,3.05,0,0,0,1.17-.237A2.953,2.953,0,0,0,23,20.779V5a5.006,5.006,0,0,0-5-5H6A5.006,5.006,0,0,0,1,5V20.779A2.953,2.953,0,0,0,2.849,23.55Z"/></svg>`;
const canSaveIcon = `<svg xmlns="http://www.w3.org/2000/svg" id="Outline" viewBox="0 0 24 24" width="512" height="512"><path d="M20.137,24a2.8,2.8,0,0,1-1.987-.835L12,17.051,5.85,23.169a2.8,2.8,0,0,1-3.095.609A2.8,2.8,0,0,1,1,21.154V5A5,5,0,0,1,6,0H18a5,5,0,0,1,5,5V21.154a2.8,2.8,0,0,1-1.751,2.624A2.867,2.867,0,0,1,20.137,24ZM6,2A3,3,0,0,0,3,5V21.154a.843.843,0,0,0,1.437.6h0L11.3,14.933a1,1,0,0,1,1.41,0l6.855,6.819a.843.843,0,0,0,1.437-.6V5a3,3,0,0,0-3-3Z"/></svg>`;

// This dunction is used to send the selected question id to the server to mark it as saved or unsaved
// and change the icon accordingly.
// This function works when the user clicks on the save button in the question card
// toggleSaveURl is come from the community_all.html file
const toggleSave = (questionId, saveButton) => {
  fetch(toggleSaveUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ questionId: questionId }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("success:", data);
      if (data["isSave"] == "yes") {
        saveButton.innerHTML = hasSavedIcon;
      } else if (data["isSave"] == "no") {
        saveButton.innerHTML = canSaveIcon;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

const openTheDiscussion = (questionId) => {
  fetch(questionGateUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ questionId: questionId }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.redirect_url) {
        window.location.href = data.redirect_url;
      }
    })
    .catch((error) => {
      console.error("Error: ", error);
    });
};

// Function to create a question card in the community page
// Rough HTML structure of the question card
{
  /* <div class="question-card">
    <img src="{{ profilePicOfWriter}}" alt="" />
    <div class="question-card-cont">
        <div class="question-card-top-bar">
            <div>
                <p class="writer">{{ writerName }}</p>
                <p class="time">{{ postedTimeData }}</p>
            </div>
            <button class="save-btn"></button>
        </div>
        <p class="question">{{ questionData }}</p>
        <div class="number-of-answers-wrapper">
            <p class="number-of-answers">{{ nuOfAnswers }}</p>
        </div>
    </div>
</div> */
}
const createQuestionCard = (
  questionId,
  questionData,
  postedTimeData,
  writerName,
  profilePicOfWriter,
  nuOfAnswers,
  isSaved,
  isFirstCall
) => {
  const questionCard = document.createElement("div");
  questionCard.classList.add("question-card");

  const img = document.createElement("img");
  img.src = `${profilePicOfWriter}`;

  questionCard.appendChild(img);

  const questionCardCont = document.createElement("div");
  questionCardCont.classList.add("question-card-cont");

  const questionCardTopBar = document.createElement("div");
  questionCardTopBar.classList.add("question-card-top-bar");

  const writerAndTimeWrapper = document.createElement("div");

  const writer = document.createElement("p");
  writer.classList.add("writer");

  writer.innerText = writerName;

  writerAndTimeWrapper.appendChild(writer);

  const postedTime = document.createElement("p");
  postedTime.classList.add("time");

  postedTime.innerText = postedTimeData;

  writerAndTimeWrapper.appendChild(postedTime);

  questionCardTopBar.appendChild(writerAndTimeWrapper);

  const saveButton = document.createElement("button");
  saveButton.classList.add("save-btn");

  if (isSaved == "saved") {
    saveButton.innerHTML = hasSavedIcon;
  } else if (isSaved == "unsaved") {
    saveButton.innerHTML = canSaveIcon;
  }

  saveButton.setAttribute("data-question-id", questionId);

  saveButton.addEventListener("click", () => {
    toggleSave(questionId, saveButton);
  });

  questionCardTopBar.appendChild(saveButton);

  questionCardCont.appendChild(questionCardTopBar);

  const question = document.createElement("p");
  question.classList.add("question");

  question.innerText = questionData;

  questionCardCont.appendChild(question);

  const numberOfAnswersWrapper = document.createElement("div");
  numberOfAnswersWrapper.classList.add("number-of-answers-wrapper");

  const numberOfAnswers = document.createElement("button");
  numberOfAnswers.classList.add("number-of-answers");
  numberOfAnswers.innerText = nuOfAnswers;
  numberOfAnswers.innerHTML += questionIcon;
  numberOfAnswers.addEventListener("click", () => {
    openTheDiscussion(questionId);
  });

  numberOfAnswersWrapper.appendChild(numberOfAnswers);

  questionCardCont.appendChild(numberOfAnswersWrapper);

  questionCard.appendChild(questionCardCont);
  if (isFirstCall) {
    discussionsContainer.appendChild(questionCard);
  } else {
    discussionsContainer.prepend(questionCard);
  }
};


// Export the functions to use in other files
export { createQuestionCard };

const adjustWidhtOfQuestion = () => {
  if (window.innerWidth < 1280) {
    let style = document.createElement("style");
    style.innerHTML = `
      .question {
          width: ${window.innerWidth - 200}px;
        }
      `;
    document.head.appendChild(style);
  } else {
    let style = document.createElement("style");
    style.innerHTML = `
      .question {
          width: 90%;
        }
      `;
    document.head.appendChild(style);
  }
};

window.addEventListener("load", adjustWidhtOfQuestion);
window.addEventListener("resize", adjustWidhtOfQuestion);
