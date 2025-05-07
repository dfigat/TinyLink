async function createTinyLink() {
    const longLink = document.querySelector('.tiny_link_input').value
    const outputContainer = document.querySelector('.tiny_link_output')
    try {
        const response = await fetch('http://link.cbpio.pl/api/v1.0/short', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ longLink: longLink })
        })

        const data = await response.json()

        if (response.ok)
            outputContainer.textContent = data.code

    } catch (error) {
        console.error(error)
        outputContainer.textContent = 'An error has occured while creating tiny link: ' + error
    }
}
console.log(document.querySelector('.tiny_link_input').value);

const submitButton = document.querySelector('.tiny_link_submit')
submitButton.addEventListener('click', createTinyLink)