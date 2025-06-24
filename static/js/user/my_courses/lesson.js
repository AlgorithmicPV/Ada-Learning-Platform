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
