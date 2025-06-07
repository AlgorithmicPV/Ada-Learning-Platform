// Javascript codes for the landing page

// Below Function is to adjust the height of the wrapper div
const adjust_height_wrapper = () => {
  const navigation_bar = document.querySelector(".navbar"); // Selects the navigation bar element from the DOM
  const sections = document.querySelectorAll("section"); // Selects all section elements on the page
  const wrappers = document.querySelectorAll(".wrapper"); // Selects all <div> elements with the class 'wrapper' for layout control
  const mobile_menu = document.querySelector(".mobile-menu"); // Selects all <div> element with the class 'mobile-menu' for layout control
  let height_navigationbar = navigation_bar.offsetHeight; // Gets the height of the navigation bar to adjust section heights accordingly

  // Loops through each section to resize it
  for (let wrapper = 0; wrapper < wrappers.length; wrapper++) {
    let height_sections = sections[wrapper].offsetHeight; // Gets the original height of the current section
    let new_height = height_sections - height_navigationbar; // Calculates the new height by subtracting the navbar height
    wrappers[wrapper].style.height = `${new_height - 20}px`; // Applies the new height to the wrapper div to prevent overflow behind the navbar

    mobile_menu.style.height = `${new_height}px`;
  }
};

window.addEventListener("load", adjust_height_wrapper); // Run once when the page loads
window.addEventListener("resize", adjust_height_wrapper); // Run again on window resize to keep layout responsive
// This ensures wrapper heights adjust correctly on window resize,
// since running the code only once would cause layout issues if the navigation bar size changes with screen size
//########### End of above code part ###################//
//

// Below code is for the gradient circle animation in the cards in the "Why Us" section
const gradient_circles = document.querySelectorAll(".gradient-circle"); // Selects all gradient circle elements inside the cards
const cards = document.querySelectorAll(".card"); // Selects all card elements that the user can interact with

// Loops through each card and attaches a pointer move event to animate the corresponding gradient circle
for (let i = 0; i < gradient_circles.length; i++) {
  cards[i].onpointermove = (event) => {
    const rect = cards[i].getBoundingClientRect(); // Gets the card's position and size relative to the viewport
    const x = event.clientX - rect.left; // Calculates the horizontal pointer position relative to the card
    const y = event.clientY - rect.top; // Calculates the vertical pointer position relative to the card

    // Animates the gradient circle to follow the user's pointer within the card area
    gradient_circles[i].animate(
      {
        left: `${x}px`,
        top: `${y}px`,
      },
      { duration: 1000, fill: "forwards" } // Smoothly moves the circle and retains its final position after the animation
    );
  };
}
//########### End of above code part ###################//
//

// Adjusts gap between comment boxes. When the duplicated wrapper (aria-hidden="true") becomes visible during scroll, spacing appears uneven due to the gap being split between the two wrappers.
// All comment boxes are wrapped inside a <div> with class "comments-box-wrapper",
// which is itself contained within the "comments-section" <div>.
const adjustCommentBoxGaps = () => {
  const comment_box_wrapper = document.querySelectorAll(
    ".comments-boxs-wrapper"
  ); // Selects all <div> elements with the class name "comments-box-wrapper" as an array
  const comment_boxes = document.querySelectorAll(".comment-box"); // Selects all <div> elements with the class name "comment-box" as an array
  let width_comments_boxs_wrapper =
    comment_box_wrapper[0].getBoundingClientRect().width; // Gets the total width of the .comments-box-wrapper to calculate the exact gap needed for proper alignment inside the .comments-section.
  let widht_comment_box = comment_boxes[0].getBoundingClientRect().width; // Gets the width of one comment box (takes only as the width of all comment boxes are same).
  let gaps =
    width_comments_boxs_wrapper -
    widht_comment_box * (comment_boxes.length / 2); // Finds the exact total gaps: subtract the total width of .comments-box-wrapper by the combined width of the comment boxes. We divide by two times the width of a single .comment-box because comment_boxes.length gives 6, but 3 are repetitions of the original 3.
  let gap_between_two_boxes = gaps / (comment_boxes.length / 2 - 1); // Divides the total gap by the number of gaps to get the width of a single gap.
  const comments_section = document.querySelector(".comments-section"); // Selects the <div> element with the class name ".comments-section".
  comments_section.style.gap = `${gap_between_two_boxes}px`; // Sets the gap
};

window.addEventListener("resize", adjustCommentBoxGaps); // Run again on window resize
window.addEventListener("load", adjustCommentBoxGaps); // Run once when the page loads
//########### End of above code part ###################//
//

// Displays the relevant card when a slider dot (small ball) is clicked in the "Why Us" section (less than 1200px screen - mobiles and tabs)

const slider_dots = document.querySelectorAll(".slider-nav div"); // Selects all the slider dots

const show_card = (x) => {
  //  Runs the below code, the number of the slider_dots array, The code below avoids being coloured and show the card more than one
  // Identifies the selected slider_dot among other dots using a for loop, and according to that, changes its background colour and shows the relevant card
  for (let i = 0; i < slider_dots.length; i++) {
    if (slider_dots[x] == slider_dots[i]) {
      slider_dots[x].style.backgroundColor = "#ede3ff";
      cards[x].style.display = "flex";
      cards[x].style.visibility = "visible";
    } else {
      slider_dots[i].style.backgroundColor = "transparent";
      cards[i].style.display = "none";
      cards[i].style.visibility = "hidden";
    }
  }
};

