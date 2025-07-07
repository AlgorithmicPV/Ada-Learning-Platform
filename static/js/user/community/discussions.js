// Javascript code for the discussions page in the community section

const hassaveIcon = `<svg xmlns="http://www.w3.org/2000/svg" id="Filled" viewBox="0 0 24 24" width="512" height="512"><path d="M2.849,23.55a2.954,2.954,0,0,0,3.266-.644L12,17.053l5.885,5.853a2.956,2.956,0,0,0,2.1.881,3.05,3.05,0,0,0,1.17-.237A2.953,2.953,0,0,0,23,20.779V5a5.006,5.006,0,0,0-5-5H6A5.006,5.006,0,0,0,1,5V20.779A2.953,2.953,0,0,0,2.849,23.55Z"/></svg>`;
const canSaveIcon = `<svg xmlns="http://www.w3.org/2000/svg" id="Outline" viewBox="0 0 24 24" width="512" height="512"><path d="M20.137,24a2.8,2.8,0,0,1-1.987-.835L12,17.051,5.85,23.169a2.8,2.8,0,0,1-3.095.609A2.8,2.8,0,0,1,1,21.154V5A5,5,0,0,1,6,0H18a5,5,0,0,1,5,5V21.154a2.8,2.8,0,0,1-1.751,2.624A2.867,2.867,0,0,1,20.137,24ZM6,2A3,3,0,0,0,3,5V21.154a.843.843,0,0,0,1.437.6h0L11.3,14.933a1,1,0,0,1,1.41,0l6.855,6.819a.843.843,0,0,0,1.437-.6V5a3,3,0,0,0-3-3Z"/></svg>`;

// This dunction is used to send the selected answer id to the server to mark it as like or unlike
// and change the icon accordingly.
// This function works when the user clicks on the save button in the answer card
// toggleSaveURl is come from the html file
// answerId is also cime from the html file
const toggleSave = (questionId) => {
  fetch(toggleSaveUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ questionId: questionId }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data["isSave"] == "yes") {
        saveButton.innerHTML = hassaveIcon;
      } else if (data["isSave"] == "no") {
        saveButton.innerHTML = canSaveIcon;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

const saveButton = document.querySelector(".save-btn");
saveButton.addEventListener("click", () => {
  toggleSave(questionId);
});

// This part of the code pass the user input (Answer) to the server
// addAnswersUrl is come from the html file
const userReplyInputBox = document.querySelector(".user-answer-input-box");
const sendUserAnswerBtn = document.querySelector(".send-user-answer-btn");

const addAnswers = () => {
  let userAnswer = userReplyInputBox.value;
  // After getting the user input, it will set to empty
  // So user doent have to clean the input box manually
  userReplyInputBox.value = "";
  fetch(addAnswersUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ userAnswer: userAnswer }),
  }).catch((error) => {
    console.log("Error: ", error);
  });
};

// Calls the addAnswers function when the user clicks on the send button
sendUserAnswerBtn.addEventListener("click", () => {
  addAnswers();
});

// This part of the code is used to get the answers from the server
// getAnswersUrl is come from the html file
const discussionsContainer = document.querySelector(".discs-cont");
const nestedBranch = document.querySelector(".nested li");
const canLikeicon = `<svg xmlns="http://www.w3.org/2000/svg" id="Outline" viewBox="0 0 24 24" width="512" height="512"><path d="M22.773,7.721A4.994,4.994,0,0,0,19,6H15.011l.336-2.041A3.037,3.037,0,0,0,9.626,2.122L7.712,6H5a5.006,5.006,0,0,0-5,5v5a5.006,5.006,0,0,0,5,5H18.3a5.024,5.024,0,0,0,4.951-4.3l.705-5A5,5,0,0,0,22.773,7.721ZM2,16V11A3,3,0,0,1,5,8H7V19H5A3,3,0,0,1,2,16Zm19.971-4.581-.706,5A3.012,3.012,0,0,1,18.3,19H9V7.734a1,1,0,0,0,.23-.292l2.189-4.435A1.07,1.07,0,0,1,13.141,2.8a1.024,1.024,0,0,1,.233.84l-.528,3.2A1,1,0,0,0,13.833,8H19a3,3,0,0,1,2.971,3.419Z"/></svg>`;
const hasLikeIcon = `<svg xmlns="http://www.w3.org/2000/svg" id="Filled" viewBox="0 0 24 24" width="512" height="512"><path d="M22.773,7.721A4.994,4.994,0,0,0,19,6H15.011l.336-2.041A3.037,3.037,0,0,0,9.626,2.122L8,5.417V21H18.3a5.024,5.024,0,0,0,4.951-4.3l.705-5A4.994,4.994,0,0,0,22.773,7.721Z"/><path d="M0,11v5a5.006,5.006,0,0,0,5,5H6V6H5A5.006,5.006,0,0,0,0,11Z"/></svg>`;

