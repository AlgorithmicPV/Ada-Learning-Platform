// Javascript code for the lesson page

const main_top_bar = document.querySelector(".top-bar");
const lesson_top_bar = document.querySelector(".lesson-cont-top-bar");
const lesson_cont = document.querySelector(".lesson-cont");

// Function to adjust the height of the lesson container
// based on the window height and the heights of the top bars
const adjust_the_height_of_lesson_cont = () => {
  const window_height = window.innerHeight; // Get the height of the window

  let available_height =
    window_height -
    (lesson_top_bar.offsetHeight + main_top_bar.offsetHeight + 40); // Calculate available height by subtracting the heights of the top bars and some padding

  lesson_cont.style.height = `${available_height}px`; // Set the height of the lesson container to the available height
};

// Adjust the height of the lesson container on page load and resize
window.addEventListener("load", () => {
  adjust_the_height_of_lesson_cont();
});

window.addEventListener("resize", () => {
  adjust_the_height_of_lesson_cont();
});

// Function to toggle the visibility of the lesson menu bar
const toggle_lesson_menu_bar = () => {
  document
    .querySelector(".show-lesson-menu-btn")
    .addEventListener("click", () => {
      document.querySelector(".lesson-menu-bar").style.display = "flex"; // Show the lesson menu bar
      document.querySelector(".lesson").style.display = "none"; // Hide the lesson content
    });
};

toggle_lesson_menu_bar(); // Call the function to set up the toggle functionality
