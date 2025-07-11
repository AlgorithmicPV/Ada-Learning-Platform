const mainTopBar = document.querySelector(".top-bar");
const challengeTopBar = document.querySelector(".sub-navigation-bar-practice-hub");
const challengeCont = document.querySelector(".challenge-detail-wrapper");
const challengeDetailWrapper = document.querySelector(".challenge-detail-wrapper")
const codeEnvWrapper = document.querySelector(".code-env-wrapper");

const adjustTheHeightOfConts = () => {
  const windowHeight = window.innerHeight;

  let availableHeight = windowHeight - (mainTopBar.offsetHeight + challengeTopBar.offsetHeight + 100)
  challengeCont.style.height = `${availableHeight}px`
  codeEnvWrapper.style.height = `${availableHeight}px`
}

window.addEventListener("load", () => {
  adjustTheHeightOfConts();
})

window.addEventListener("resize", () => {
  adjustTheHeightOfConts();
})


const selectedLanguageWrapper = document.querySelector(".selected-language-wrapper");
const optionsWrapper = document.querySelector(".options-wrapper")
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
}

selectedLanguageWrapper.addEventListener("click", () => {
  showOptionsWrapper()
})

const options = document.querySelectorAll(".option")

let language = "python"
options.forEach(option => {
  option.addEventListener("click", () => {
    const lang = option.dataset.value;
    let language = lang
    const selectedContent = option.innerHTML
    selectedLanguage.innerHTML = selectedContent
    showOptionsWrapper()
    monaco.editor.setModelLanguage(editor.getModel(), language);
  })
})


