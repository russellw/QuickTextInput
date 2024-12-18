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
