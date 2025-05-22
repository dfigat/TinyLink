domain = 'https://link.cbpio.pl:8080'
async function isAlive() {
    try {
        const response = await fetch(`${domain}/api/v1.0/is_alive`);
        return response.ok;
    } catch (error) {
        return false;
    }
}

async function createTinyLink() {
    const longLink = document.querySelector('#linkBox').value
    const outputContainer = document.querySelector('#linkBox')
    try {
         if(!regexPattern.test(inputField.value)){
            showError("Invalid link format: should be like: https://example.com")
        }
        showError()
        const response = await fetch('${domain}/api/v1.0/short/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ long_link: longLink })
        })

        const data = await response.json()

        if (response.status == 400){
            showError('There is an issue with the provided link')
        }
        else if (response.status == 429)
            showError('Too many requests')       

        else if (response.ok){
            // showError(data.code) // ??
            outputContainer.value = data.code
        }
        else if(!response.ok){
            showError("Server is down")
        }

    } catch (error) {
        console.error(error)

        const alive = await isAlive()
        if (!alive)
            showError('Server is down')
        else
            showError('An error has occured while creating tiny link: ' + error)
    }
}

const submitButton = document.querySelector('#SubmitButton')
submitButton.addEventListener('click', createTinyLink)

const inputField = document.querySelector('#linkBox')

inputField.addEventListener('keydown', (event) => {
    regexPattern =/^(https?:\/\/)?([\w-]+\.)+[\w-]{2,}(\/[\w-]*)*\/?$/
    if (event.key === 'Enter') {
        event.preventDefault()
       
        createTinyLink()
    }
})

function showError(error)
{
    document.querySelector('#urlError').textContent = error
}