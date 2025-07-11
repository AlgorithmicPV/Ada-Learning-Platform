// Javascript code fot the code editor page

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
