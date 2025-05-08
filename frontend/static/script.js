const inputField = document.getElementById("linkBox");
const button = document.getElementById("SubmitButton");
button.addEventListener("click", () => {
    inputField.classList.remove("open")
    inputField.classList.add("close");
    setTimeout(() => {
        inputField.classList.remove("close");
        inputField.classList.add("open");
<<<<<<< HEAD
        inputField.value = "TINY LINK HERE";
=======
>>>>>>> 442465a (Few Fixes)
    }, 400); 
});
