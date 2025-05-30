const source = 'https://tiny.cbpio.pl:8080/api/v2.0/'

function showError(error)
{
    document.querySelector('#urlError').textContent = error
}

async function isAlive() {
    try {
        const response = await fetch(`${source}is_alive`);
        return response.ok;
    } catch (error) {
        return false;
    }
}

async function login(username, password) {
    const res = await fetch(`${source}get_tokens/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username, password: password }),
        // credentials: 'include'
    });

    const data = await res.json();

    if (res.ok) {
        sessionStorage.setItem('access_token', data.access);
        sessionStorage.setItem('refresh_token', data.refresh)
        console.log('Logged in as', username)
        return true;
    } else {
        showError('Login failed');
        return false;
    }
}

async function refreshToken() {
    const res = await fetch(`${source}refresh_token/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({refresh: sessionStorage.getItem('refresh_token')}),
    });
    const data = await res.json();

    if (res.ok) {
        sessionStorage.setItem('access_token', data.access);
        return true;
    } else {
        return false;
    }
}

async function createTinyLink() {
    const longLink = document.querySelector('#linkBox').value
    const outputContainer = document.querySelector('#linkBox')

    await refreshToken()
    const accessToken = sessionStorage.getItem('access_token');
    try {
        regexPattern =/^(https?:\/\/)?([\w-]+\.)+[\w-]{2,}(\/[\w-]*)*\/?$/
         if(!regexPattern.test(inputField.value)){
            showError("Invalid link format: should be like: https://example.com")
        }
        showError()
        const response = await fetch(`${source}short/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${accessToken}`
            },
            body: JSON.stringify({ long_link: longLink })
        })

        const data = await response.json()

        if (response.status == 400){
            showError('There is an issue with the provided link')
        }
        else if (response.status == 403){
            showError('You don\'t have access')
        }
        else if (response.status == 429){
            showError('Too many requests')       
        }
        else if (response.ok){
            // showError(data.code) // ??
            outputContainer.value = data.code
        }
    } catch (error) {
        console.error(error)

        const alive = await isAlive()
        if (!alive)
            showError('No response from server :/')
        else
            showError('An error has occured while creating tiny link: ' + error)
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

login('demouser', 'demodemo')
