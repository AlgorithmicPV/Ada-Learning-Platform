// Javascript codes for the Base template

const navigation_bar = document.querySelector(".navigation-bar-wrapper");
const menu_cloppased_button = document.querySelector(".menu-cloppased-button");
const menu_wrapper = document.querySelector(".main-wrapper");
const close_button_small_screen_menu =
  document.querySelector(".close-menu-button");
const small_screen_menu = document.querySelector(".menu-wrapper-small-screen");
const menu_cloppased_button_small_Screen = document.querySelector(
  ".menu-cloppased-button.small-screen"
);
const theme_toggle_button = document.querySelector(".theme-toggle-btn");
const buttons = document.querySelectorAll(".navigation-bar-wrapper button");
const texts_in_buttons = document.querySelectorAll(
  ".navigation-bar-wrapper button p"
);
const button_svgs = document.querySelectorAll(
  ".navigation-bar-wrapper button svg"
);

let collapsed_menu = false;
let small_menu_showing = false;

const collapsed_menu_func = () => {
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
  menu_wrapper.style.width = "100vw";
};

const expanded_menu_func = () => {
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
  menu_wrapper.style.width = "calc(100vw - 200px)";
};

window.addEventListener("load", () => {
  if (window.innerWidth > 1280) {
    // Runs only in large screens
    var menu_mode = localStorage.getItem("menu-mode");
    if (menu_mode == "collapsed") {
      collapsed_menu_func();
    } else if (menu_mode == "expanded") {
      expanded_menu_func();
    } else {
      expanded_menu_func();
    }
  } else {
    menu_wrapper.style.width = "100vw";
  }
});

window.addEventListener("resize", () => {
  if (window.innerWidth > 1280) {
    // Runs only in large screens
    var menu_mode = localStorage.getItem("menu-mode");
    if (menu_mode == "collapsed") {
      collapsed_menu_func();
    } else if (menu_mode == "expanded") {
      expanded_menu_func();
    } else {
      expanded_menu_func();
    }
  } else {
    menu_wrapper.style.width = "100vw";
  }
});

/* Collpases and Opens the veritcal navigation bar when the collpased button clicks */
menu_cloppased_button.addEventListener("click", () => {
  if (collapsed_menu != true) {
    collapsed_menu_func();
    menu_mode = "collapsed";
    localStorage.setItem("menu-mode", menu_mode);
  } else {
    expanded_menu_func();
    menu_mode = "expanded";
    localStorage.setItem("menu-mode", menu_mode);
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

/* Changes the theme when the user clicks on theme toggle button */
theme_toggle_button.addEventListener("click", () => {
  if (is_dark_theme == true) {
    light_theme();
  } else {
    dark_theme();
  }
});
