const inputField = document.getElementById("linkBox");
const button = document.getElementById("SubmitButton");
button.addEventListener("click", () => {
    inputField.classList.add("close");
    setTimeout(() => {
        inputField.classList.remove("close");
        inputField.classList.add("open");
        inputField.value = "TINY LINK HERE";
    }, 400); 
});
