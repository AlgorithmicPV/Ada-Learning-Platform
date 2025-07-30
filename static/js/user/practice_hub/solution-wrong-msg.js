const messageBox = document.querySelector(".message-box");

export const solutionWrongMsg = (image_url) => {
  messageBox.innerHTML = "";

  messageBox.style.display = "flex";
  setTimeout(() => {
    messageBox.style.opacity = 1;
  }, 500);

  const solutionWrongMsgWrapper = document.createElement("div");
  solutionWrongMsgWrapper.classList.add("solution-wrong-msg-wrapper");

  const image = document.createElement("img");
  image.classList.add("solution-wrong-image");
  image.src = image_url;

  const heading = document.createElement("p");
  heading.classList.add("heading-txt");
  heading.innerText = "Hmm… Something’s Off";

  const msgText = document.createElement("p");
  msgText.classList.add("msg-txt");
  msgText.innerText = "Refactor, rethink, and give it another shot.";

  solutionWrongMsgWrapper.appendChild(heading);
  solutionWrongMsgWrapper.appendChild(image);
  solutionWrongMsgWrapper.appendChild(msgText);
  messageBox.append(solutionWrongMsgWrapper);

  setTimeout(() => {
    solutionWrongMsgWrapper.remove();
    messageBox.style.opacity = 0;
    setTimeout(() => {
      messageBox.style.display = "none";
    }, 500);
  }, 5000);
};
