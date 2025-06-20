// Javascript codes for the Base template

const navigation_bar = document.querySelector(".navigation-bar-wrapper");
const menu_cloppased_button = document.querySelector(".menu-cloppased-button");
const dashboard_wrapper = document.querySelector(".main-wrapper");
const close_button_small_screen_menu =
  document.querySelector(".close-menu-button");
const small_screen_menu = document.querySelector(".menu-wrapper-small-screen");
const menu_cloppased_button_small_Screen = document.querySelector(
  ".menu-cloppased-button.small-screen"
);
const theme_toggle_button = document.querySelector(".theme-toggle-btn");

let collapsed_menu = false;
let small_menu_showing = false;
let is_dark_theme = true;

/* Collpases and Opens the veritcal navigation bar when the collpased button clicks */
menu_cloppased_button.addEventListener("click", () => {
  const buttons = document.querySelectorAll(".navigation-bar-wrapper button");
  const texts_in_buttons = document.querySelectorAll(
    ".navigation-bar-wrapper button p"
  );
  const button_svgs = document.querySelectorAll(
    ".navigation-bar-wrapper button svg"
  );

  if (collapsed_menu != true) {
    collapsed_menu = true;

    for (let i = 1; i < buttons.length; i++) {
      buttons[i].style.width = "min-content";
    }

    for (let i = 0; i < texts_in_buttons.length; i++) {
      texts_in_buttons[i].style.display = "none";
    }

    for (let i = 0; i < button_svgs.length; i++) {
      button_svgs[i].style.marginRight = "0";
    }
    navigation_bar.style.width = "min-content";
    dashboard_wrapper.style.width = "100vw";
  } else {
    collapsed_menu = false;

    for (let i = 0; i < texts_in_buttons.length; i++) {
      texts_in_buttons[i].style.display = "block";
    }

    for (let i = 1; i < buttons.length; i++) {
      buttons[i].style.width = "150px";
    }

    for (let i = 0; i < button_svgs.length; i++) {
      button_svgs[i].style.marginRight = "10px";
    }

    navigation_bar.style.width = "200px";
    dashboard_wrapper.style.width = "calc(100vw - 200px)";
  }
});

/* Shows the menu screen for small screen users when they click on the menu icon */
menu_cloppased_button_small_Screen.addEventListener("click", () => {
  if (small_menu_showing != true) {
    small_screen_menu.style.display = "flex";
    small_menu_showing = true;
  } else {
    small_screen_menu.style.display = "none";
    small_menu_showing = false;
  }
});

/* Hides the menu when the user clicks the close button */
close_button_small_screen_menu.addEventListener("click", () => {
  if (small_menu_showing != true) {
    small_screen_menu.style.display = "flex";
    small_menu_showing = true;
  } else {
    small_screen_menu.style.display = "none";
    small_menu_showing = false;
  }
});

// let colour_variables = [
//   "--background-color",
//   "--text-color",
//   "--border-color",
//   "--second-text-color",
//   "--primary-color",
// ];

// let dark_theme_colours = [
//   "#010104",
//   "#ebe9fc",
//   "#ebe9fc22",
//   "#ebe9fc70",
//   "#3a31d8",
// ];

// let white_theme_colours = [
//   "#FBFBFE",
//   "#050316",
//   "#0503161e",
//   "#0503167a",
//   "#2F27CE",
// ];

let colour_variables = [
  "--background-color",
  "--text-color",
  "--border-color",
  "--second-text-color",
  "--primary-color",
  "--blocks-color",
  "--small-blocks-color",
  "--home-text-color",
  "--text-color-first",
  "--text-color-second",
  "--text-color-third",
  "--text-color-rest",
];

let dark_theme_colours = [
  "#010104",
  "#ebe9fc",
  "#ebe9fc22",
  "#ebe9fc70",
  "#3a31d8",
  "#0d0d11",
  "#ebe9fc36",
  "#ebe9fc",
  "#ffd700",
  "#eeeeee",
  "#ffa500",
  "#ffffff99",
];

let white_theme_colours = [
  "#FBFBFE",
  "#050316",
  "#0503161e",
  "#0503167a",
  "#2F27CE",
  "#EEEEF2",
  "#05031611",
  "#ebe9fc",
  "#CAAB00",
  "#000000",
  "#FFA500",
  "#000000c8",
];

const dark_theme = () => {
  for (let i = 0; i < colour_variables.length; i++) {
    document.documentElement.style.setProperty(
      colour_variables[i],
      dark_theme_colours[i]
    );
  }
  is_dark_theme = true;
  theme_preference = "dark";
  localStorage.setItem("theme-preference", theme_preference); // Saves to the local storage, later we can change the colour theme of the landing page according to the user's preference
};

const light_theme = () => {
  for (let i = 0; i < colour_variables.length; i++) {
    document.documentElement.style.setProperty(
      colour_variables[i],
      white_theme_colours[i]
    );
  }
  is_dark_theme = false;
  theme_preference = "light";
  localStorage.setItem("theme-preference", theme_preference); // Saves to the local storage, later we can change the colour theme of the landing page according to the user's preference
};

/* Changes the theme when the user clicks on theme toggle button */
theme_toggle_button.addEventListener("click", () => {
  if (is_dark_theme == true) {
    light_theme();
  } else {
    dark_theme();
  }
});

// Gets the prefered_theme if user has selected from the local storage
var prefered_theme = localStorage.getItem("theme-preference");

if (prefered_theme == "dark") {
  dark_theme();
} else if (prefered_theme == "light") {
  light_theme();
} else {
  dark_theme();
}
