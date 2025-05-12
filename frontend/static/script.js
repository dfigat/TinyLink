const linkBox = document.getElementById("linkBox");
const button = document.getElementById("SubmitButton");

const playAnimation = () => {
    linkBox.classList.remove("open")
    linkBox.classList.add("close");
    setTimeout(() => {
        linkBox.classList.remove("close");
        linkBox.classList.add("open");
        // linkBox.value = "TINY LINK HERE";
    }, 400);
};

button.addEventListener("click", playAnimation)

// const urlPattern = /^(https?:\/\/)?([\w-]+\.)+[\w-]{2,}(\/[\w-]*)*\/?$/;

linkBox.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault()
        playAnimation()
    }
})

