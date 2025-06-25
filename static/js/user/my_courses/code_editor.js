// Javascript code fot the code editor page

// This code is responsible for setting up the Monaco Editor and handling theme toggling
require(["vs/editor/editor.main"], function () {
  // Create the editor instance
  language = language;
  window.editor = monaco.editor.create(document.querySelector(".code-editor"), {
    value: ``,
    language: language,
    theme: "vs-light",
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

const main_top_bar = document.querySelector(".top-bar");
const code_editor_top_bar = document.querySelector(".code-editor-top-bar");
const coding_env = document.querySelector(".coding-env");

// Function to adjust the height of the lesson container
// based on the window height and the heights of the top bars
const adjust_the_height_of_coding_env = () => {
  const window_height = window.innerHeight; // Get the height of the window

  let available_height =
    window_height -
    (code_editor_top_bar.offsetHeight + main_top_bar.offsetHeight + 50); // Calculate available height by subtracting the heights of the top bars and some padding

  coding_env.style.height = `${available_height}px`; // Set the height of the lesson container to the available height

  // If the editor is initialized, adjust its layout
  // This ensures that the editor resizes correctly when the window size changes
  if (window.editor) {
    window.editor.layout();
  }
};

// Adjust the height of the lesson container on page load and resize
window.addEventListener("load", () => {
  adjust_the_height_of_coding_env();
});

window.addEventListener("resize", () => {
  adjust_the_height_of_coding_env();
});

const output_wrapper = document.querySelector(".output-wrapper");
const ai_assistance_wrapper = document.querySelector(".ai-assistance-wrapper");

// Function to toggle the visibility of the output and AI assistance sections
// This function is triggered by clicking the respective buttons
document.querySelector(".btn-to-show-output").addEventListener("click", () => {
  output_wrapper.style.display = "flex";
  ai_assistance_wrapper.style.display = "none";
  document.querySelector(".btn-to-show-output").classList.add("active-btn");
  document
    .querySelector(".btn-to-show-ai-assistance")
    .classList.remove("active-btn");
});

document
  .querySelector(".btn-to-show-ai-assistance")
  .addEventListener("click", () => {
    output_wrapper.style.display = "none";
    ai_assistance_wrapper.style.display = "flex";
    document
      .querySelector(".btn-to-show-output")
      .classList.remove("active-btn");
    document
      .querySelector(".btn-to-show-ai-assistance")
      .classList.add("active-btn");
  });

// Initially show the output section and hide the AI assistance section
output_wrapper.style.display = "flex";
ai_assistance_wrapper.style.display = "none";
