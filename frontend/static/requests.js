async function createTinyLink() {
    const longLink = document.querySelector('#linkBox').value
    const outputContainer = document.querySelector('#linkBox')
    try {
        const response = await fetch('https://link.cbpio.pl:8080/api/v1.0/short/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ long_link: longLink })
        })

        const data = await response.json()

        if (response.status == 400)
            outputContainer.value = 'There is an issue with the provided link'

        else if (response.ok)
            outputContainer.value = data.code

    } catch (error) {
        console.error(error)
        outputContainer.value = 'An error has occured while creating tiny link: ' + error
    }
}

const submitButton = document.querySelector('#SubmitButton')
submitButton.addEventListener('click', createTinyLink)

const inputField = document.querySelector('#linkBox')

inputField.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault()
        createTinyLink()
    }
})