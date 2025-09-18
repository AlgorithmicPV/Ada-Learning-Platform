import { showAlertMessages } from "../message-handler.js";

// This JavaScript file is the base foundation for the code editors used in this platform
// This code is responsible for setting up the Monaco Editor and handling theme toggling
require(["vs/editor/editor.main"], function () {
  let activatedLanguage = window.language;
  // Create the editor instance
  window.editor = monaco.editor.create(document.querySelector(".code-editor"), {
    value: ``,
    language: activatedLanguage,
    theme: "vs-light",
    automaticLayout: true,
    wordWrap: "on",
    scrollBeyondLastLine: false,
  });

  // dark mode and light mode themes for the Monaco Editor

  monaco.editor.defineTheme("ada-theme-dark", {
    base: "vs-dark",
    inherit: true,
    rules: [
      { token: "", background: "010104", foreground: "c9d1d9" },
      { token: "comment", foreground: "8b949e" },
      { token: "keyword", foreground: "ff7b72" },
      { token: "string", foreground: "a5d6ff" },
    ],
    colors: {
      "editor.background": "#010104",
    },
  });

  monaco.editor.defineTheme("ada-theme-light", {
    base: "vs",
    inherit: true,
    rules: [],
    colors: {
      "editor.background": "#FBFBFE",
    },
  });

  // Get the user's preferred theme from localStorage
  const theme_toggle_button_code_editor =
    document.querySelector(".theme-toggle-btn");

  let is_dark_theme_code_editor;

  // Toggle the theme between dark and light
  theme_toggle_button_code_editor.addEventListener("click", () => {
    var prefered_theme = localStorage.getItem("app-theme-preference");

    if (prefered_theme == "dark") {
      monaco.editor.setTheme("ada-theme-dark");

      is_dark_theme_code_editor = false;
    } else {
      monaco.editor.setTheme("ada-theme-light");

      is_dark_theme_code_editor = true;
    }
  });

  // Set the initial theme based on the user's preference
  // If no preference is set, default to dark theme
  if (prefered_theme == "dark") {
    monaco.editor.setTheme("ada-theme-dark");
    is_dark_theme_code_editor = true;
  } else if (prefered_theme == "light") {
    monaco.editor.setTheme("ada-theme-light");
    is_dark_theme_code_editor = false;
  } else {
    monaco.editor.setTheme("ada-theme-dark");
    is_dark_theme_code_editor = true;
  }
});

const output_wrapper = document.querySelector(".output-wrapper");
const ai_assistance_wrapper = document.querySelector(".ai-assistance-wrapper");
const input_wrapper = document.querySelector(".input-wrapper");

// This is to convert markdown to HTML
import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";

// Function to toggle the visibility of the output and AI assistance sections
// This function is triggered by clicking the respective buttons
document.querySelector(".btn-to-show-output").addEventListener("click", () => {
  output_wrapper.style.display = "flex";
  ai_assistance_wrapper.style.display = "none";
  input_wrapper.style.display = "none";

  document.querySelector(".btn-to-show-output").classList.add("active-btn");
  document
    .querySelector(".btn-to-show-ai-assistance")
    .classList.remove("active-btn");
  document.querySelector(".btn-to-show-input").classList.remove("active-btn");
});

document
  .querySelector(".btn-to-show-ai-assistance")
  .addEventListener("click", () => {
    output_wrapper.style.display = "none";
    ai_assistance_wrapper.style.display = "flex";
    input_wrapper.style.display = "none";

    document
      .querySelector(".btn-to-show-output")
      .classList.remove("active-btn");
    document.querySelector(".btn-to-show-input").classList.remove("active-btn");
    document
      .querySelector(".btn-to-show-ai-assistance")
      .classList.add("active-btn");
  });

document.querySelector(".btn-to-show-input").addEventListener("click", () => {
  output_wrapper.style.display = "none";
  ai_assistance_wrapper.style.display = "none";
  input_wrapper.style.display = "flex";
  document.querySelector(".btn-to-show-output").classList.remove("active-btn");
  document
    .querySelector(".btn-to-show-ai-assistance")
    .classList.remove("active-btn");
  document.querySelector(".btn-to-show-input").classList.add("active-btn");
});

