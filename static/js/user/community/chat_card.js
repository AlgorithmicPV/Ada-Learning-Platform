// Javascript code for the creating chat cards in the community page
// put this code in chat_card.js file to reduce the code repetition
// as I have to use this code in multiple pages

const discussionsContainer = document.querySelector(".discs-cont");

const canSaveIcon = `<svg xmlns="http://www.w3.org/2000/svg" id="Outline" viewBox="0 0 24 24" width="512" height="512"><path d="M20.137,24a2.8,2.8,0,0,1-1.987-.835L12,17.051,5.85,23.169a2.8,2.8,0,0,1-3.095.609A2.8,2.8,0,0,1,1,21.154V5A5,5,0,0,1,6,0H18a5,5,0,0,1,5,5V21.154a2.8,2.8,0,0,1-1.751,2.624A2.867,2.867,0,0,1,20.137,24ZM6,2A3,3,0,0,0,3,5V21.154a.843.843,0,0,0,1.437.6h0L11.3,14.933a1,1,0,0,1,1.41,0l6.855,6.819a.843.843,0,0,0,1.437-.6V5a3,3,0,0,0-3-3Z"/></svg>`;
const chatIcon = `<svg xmlns="http://www.w3.org/2000/svg" id="Layer_1" data-name="Layer 1" viewBox="0 0 24 24" width="512" height="512"><path d="M12.85,.03C9.38-.21,5.97,1.06,3.51,3.52,1.06,5.97-.21,9.38,.03,12.85c.43,6.25,5.84,11.15,12.31,11.15h6.66c2.94,0,5-2.4,5-5.85v-5.82C24,5.87,19.1,.46,12.85,.03Zm9.15,18.12c0,2.3-1.21,3.85-3,3.85h-6.66c-5.42,0-9.95-4.08-10.31-9.28-.2-2.9,.86-5.74,2.9-7.79,1.88-1.88,4.43-2.93,7.09-2.93,.23,0,.47,0,.7,.02,5.21,.36,9.28,4.89,9.28,10.31v5.82Z"/></svg>`;
const hasSavedIcon = `<svg xmlns="http://www.w3.org/2000/svg" id="Filled" viewBox="0 0 24 24" width="512" height="512"><path d="M2.849,23.55a2.954,2.954,0,0,0,3.266-.644L12,17.053l5.885,5.853a2.956,2.956,0,0,0,2.1.881,3.05,3.05,0,0,0,1.17-.237A2.953,2.953,0,0,0,23,20.779V5a5.006,5.006,0,0,0-5-5H6A5.006,5.006,0,0,0,1,5V20.779A2.953,2.953,0,0,0,2.849,23.55Z"/></svg>`;

// This dunction is used to send the selected chat id to the server to mark it as saved or unsaved
// and change the icon accordingly.
// This function works when the user clicks on the save button in the chat card
// toggleSaveURl is come from the community_all.html file
const toggleSave = (chatId, saveButton) => {
  fetch(toggleSaveUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ chatId: chatId }),
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

