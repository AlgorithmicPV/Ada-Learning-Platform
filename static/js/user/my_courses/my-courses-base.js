//JavaScript for the my course base html page

const show_search_box = document.querySelector(".show-the-input-box");

let is_input_box_showing = false;

// Function to toggle the visibility of the search input box
const show_elements = () => {
  document.querySelector(".search-bar input").style.display = "flex";
  document.querySelector(".search-bar .search-btn").style.display = "flex";
  show_search_box.style.display = "none";
  is_input_box_showing = true;
};

// Function to hide the search input box
const hide_elements = () => {
  document.querySelector(".search-bar input").style.display = "none";
  document.querySelector(".search-bar .search-btn").style.display = "none";
  show_search_box.style.display = "flex";
  is_input_box_showing = false;
};

// Event listener for the search box button
// This will show the search input box when clicked if the screen width is less than 1200px
show_search_box.addEventListener("click", () => {
  if (window.innerWidth < 1200) {
    if (is_input_box_showing == false) {
      show_elements();
    }
  }
});

// Event listener for clicks on the document
// This will hide the search input box if clicked outside of it when the screen width is less than 1200px
// It checks if the clicked element is not the search box or its children
document.addEventListener("click", (e) => {
  if (window.innerWidth < 1200) {
    if (e.target.classList[0] != undefined) {
      hide_elements();
    }
  }
});

// Function to show the search box when the window is loaded or resized
const show_the_search_Box = () => {
  if (window.innerHeight >= 1200) {
    show_elements();
  }
};

window.addEventListener("load", show_the_search_Box, false); // Show the search box when the page loads
window.addEventListener("resize", show_the_search_Box, false); // Show the search box when the window is resized
// Also call the function on window resize to ensure the search box is displayed correctly
window.onresize = show_the_search_Box;

// Function to clear the search input when the page is shown
const clearinput = () => {
  document.getElementById("search").value = "";
};

// Add an event listener to clear the input when the page is shown, this is useful for when the user navigates back to this page
// The user doesn't clear the input manually
window.addEventListener("pageshow", clearinput);
