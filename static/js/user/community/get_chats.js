import { createChatCard, createNewChatCard } from "./chat_card.js";

let numberOfChatCards = 0;

// This function fetches all community discussions from the server in every 2.5 seconds
// and creates chat cards for each discussion.

// To stop making same chat cards again and again use numberOfChatCards variable
// that variable initially set to 0 and after a one fetch it set to the the length of the data (number of chat cards created)
// then using that, next time when I fetch the data, i slice the data to get only new discussions and update the numberOfChatCards variable
// and create new chat cards for those new discussions

// chatId - [i][0]
// questionData - [i][1]
// postedTimeData - [i][2]
// writerName - [i][3]
// profilePicOfWriter - [i][4]
// nuOfAnswers - [i][5]
// isSave - [i][6]

// urlForDiscs has set in the community_all.html file
const getAllCommunityDiscussion = () => {
  fetch(urlForDiscs)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      if (numberOfChatCards == 0) {
        console.log(data.length);
        numberOfChatCards = data.length;
        for (let i = 0; i < data.length; i++) {
          createChatCard(
            data[i][0],
            data[i][1],
            data[i][2],
            data[i][3],
            data[i][4],
            data[i][5],
            data[i][6]
          );
        }
      } else {
        let newQuestions = data.slice(0, data.length - numberOfChatCards);
        for (let i = 0; i < newQuestions.length; i++) {
          createNewChatCard(
            newQuestions[i][0],
            newQuestions[i][1],
            newQuestions[i][2],
            newQuestions[i][3],
            newQuestions[i][4],
            newQuestions[i][5],
            newQuestions[i][6]
          );
        }
        numberOfChatCards = data.length;
      }
    })
    .catch((error) => {
      console.error(error);
    });
};

getAllCommunityDiscussion();
setInterval(getAllCommunityDiscussion, 2500);
