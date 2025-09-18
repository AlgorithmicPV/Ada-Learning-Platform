// Javascript codes for the Base template

const navigationBar = document.querySelector(".navigation-bar-wrapper");
const menuCloppasedButton = document.querySelector(".menu-cloppased-button");
const mainWrapper = document.querySelector(".main-wrapper");
const closeButtonSmallScreenMenu = document.querySelector(".close-menu-button");
const smallScreenMenu = document.querySelector(".menu-wrapper-small-screen");
const menuCloppasedButtonSmallScreen = document.querySelector(
  ".menu-cloppased-button.small-screen"
);
const themeToggleButton = document.querySelector(".theme-toggle-btn");
const buttons = document.querySelectorAll(".navigation-bar-wrapper a");
const textsInButtons = document.querySelectorAll(".navigation-bar-wrapper a p");
const buttonSvgs = document.querySelectorAll(".navigation-bar-wrapper a svg");

let collapsedMenu = false;
let smallMenuShowing = false;

const toggleMenu = (
  collapsedMenuState,
  buttonsWidth,
  textsInButtonsDisplay,
  buttonsmarginRight,
  navigationBarWidth,
  mainWrapperWidth
) => {
  collapsedMenu = collapsedMenuState;

  for (let i = 1; i < buttons.length; i++) {
    buttons[i].style.width = buttonsWidth;
  }

  for (let i = 0; i < textsInButtons.length; i++) {
    textsInButtons[i].style.display = textsInButtonsDisplay;
  }

  for (let i = 0; i < buttonSvgs.length; i++) {
    buttonSvgs[i].style.marginRight = buttonsmarginRight;
  }
  navigationBar.style.width = navigationBarWidth;
  mainWrapper.style.width = mainWrapperWidth;
};

const collapsedMenuFunc = () => {
  toggleMenu(true, "min-content", "none", "0", "min-content", "100vw");
};

const expandedMenuFunc = () => {
  toggleMenu(false, "150px", "block", "10px", "200px", "calc(100vw - 200px)");
};

const adjustTheScreenWidth = () => {
  if (window.innerWidth > 1280) {
    // Runs only in large screens
    var menuMode = localStorage.getItem("menu-mode");
    if (menuMode == "collapsed") {
      collapsedMenuFunc();
    } else if (menuMode == "expanded") {
      expandedMenuFunc();
    } else {
      expandedMenuFunc();
    }
  } else {
    mainWrapper.style.width = "100vw";
  }
};

window.addEventListener("load", () => {
  adjustTheScreenWidth();
});

window.addEventListener("resize", () => {
  adjustTheScreenWidth();
});

/* Collpases and Opens the veritcal navigation bar when the collpased button clicks */
menuCloppasedButton.addEventListener("click", () => {
  if (collapsedMenu != true) {
    collapsedMenuFunc();
    menuMode = "collapsed";
    localStorage.setItem("menu-mode", menuMode);
  } else {
    expandedMenuFunc();
    menuMode = "expanded";
    localStorage.setItem("menu-mode", menuMode);
  }
});

const menutoggle = () => {
  if (smallMenuShowing != true) {
    smallScreenMenu.style.display = "flex";
    smallMenuShowing = true;
  } else {
    smallScreenMenu.style.display = "none";
    smallMenuShowing = false;
  }
};

/* Shows the menu screen for small screen users when they click on the menu icon */
menuCloppasedButtonSmallScreen.addEventListener("click", () => {
  menutoggle();
});

/* Hides the menu when the user clicks the close button */
closeButtonSmallScreenMenu.addEventListener("click", () => {
  menutoggle();
});

/* Changes the theme when the user clicks on theme toggle button */
themeToggleButton.addEventListener("click", () => {
  if (is_dark_theme == true) {
    light_theme();
  } else {
    dark_theme();
  }
});