// Function to create a chat card in the community page
// Rough HTML structure of the chat card
{
  /* <div class="chat-card">
    <img src="{{ profilePicOfWriter}}" alt="" />
    <div class="chat-card-cont">
        <div class="chat-card-top-bar">
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
const createChatCard = (
  chatId,
  questionData,
  postedTimeData,
  writerName,
  profilePicOfWriter,
  nuOfAnswers,
  isSaved
) => {
  const chatCard = document.createElement("div");
  chatCard.classList.add("chat-card");

  const img = document.createElement("img");
  img.src = `${STATIC_BASE}${profilePicOfWriter}`;

  chatCard.appendChild(img);

  const chatCardCont = document.createElement("div");
  chatCardCont.classList.add("chat-card-cont");

  const chatCardTopBar = document.createElement("div");
  chatCardTopBar.classList.add("chat-card-top-bar");

  const writerAndTimeWrapper = document.createElement("div");

  const writer = document.createElement("p");
  writer.classList.add("writer");

  writer.innerText = writerName;

  writerAndTimeWrapper.appendChild(writer);

  const postedTime = document.createElement("p");
  postedTime.classList.add("time");

  postedTime.innerText = postedTimeData;

  writerAndTimeWrapper.appendChild(postedTime);

  chatCardTopBar.appendChild(writerAndTimeWrapper);

  const saveButton = document.createElement("button");
  saveButton.classList.add("save-btn");

  if (isSaved == "saved") {
    saveButton.innerHTML = hasSavedIcon;
  } else if (isSaved == "unsaved") {
    saveButton.innerHTML = canSaveIcon;
  }

  saveButton.setAttribute("data-chat-id", chatId);

  saveButton.addEventListener("click", () => {
    toggleSave(chatId, saveButton);
  });

  chatCardTopBar.appendChild(saveButton);

  chatCardCont.appendChild(chatCardTopBar);

  const question = document.createElement("p");
  question.classList.add("question");

  question.innerText = questionData;

  chatCardCont.appendChild(question);

  const numberOfAnswersWrapper = document.createElement("div");
  numberOfAnswersWrapper.classList.add("number-of-answers-wrapper");

  const numberOfAnswers = document.createElement("button");
  numberOfAnswers.classList.add("number-of-answers");
  numberOfAnswers.innerText = nuOfAnswers;
  numberOfAnswers.innerHTML += chatIcon;
  numberOfAnswers.setAttribute("data-chat-id", chatId);

  numberOfAnswersWrapper.appendChild(numberOfAnswers);

  chatCardCont.appendChild(numberOfAnswersWrapper);

  chatCard.appendChild(chatCardCont);

  discussionsContainer.appendChild(chatCard);
  console.log("created");
};

// Function to create a new chat card in the community page
// The reason to can't use the above function to create a new chat card is
// new chat cards created at the end of all other chat cards
// therefore I have to create a new function to create a new chat card only difference is discussionsContainer.prepend(chatCard);
// same html structure as above
const createNewChatCard = (
  chatId,
  questionData,
  postedTimeData,
  writerName,
  profilePicOfWriter,
  nuOfAnswers,
  isSaved
) => {
  const chatCard = document.createElement("div");
  chatCard.classList.add("chat-card");

  const img = document.createElement("img");
  img.src = `${STATIC_BASE}${profilePicOfWriter}`;

  chatCard.appendChild(img);

  const chatCardCont = document.createElement("div");
  chatCardCont.classList.add("chat-card-cont");

  const chatCardTopBar = document.createElement("div");
  chatCardTopBar.classList.add("chat-card-top-bar");

  const writerAndTimeWrapper = document.createElement("div");

  const writer = document.createElement("p");
  writer.classList.add("writer");

  writer.innerText = writerName;

  writerAndTimeWrapper.appendChild(writer);

  const postedTime = document.createElement("p");
  postedTime.classList.add("time");

  postedTime.innerText = postedTimeData;

  writerAndTimeWrapper.appendChild(postedTime);

  chatCardTopBar.appendChild(writerAndTimeWrapper);

  const saveButton = document.createElement("button");
  saveButton.classList.add("save-btn");

  if (isSaved == "saved") {
    saveButton.innerHTML = hasSavedIcon;
  } else if (isSaved == "unsaved") {
    saveButton.innerHTML = canSaveIcon;
  }

  saveButton.setAttribute("data-chat-id", chatId);

  saveButton.addEventListener("click", () => {
    toggleSave(chatId, saveButton);
  });

  chatCardTopBar.appendChild(saveButton);

  chatCardCont.appendChild(chatCardTopBar);

  const question = document.createElement("p");
  question.classList.add("question");

  question.innerText = questionData;

  chatCardCont.appendChild(question);

  const numberOfAnswersWrapper = document.createElement("div");
  numberOfAnswersWrapper.classList.add("number-of-answers-wrapper");

  const numberOfAnswers = document.createElement("button");
  numberOfAnswers.classList.add("number-of-answers");
  numberOfAnswers.innerText = nuOfAnswers;
  numberOfAnswers.innerHTML += chatIcon;
  numberOfAnswers.setAttribute("data-chat-id", chatId);

  numberOfAnswersWrapper.appendChild(numberOfAnswers);

  chatCardCont.appendChild(numberOfAnswersWrapper);

  chatCard.appendChild(chatCardCont);

  discussionsContainer.prepend(chatCard);
  console.log("created");
};

// Export the functions to use in other files
export { createChatCard, createNewChatCard };

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
