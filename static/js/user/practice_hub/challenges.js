const selectedLanguageWrapper = document.querySelector(
  ".selected-language-wrapper"
);
const optionsWrapper = document.querySelector(".options-wrapper");
const selectedLanguage = document.querySelector(".selected-language");
const floatWrapper = document.querySelector(".float-wrapper");
let showingOptionsWrapper = false;

const showOptionsWrapper = () => {
  if (showingOptionsWrapper == true) {
    showingOptionsWrapper = false;
    optionsWrapper.style.opacity = 0;
    optionsWrapper.style.display = "none";
    floatWrapper.style.display = "none";
  } else {
    showingOptionsWrapper = true;
    optionsWrapper.style.opacity = 1;
    optionsWrapper.style.display = "flex";
    floatWrapper.style.display = "flex";
  }
};

const options = document.querySelectorAll(".option");
const code = document.querySelector(".code");

options.forEach((option) => {
  option.addEventListener("click", () => {
    const lang = option.dataset.value;
    language = lang;
    const selectedContent = option.innerHTML;
    selectedLanguage.innerHTML = selectedContent;
    fetch(getSolutionSecondCallUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ language: language }),
    })
      .then((response) => response.json())
      .then((data) => {
        code.innerHTML = data["answer"];
        hljs.highlightAll();
        showOptionsWrapper();
      })
      .catch((error) => console.error(error));
  });
});

selectedLanguageWrapper.addEventListener("click", () => {
  showOptionsWrapper();
});

const solutionShowButtons = document.querySelectorAll(".soloution-show-button");
const solutionsWrapper = document.querySelector(".solutions-wrapper");
const challengeTitle = document.querySelector(".challenge-title");

solutionShowButtons.forEach((button) => {
  button.addEventListener("click", () => {
    fetch(getSolutionFirstCallUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ value: button.dataset.value }),
    })
      .then((res) => res.json())
      .then((data) => {
        solutionsWrapper.style.display = "flex";
        solutionsWrapper.style.opacity = 1;

        challengeTitle.innerText = data["title"];
        code.innerHTML = data["answer"];
        hljs.highlightAll();
      })
      .catch((err) => console.error(err));
  });
});

const solutionCloseBtn = document.querySelector(".solution-close-btn");

const hideSolution = () => {
  solutionsWrapper.style.opacity = 0;
  solutionsWrapper.style.display = "none";
  selectedLanguage.innerHTML = "<p>Python</p>";
};

solutionCloseBtn.addEventListener("click", () => {
  hideSolution();
});
