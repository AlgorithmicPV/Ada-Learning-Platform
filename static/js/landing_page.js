// Javascript codes for the landing page

// Below Function is to adjust the height of the wrapper div
const adjust_height_wrapper = () => {
  const navigation_bar = document.querySelector(".navbar"); // Selects the navigation bar element from the DOM
  const sections = document.querySelectorAll("section"); // Selects all section elements on the page
  const wrappers = document.querySelectorAll(".wrapper"); // Selects all <div> elements with the class 'wrapper' for layout control
  let height_navigationbar = navigation_bar.offsetHeight; // Gets the height of the navigation bar to adjust section heights accordingly

  // Loops through each section to resize it
  for (let wrapper = 0; wrapper < wrappers.length; wrapper++) {
    let height_sections = sections[wrapper].offsetHeight; // Gets the original height of the current section
    let new_height = height_sections - height_navigationbar; // Calculates the new height by subtracting the navbar height
    wrappers[wrapper].style.height = `${new_height - 20}px`; // Applies the new height to the wrapper div to prevent overflow behind the navbar
  }
};

window.addEventListener("load", adjust_height_wrapper); // Run once when the page loads
window.addEventListener("resize", adjust_height_wrapper); // Run again on window resize to keep layout responsive
// This ensures wrapper heights adjust correctly on window resize,
// since running the code only once would cause layout issues if the navigation bar size changes with screen size

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
