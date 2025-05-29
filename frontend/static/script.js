const linkBox = document.getElementById("linkBox");
const button = document.getElementById("SubmitButton");

const playAnimation = () => {
    linkBox.classList.remove("open")
    linkBox.classList.add("close");
    setTimeout(() => {
        linkBox.classList.remove("close");
        linkBox.classList.add("open");
    }, 400);
};

button.addEventListener("click", playAnimation)

linkBox.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault()
        playAnimation()
    }
})
