// JaavaScript code for the AI course page

let isSearchBoxOn = false;

// Function to toggle the visibility of the search box
const show_search_box = () => {
  if (isSearchBoxOn) {
    isSearchBoxOn = false;
    document.getElementById("searchBox").style.visibility = "hidden";
  } else {
    isSearchBoxOn = true;
    document.getElementById("searchBox").style.visibility = "visible";
  }
};

const main_top_bar = document.querySelector(".top-bar");
const aiContTopBar = document.querySelector(".ai-course-cont-top-bar");
const aiCourseCont = document.querySelector(".content-and-chat-wrapper");

// Function to adjust the height of the ai course container
// based on the window height and the heights of the top bars
const adjust_the_height_of_aiCourseCont = () => {
  const window_height = window.innerHeight; // Get the height of the window

  let available_height =
    window_height -
    (aiContTopBar.offsetHeight + main_top_bar.offsetHeight + 100); // Calculate available height by subtracting the heights of the top bars and some padding

  aiCourseCont.style.height = `${available_height}px`; // Set the height of the ai course container to the available height
};

// Adjust the height of the lesson container on page load and resize
window.addEventListener("load", () => {
  adjust_the_height_of_aiCourseCont();
});

window.addEventListener("resize", () => {
  adjust_the_height_of_aiCourseCont();
});

const speakButton = document.querySelector(".speak-btn");

// Function to read aloud the text content of the lesson
const synth = window.speechSynthesis;

const read_aloud_text = (text) => {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 1.5;
  synth.speak(utterance);
};

const stop_read_aloud = () => {
  synth.cancel();
};

const pause_read_aloud = () => {
  synth.pause();
};

const resume_read_aloud = () => {
  synth.resume();
};

let isStoppedByUse = false;
let hasStartedReading = false;

// Function to handle the speak button click event
speakButton.addEventListener("click", () => {
  content = document.querySelector(".content").textContent;
  // Remove emojis and special characters from the content
  content = content.replace(
    /([\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF])/g,
    ""
  );
  if (isStoppedByUse == false) {
    if (hasStartedReading) {
      pause_read_aloud();
      isStoppedByUse = true;
    }
  } else if (isStoppedByUse) {
    if (hasStartedReading) {
      resume_read_aloud();
      isStoppedByUse = false;
    }
  }

  if (hasStartedReading == false) {
    read_aloud_text(content);
    hasStartedReading = true;
    console.log("working");
    isStoppedByUse = false;
  }
});

// Stop reading aloud when the window is loaded
// This ensures that if the user navigates away or reloads the page, reading stops
window.addEventListener("load", () => {
  stop_read_aloud();
});

// Sending user input to the AI chat route and getting the AI response
// This function handles the chat interaction with the AI model
const ai_chat = async () => {
  let user_input = document.getElementById("user-input").value;
  document.getElementById("user-input").value = ""; // Clear the input field after sending

  const send_user_input = {
    user_input: user_input,
  };

  try {
    const response = await fetch(chat_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(send_user_input),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const result = await response.json();

    // Create a conversation wrapper to display the user input and AI response
    const conversation = document.createElement("div");
    conversation.classList.add("conversation");

    // Create a wrapper for the user input
    const user_input_wrapper = document.createElement("div");
    user_input_wrapper.classList.add("user-input-wrapper");

    // Create a paragraph element for the user input
    // This will display the text entered by the user in the chat input field
    const input = document.createElement("p");
    input.classList.add("input");
    input.innerText = user_input;

    // Append the user input paragraph to the user input wrapper
    // and then append the wrapper to the conversation
    user_input_wrapper.appendChild(input);
    conversation.appendChild(user_input_wrapper);

    // Create a wrapper for the AI response
    // This will contain the AI's response to the user's input
    const response_wrapper = document.createElement("div");
    response_wrapper.classList.add("answer-wrapper");

    // Create a paragraph element for the AI response
    // This will display the AI's response in a formatted way
    const ai_response = document.createElement("p");
    ai_response.classList.add("ai-response");
    ai_response.innerHTML = marked.parse(result["response"]);

    // Append the AI response paragraph to the response wrapper
    // and then append the response wrapper to the conversation
    response_wrapper.appendChild(ai_response);
    conversation.appendChild(response_wrapper);

    // Append the conversation to the chat content area
    // This will display the conversation in the chat area of the page
    document.querySelector(".chat-content").appendChild(conversation);
  } catch (error) {
    console.error(error);
  }
};

// Event listener for the "Send" button to send the user input to the AI chat
// This button triggers the AI chat function to process the user's input
document.querySelector(".send-btn").addEventListener("click", () => {
  ai_chat();
});
