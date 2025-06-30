let is_dark_theme;

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
  "--course-card-background-color",
  "--transparent-background-color",
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
  "#000000ac",
  "#0000008b",
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
  "#ffffffac",
  "#ffffff8b",
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
  localStorage.setItem("app-theme-preference", theme_preference); // Saves to the local storage, later we can change the colour theme of the landing page according to the user's preference
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
  localStorage.setItem("app-theme-preference", theme_preference); // Saves to the local storage, later we can change the colour theme of the landing page according to the user's preference
};
// Gets the prefered_theme if user has selected from the local storage
var prefered_theme = localStorage.getItem("app-theme-preference");

if (prefered_theme == "dark") {
  dark_theme();
  is_dark_theme = true;
} else if (prefered_theme == "light") {
  light_theme();
  is_dark_theme = false;
} else {
  dark_theme();
  is_dark_theme = true;
}