for (let i = 0; i < slider_dots.length; i++) {
  slider_dots[i].addEventListener("click", () => {
    show_card(i);
  });
} // Calls the show_card function when the user clicks on the slider dot, and passes the index number of the slider_dots into the show_card function, uses a for loop to reduce the repition in the code
//########### End of above code part ###################//
//

// This code checks if the width of the screen is less than 1200px, one card would show and the other cards hide,  if the screen width is larger than 1200px, it will show all the cards in the why us section
const cards_visibilty = () => {
  let width_of_the_screen = document.body.getBoundingClientRect().width;
  if (width_of_the_screen > 1200) {
    // For larger screens
    for (let i = 0; i < cards.length; i++) {
      cards[i].style.display = "flex";
      cards[i].style.visibility = "visible";
    }
  } else {
    // For smaller screens
    cards[0].style.display = "flex";
    cards[0].style.visibility = "visible";
    slider_dots[0].style.backgroundColor = "#ede3ff";
    for (let i = 1; i < cards.length; i++) {
      cards[i].style.display = "none";
      cards[i].style.visibility = "hidden";
    }
  }
};

window.addEventListener("resize", cards_visibilty);
window.addEventListener("load", cards_visibilty);
//########### End of above code part ###################//
//

// This code hides or shows the Mobile Navigation Drawer, hambuerger icon and the close icon
const hamburger_icon = document.querySelector(".hamburger-icon");
const cross_icon = document.querySelector(".cross-icon");
const mobile_menu = document.querySelector(".mobile-menu");

let is_it_showing; // This variable for identifying  the Mobile Navigation Drawer is showing or not

const show_the_menu = () => {
  hamburger_icon.style.display = "none"; // Hides the hamburger icon
  cross_icon.style.display = "block"; // Shows the close icon, this is for close that Mobile Navigation Drawer
  mobile_menu.style.display = "flex"; // Shows the Mobile Navigation Drawer
  is_it_showing = true;
};

const hide_the_menu = () => {
  hamburger_icon.style.display = "flex";
  cross_icon.style.display = "none";
  mobile_menu.style.display = "none";
  is_it_showing = false;
};

const hamburger_btn = document.querySelector(".navbar-hamburger");
hamburger_btn.addEventListener("click", () => {
  if (is_it_showing) {
    hide_the_menu(); // If the Mobile Navigation Drawer is showing, hide that when user clicks on the hamburger button
  } else {
    show_the_menu();
  }
});

const menu_links = document.querySelectorAll(".mobile-menu-texts-wrapper a");

// This is for the user clicks on a navigation link, it will hide the Mobile Navigation Drawer after the user clicks on it
for (let i = 0; i < menu_links.length; i++) {
  menu_links[i].addEventListener("click", () => {
    if (is_it_showing) {
      hide_the_menu();
    }
  });
}

const light_theme = () => {
  document.documentElement.style.setProperty("--light-text-color", "#09001a2e");
  document.documentElement.style.setProperty("--dark-text-color", "#09001A");
  document.documentElement.style.setProperty("--background-color", "#F5F0FF");
  document.documentElement.style.setProperty("--gradient-color", "#DECDFD");
  document.documentElement.style.setProperty("--gradient-color-two", "#DECDFD");
  document.documentElement.style.setProperty("--footer-color", "#FFFFFF");

  const dark_theme_images = document.querySelectorAll(".dark-theme-img");
  for (let i = 0; i < dark_theme_images.length; i++) {
    dark_theme_images[i].style.display = "none";
  }

  const light_theme_images = document.querySelectorAll(".light-theme-img");
  for (let i = 0; i < light_theme_images.length; i++) {
    light_theme_images[i].style.display = "flex";
  }

  is_dark_theme = false;
};

const dark_theme = () => {
  document.documentElement.style.setProperty("--light-text-color", "#ede3ff2b");
  document.documentElement.style.setProperty("--dark-text-color", "#ede3ff");
  document.documentElement.style.setProperty("--background-color", "#05000e");
  document.documentElement.style.setProperty("--gradient-color", "#17013d");
  document.documentElement.style.setProperty("--gradient-color-two", "#3d059e");
  document.documentElement.style.setProperty("--footer-color", "#000000");

  const dark_theme_images = document.querySelectorAll(".dark-theme-img");
  for (let i = 0; i < dark_theme_images.length; i++) {
    dark_theme_images[i].style.display = "flex";
  }

  const light_theme_images = document.querySelectorAll(".light-theme-img");
  for (let i = 0; i < light_theme_images.length; i++) {
    light_theme_images[i].style.display = "none";
  }

  is_dark_theme = true;
};

let is_dark_theme = true;

document.querySelector(".theme-toggle").addEventListener("click", () => {
  if (is_dark_theme) {
    light_theme();
  } else {
    dark_theme();
  }
});