const loadWrapper = document.querySelector(".loader-wrapper");
const loader = document.querySelector(".loader");

const showLoader = () => {
  loadWrapper.style.display = "flex";
  loader.style.opacity = 1;
  loader.style.visibility = "visible";
};

const hideLoader = () => {
  loadWrapper.style.display = "none";
  loader.style.opacity = 0;
  loader.style.visibility = "hidden";
};

// Initially show the output section and hide the AI assistance section
output_wrapper.style.display = "flex";
ai_assistance_wrapper.style.display = "none";
input_wrapper.style.display = "none";

// Sending code to server to compile and run,
// and get the output from the server
const send_the_code = async () => {
  let user_code = window.editor.getValue();
  let user_input = document.querySelector(".input-wrapper textarea").value;

  // Checks whether the user code is empty
  // TODO: Have to do input number of texts and spaces thing
  // TODO Make JS function to check the input number
  if (!user_code.trim()) {
    showAlertMessages("warning", "No code detected. Type something first");
    return;
  }

  const send_user_code = {
    user_code: user_code, // The code written by the user in the editor
    user_input: user_input, // The input provided by the user for the code execution (works with python)
  };
  showLoader();
  output_wrapper.style.display = "none";

  try {
    const response = await fetch(fetch_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(send_user_code),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    hideLoader();
    output_wrapper.style.display = "flex";
    ai_assistance_wrapper.style.display = "none";
    input_wrapper.style.display = "none";

    const result = await response.json();

    // Make a wrapper for the terminal line
    const terminal_line_wrapper = document.createElement("div");
    terminal_line_wrapper.classList.add("terminal-line-wrapper");

    // Create a paragraph element for the mark and the terminal line
    // The mark indicates the start of the output line
    const mark = document.createElement("p");
    mark.classList.add("mark");
    mark.innerText = ">>> ";

    // Create a paragraph element for the terminal line output
    // This will display the output of the code execution
    const terminal_line = document.createElement("p");
    terminal_line.classList.add("terminal-line");
    terminal_line.innerText = result["output"];

    terminal_line_wrapper.appendChild(mark);
    terminal_line_wrapper.appendChild(terminal_line);

    output_wrapper.appendChild(terminal_line_wrapper);
  } catch (error) {
    console.error(error);
  }
};

// Event listener for the "Run" button to send the code to the server
document.querySelector(".run").addEventListener("click", () => {
  send_the_code();
});

// Sending user input to the AI chat route and getting the AI response
// This function handles the chat interaction with the AI model
const ai_chat = async () => {
  let user_input = document.getElementById("user-input").value;
  document.getElementById("user-input").value = ""; // Clear the input field after sending

  if (!user_input) {
    showAlertMessages(
      "warning",
      "Oops! Looks like you forgot to type your message."
    );
    return;
  }

  const send_user_input = {
    user_input: user_input,
  };
  showLoader();
  ai_assistance_wrapper.style.display = "none";

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
    hideLoader();
    ai_assistance_wrapper.style.display = "flex";

    const result = await response.json();

    if (result["warning"]) {
      showAlertMessages("warning", result["warning"]);
      return;
    }

    if (result["error"]) {
      showAlertMessages("error", result["error"]);
      return;
    }
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
    const ai_response = document.createElement("div");
    ai_response.classList.add("ai-response");
    ai_response.innerHTML = marked.parse(result["result"]);

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

const chatContent = document.querySelector(".chat-content");
const verticalNavBar = document.querySelector(".vertical-nav-bar");

// This Function will adjust the height of the chat-content div
// I took the total  height of the the vertical navigation bar and substract 50 from that
// because of the input box
// Reason to take the height of the vertical navigation bar is
// It is common in every section in that parent div
function updateHeight() {
  requestAnimationFrame(() => {
    const newHeight = verticalNavBar.offsetHeight;
    chatContent.style.height = `${newHeight - 50}px`;
  });
}

window.addEventListener("resize", updateHeight);
window.addEventListener("load", updateHeight);
