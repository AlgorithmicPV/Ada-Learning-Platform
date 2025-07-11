const mainTopBar = document.querySelector(".top-bar");
const challengeTopBar = document.querySelector(
  ".sub-navigation-bar-practice-hub"
);
const challengeCont = document.querySelector(".challenge-detail-wrapper");
const challengeDetailWrapper = document.querySelector(
  ".challenge-detail-wrapper"
);
const codeEnvWrapper = document.querySelector(".code-env-wrapper");

const adjustTheHeightOfConts = () => {
  const windowHeight = window.innerHeight;

  let availableHeight =
    windowHeight -
    (mainTopBar.offsetHeight + challengeTopBar.offsetHeight + 100);
  challengeCont.style.height = `${availableHeight}px`;
  codeEnvWrapper.style.height = `${availableHeight}px`;
};

window.addEventListener("load", () => {
  adjustTheHeightOfConts();
});

window.addEventListener("resize", () => {
  adjustTheHeightOfConts();
});

const selectedLanguageWrapper = document.querySelector(
  ".selected-language-wrapper"
);
const optionsWrapper = document.querySelector(".options-wrapper");
const selectedLanguage = document.querySelector(".selected-language");
let showingOptionsWrapper = false;

const showOptionsWrapper = () => {
  if (showingOptionsWrapper == true) {
    showingOptionsWrapper = false;
    optionsWrapper.style.opacity = 0;
    optionsWrapper.style.display = "none";
  } else {
    showingOptionsWrapper = true;
    optionsWrapper.style.opacity = 1;
    optionsWrapper.style.display = "flex";
  }
};

selectedLanguageWrapper.addEventListener("click", () => {
  showOptionsWrapper();
});

const options = document.querySelectorAll(".option");

let language = "python";
options.forEach((option) => {
  option.addEventListener("click", () => {
    const lang = option.dataset.value;
    language = lang;
    const selectedContent = option.innerHTML;
    selectedLanguage.innerHTML = selectedContent;
    console.log(language);
    fetch(send_language_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ language: language }),
    })
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error(error));
    showOptionsWrapper();
    monaco.editor.setModelLanguage(editor.getModel(), language);
  });
});

const doneButton = document.querySelector(".done-btn");

doneButton.addEventListener("click", () => {
  let userCode = window.editor.getValue();
  console.log(check_answers_url);

  fetch(check_answers_url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ user_code: userCode }),
  })
    .then((response) => response.json())
    .then((data) => console.log(data))
    .catch((error) => console.error(error));
});

const toggleSolution = document.querySelector(".toggle-solution");
const solutionCode = document.querySelector(".solution .code");
const solution = document.querySelector(".solution")

toggleSolution.addEventListener("click", () => {
  fetch(get_solution_url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ language: language }),
  })
    .then((response) => response.json())
    .then((data) => {
      solutionCode.innerHTML = data["answer"];
      solution.style.display = "flex";
      solution.style.opacity = 1;
      hljs.highlightAll();
    })
    .catch((error) => console.error(error));
});

const solutionCloseBtn = document.querySelector(".solution-close-btn");

const hideSolution = () => {
  solution.style.opacity = 0;
  solution.style.display = "none";
};

solutionCloseBtn.addEventListener("click", () => {
  hideSolution()
})


