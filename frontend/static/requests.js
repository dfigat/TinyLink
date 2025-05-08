async function createTinyLink() {
    const longLink = document.querySelector('.tiny_link_input').value
    const outputContainer = document.querySelector('.tiny_link_output')
    try {
        const response = await fetch('http://link.cbpio.pl:8080/api/v1.0/short/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ long_link: longLink })
        })

        const data = await response.json()

        if(response.status == 400)
            outputContainer.textContent = 'There is an issue with the provided link'

        else if (response.ok)
            outputContainer.textContent = data.code

    } catch (error) {
        console.error(error)
        outputContainer.textContent = 'An error has occured while creating tiny link: ' + error
    }
}

const submitButton = document.querySelector('.tiny_link_submit')
submitButton.addEventListener('click', createTinyLink)