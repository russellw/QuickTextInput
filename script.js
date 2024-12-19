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
	document.getElementById('contactForm').addEventListener('submit', async (event) => {
		event.preventDefault(); 
		const formData = {
			domain: 'quicktextinput.com',
			name: '',
			email: document.getElementById('email').value,
			phone:'',
			message: document.getElementById('message').value
		};
alert(JSON.stringify(formData))

		try {
			const response = await fetch("https://mapsyvgete.execute-api.eu-west-1.amazonaws.com/prod", {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify(formData)
			});

alert(response)
			if (!response.ok) {
				throw new Error(`HTTP error! Status: ${response.status}`);
			}

			const result = await response.json();
			alert(result)
			console.log("Success:", result);
			// You can display a success message to the user here
		} catch (error) {
			console.error("Error:", error);
			// Display an error message to the user if needed
		}
	});
