import { createQuestionCard } from "./question-card.js";


// This function fetches all community discussions from the server in every 2.5 seconds
// and creates chat cards for each discussion.

// questionId - [i][0]
// questionData - [i][1]
// postedTimeData - [i][2]
// writerName - [i][3]
// profilePicOfWriter - [i][4]
// nuOfAnswers - [i][5]
// isSave - [i][6]

let since_id = ""
let firstCall = true

// urlForQuestions has set in the community_all.html file
const getAllCommunityDiscussion = () => {
  fetch(urlForQuestions, {
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
      if (data[0][0]) {
        since_id = data[0][0]
      }
      if (data[0] == "") {
        return;
      }

      for (let i = 0; i < data.length; i++) {
        createQuestionCard(
          data[i][0],
          data[i][1],
          data[i][2],
          data[i][3],
          data[i][4],
          data[i][5],
          data[i][6],
          firstCall
        );
      }
      firstCall = false
    })
    .catch((error) => {
      console.error(error);
    });
};

getAllCommunityDiscussion();
setInterval(getAllCommunityDiscussion, 2500);
