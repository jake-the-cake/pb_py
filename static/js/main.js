function hideModal() {
	modal = document.querySelector('.modal')
	closeAndHide(modal)
}

function closeAndHide(element) {
	element.classList.remove('open')		
	setTimeout(() => element.classList.add('hidden'), 200)
}

function getFormDataObj(form) {
	return Object.fromEntries(new FormData(form))
}

async function apiPostRequest(url, data) {
	try {
		req = await fetch('http://localhost:5000' + url, {
			method: 'POST',
			body: JSON.stringify(data),
			headers: {
				'Content-Type': 'application/json'
			}
		})
		return await req.json()
	}
	catch (e) {
		return { error: e }
	}
}

function bindSignUpForms(){
	links = Array.from(document.querySelectorAll('a')).filter((link) => link.hash === '#sign-up')
	
	if (links.length > 0) {
		links.forEach(link => {
			link.onclick = (e) => {
				e.preventDefault()
				modal = document.querySelector('.modal')
				modal.classList.remove('hidden')
				modal.classList.add('open')
				modal.onclick = (e) => {
					if (e.target === modal) {
						closeAndHide(modal)
					}
				}
			}
		})
	}
}

window.addEventListener('DOMContentLoaded', () => {
	bindSignUpForms()
})