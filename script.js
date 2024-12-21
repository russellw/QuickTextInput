function toggleBurger() {
	const s = document.getElementById("burger-symbol")
	const m = document.getElementById("burger-menu")
	if (s.textContent === "☰") {
		s.textContent = "✕"
		m.style.display = "block"
	} else {
		s.textContent = "☰"
		m.style.display = "none"
	}
}
document.getElementById('contact-form').addEventListener('submit', async (event) => {
	event.preventDefault();
	const formData = {
		domain: window.location.hostname,
		email: document.getElementById('email').value,
		message: document.getElementById('message').value
	};
	const r = document.getElementById("response")
	try {
		const response = await fetch("https://mapsyvgete.execute-api.eu-west-1.amazonaws.com/prod", {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(formData)
		});
		if (!response.ok) {
			throw new Error(`HTTP error! Status: ${response.status}`);
		}
		document.getElementById('contact-form').reset();
		r.textContent = 'Message sent.'
	} catch (error) {
		r.textContent = `${error}`
	}
});