// This function is used to toggle the like and unlike functionality of the answers
// It will send the answerId to the server and get the response back
// depend on that change the Like button icon and the number of likes
// toggleLikeUrl is come from the html file
const toggleLike = (answerId, likeButton, numberOfLikes) => {
  fetch(toggleLikeUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ answerId: answerId }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data["like"] == "yes") {
        likeButton.innerHTML = hasLikeIcon;
        numberOfLikes.innerText = data["nu_likes"];
      } else if (data["like"] == "no") {
        likeButton.innerHTML = canLikeicon;
        numberOfLikes.innerText = data["nu_likes"];
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

// This function creates the answer card
const createAnswerCard = (
  answerId,
  content,
  answeredTime,
  writerName,
  profilePicOfWriter,
  nuOfLikes,
  isLiked
) => {
  const ulElement = document.createElement("ul");

  const liElement = document.createElement("li");

  const answerCard = document.createElement("div");
  answerCard.classList.add("answer-card");

  const img = document.createElement("img");
  img.src = `${STATIC_BASE}${profilePicOfWriter}`;

  answerCard.appendChild(img);

  const answerCardCont = document.createElement("div");
  answerCardCont.classList.add("answer-card-cont");

  const answerCardTopBar = document.createElement("div");
  answerCardTopBar.classList.add("answer-card-top-bar");

  const writerAndTimeWrapper = document.createElement("div");

  const writer = document.createElement("p");
  writer.classList.add("writer");

  writer.innerText = writerName;

  writerAndTimeWrapper.appendChild(writer);

  const postedTime = document.createElement("p");
  postedTime.classList.add("time");

  postedTime.innerText = answeredTime;

  writerAndTimeWrapper.appendChild(postedTime);

  answerCardTopBar.appendChild(writerAndTimeWrapper);

  answerCardCont.appendChild(answerCardTopBar);

  const answer = document.createElement("div");
  answer.classList.add("answer");

  answer.innerHTML = content;

  answerCardCont.appendChild(answer);

  const numberOfLikesWrapper = document.createElement("div");
  numberOfLikesWrapper.classList.add("number-of-likes-wrapper");

  const likeButton = document.createElement("button");
  likeButton.classList.add("like-btn");

  if (isLiked == "like") {
    likeButton.innerHTML = hasLikeIcon;
  } else if (isLiked == "unlike") {
    likeButton.innerHTML = canLikeicon;
  }

  const numberOfLikes = document.createElement("p");
  numberOfLikes.classList.add("number-of-likes");
  numberOfLikes.innerText = nuOfLikes;

  likeButton.addEventListener("click", () => {
    toggleLike(answerId, likeButton, numberOfLikes);
  });

  numberOfLikesWrapper.appendChild(numberOfLikes);

  numberOfLikesWrapper.appendChild(likeButton);

  answerCardCont.appendChild(numberOfLikesWrapper);

  answerCard.appendChild(answerCardCont);

  liElement.appendChild(answerCard);

  ulElement.appendChild(liElement);

  nestedBranch.appendChild(ulElement);

  // Highlight the code inside the answer for better user experience
  hljs.highlightAll();
};

// This function has connected with the server and fetch data in every 2.5 seconds
// to keep the page updated, to stop reloading the page for users to see the new answers

// Initiially, set numberOfAnswerCards to 0, and
// After the first fetch, it will be the lenght of data array (which comes from the server)
// then this repeats in every 2.5 seconds

// If numberOfAnswerCards is 0, and creates all the answer cards
// then save the fetched data length to numberOfAnswerCards
// use that value to slice the data array to find the new answers and create new answer cards

let numberOfAnswerCards = 0;

const getAnswers = () => {
  fetch(getAnswersUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      if (numberOfAnswerCards == 0) {
        for (let i = 0; i < data.length; i++) {
          createAnswerCard(
            data[i][0],
            data[i][1],
            data[i][2],
            data[i][3],
            data[i][4],
            data[i][5],
            data[i][6],
            data[i][7]
          );
        }
      } else if (data.length != numberOfAnswerCards) {
        let newAnswers = data.slice(numberOfAnswerCards);
        for (let i = 0; i < newAnswers.length; i++) {
          createAnswerCard(
            newAnswers[i][0],
            newAnswers[i][1],
            newAnswers[i][2],
            newAnswers[i][3],
            newAnswers[i][4],
            newAnswers[i][5],
            newAnswers[i][6],
            newAnswers[i][7]
          );
        }
      }
      numberOfAnswerCards = data.length;
    });
};

getAnswers();
setInterval(getAnswers, 2500);

// This part of the code is used to get the number of answers for the relevant question
// This function also fetches data in every 2.5 seconds
// This fetchs the number of answers from the server
const numberOfAnswers = document.querySelector(".number-of-answers");

const updateNumberofAnswers = () => {
  fetch(numberOfanswersUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      numberOfAnswers.innerText = data["numberOfAnswers"];
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

updateNumberofAnswers();
setInterval(updateNumberofAnswers, 2500);
