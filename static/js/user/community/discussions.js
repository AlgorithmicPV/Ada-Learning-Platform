// Javascript code for the discussions page in the community section

import { showAlertMessages } from "../../message-handler.js";
import { toggleSave } from "./community-utils.js";

const saveButton = document.querySelector(".save-btn");
saveButton.addEventListener("click", () => {
  toggleSave(questionId, saveButton);
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
  })
    .then((response) => response.json())
    .then((data) => {
      showAlertMessages(data["message_type"], data["message"])
    })
    .catch((error) => {
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
  ulElement.classList.add("nested-ul");

  const liElement = document.createElement("li");
  liElement.classList.add("nested-li");
  const answerCard = document.createElement("div");
  answerCard.classList.add("answer-card");

  const img = document.createElement("img");
  img.src = `${profilePicOfWriter}`;

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

let since_id = ""

const getAnswers = () => {
  fetch(getAnswersUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      since_id: since_id
    })
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      if (data.length == 0) {
        return;
      } else {
        since_id = data[data.length - 1][0]
      }
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
    });
};

getAnswers();
setInterval(getAnswers, 2500);

// This part of the code is used to get the number of answers for the relevant question
// This function also fetches data in every 2.5 seconds
// This fetchs the number of answers from the server
const numberOfAnswers = document.querySelector(".number-of-answers");

const updateNumberofAnswers = () => {
  fetch(numberOfAnswersUrl)
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
