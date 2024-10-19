// const menuToggle = document.querySelector(".toggle");
// const showcase = document.querySelector(".showcase");

// menuToggle.addEventListener("click", () => {
// 	showcase.classList.toggle("active");
// 	setTimeout(() => {
// 		menuToggle.classList.toggle("active");
// 	}, 500);
// });

var TxtRotate = function (el, toRotate, period) {
	this.toRotate = toRotate;
	this.el = el;
	this.loopNum = 0;
	this.period = parseInt(period, 10) || 2000;
	this.txt = "";
	this.tick();
	this.isDeleting = false;
};

TxtRotate.prototype.tick = function () {
	var i = this.loopNum % this.toRotate.length;
	var fullTxt = this.toRotate[i];

	if (this.isDeleting) {
		this.txt = fullTxt.substring(0, this.txt.length - 1);
	} else {
		this.txt = fullTxt.substring(0, this.txt.length + 1);
	}

	this.el.innerHTML = '<span class="wrap">' + this.txt + "</span>";

	var that = this;
	var delta = 300 - Math.random() * 100;

	if (this.isDeleting) {
		delta /= 2;
	}

	if (!this.isDeleting && this.txt === fullTxt) {
		delta = this.period;
		this.isDeleting = true;
	} else if (this.isDeleting && this.txt === "") {
		this.isDeleting = false;
		this.loopNum++;
		delta = 500;
	}

	setTimeout(function () {
		that.tick();
	}, delta);
};

window.onload = function () {
	var elements = document.getElementsByClassName("txt-rotate");
	for (var i = 0; i < elements.length; i++) {
		var toRotate = elements[i].getAttribute("data-rotate");
		var period = elements[i].getAttribute("data-period");
		if (toRotate) {
			new TxtRotate(elements[i], JSON.parse(toRotate), period);
		}
	}
	// INJECT CSS
	var css = document.createElement("style");
	css.type = "text/css";
	css.innerHTML = ".txt-rotate > .wrap { border-right: 0.08em solid #666 }";
	document.body.appendChild(css);
};

document.addEventListener("DOMContentLoaded", function () {
	const loginForm = document.querySelector(".login"); // Login form selector
	const errorContainer = document.querySelector(".error-messages"); // Error message container
	const usernameDisplay = document.querySelector(".username-display"); // Where the username will be displayed

	// Listen for the login form submission
	loginForm.addEventListener("submit", function (event) {
		event.preventDefault(); // Prevent default form submission behavior

		// Gather form data
		const formData = new FormData(loginForm);
		const csrfToken = document.querySelector(
			"[name=csrfmiddlewaretoken]"
		).value;

		// Use the dynamic URL from base.html
		fetch(ajaxLoginUrl, {
			method: "POST",
			body: formData,
			headers: {
				"X-CSRFToken": csrfToken,
			},
		})
			.then((response) => response.json()) // Parse JSON response
			.then((data) => {
				if (data.success) {
					// If login is successful, update the username display
					usernameDisplay.innerText = data.username;
					document.querySelector(".menu").classList.remove("active"); // Close the menu
				} else {
					// If login fails, display error messages
					errorContainer.innerHTML = ""; // Clear any previous errors
					data.errors.forEach((error) => {
						const errorMessage = document.createElement("p");
						errorMessage.classList.add("error-text");
						errorMessage.innerText = error;
						errorContainer.appendChild(errorMessage);
					});
				}
			})
			.catch((error) => {
				console.error("Error:", error); // Log any errors in the console
			});
	});
});

// Toggle function to open/close the menu and add/remove active class
function toggleMenu() {
	const button = document.querySelector(".toggle");
	const showcase = document.querySelector(".showcase");
	showcase.classList.toggle("active");
	const isExpanded = button.getAttribute("aria-expanded") === "true";
	button.setAttribute("aria-expanded", !isExpanded);

	// Toggle classes for the button and the SVG bars
	button.classList.toggle("active");

	const rectOne = document.querySelector(".one");
	const rectTwo = document.querySelector(".two");
	const rectThree = document.querySelector(".three");

	// Add/remove animation classes
	rectOne.classList.toggle("animate");
	rectTwo.classList.toggle("animate");
	rectThree.classList.toggle("animate");
}
