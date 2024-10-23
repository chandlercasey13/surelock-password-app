// TxtRotate class: handles the rotating text effect.
class TxtRotate {
  // Constructor to initialize the rotating text instance.
  constructor(element, toRotate, period = 2000) {
      this.toRotate = toRotate;       // Array of texts to rotate
      this.element = element;         // HTML element to display the text
      this.loopNum = 0;               // Tracks the current word in the loop
      this.period = period;           // Period between text rotations
      this.txt = "";                  // Current displayed text
      this.isDeleting = false;        // Flag to track if it's deleting text
      this.tick();                    // Start the text rotation animation
  }

  // Function to handle the typing/deleting effect for text rotation
  tick() {
      // Determine the current text based on the loop number
      const i = this.loopNum % this.toRotate.length;
      const fullTxt = this.toRotate[i]; // Get the full text for the current index

      // Update current text by either adding or deleting characters
      this.txt = this.isDeleting
          ? fullTxt.substring(0, this.txt.length - 1) // Delete one character
          : fullTxt.substring(0, this.txt.length + 1); // Add one character

      // Update the inner HTML of the element with the current portion of the text
      this.element.innerHTML = `<span class="wrap">${this.txt}</span>`;

      // Determine the delay for the next tick (typing speed)
      let delta = 200 - Math.random() * 100; // Random speed for natural typing effect
      if (this.isDeleting) delta /= 2; // Decrease speed when deleting characters

      // If the full text is typed, pause for the period before deleting
      if (!this.isDeleting && this.txt === fullTxt) {
          delta = this.period;        // Pause before deleting
          this.isDeleting = true;     // Start deleting characters next
      } 
      // If the text is fully deleted, move to the next word
      else if (this.isDeleting && this.txt === "") {
          this.isDeleting = false;    // Stop deleting and start typing the next word
          this.loopNum++;             // Move to the next text in the array
          delta = 350;                // Short delay before typing the next word
      }

      // Schedule the next tick for the animation
      setTimeout(() => this.tick(), delta);
  }
}

// When the window is loaded, initialize the TxtRotate function for elements with the 'txt-rotate' class
window.onload = function () {
	var elements = document.getElementsByClassName("txt-rotate"); // Select all elements with class "txt-rotate"
	for (var i = 0; i < elements.length; i++) {
		var toRotate = elements[i].getAttribute("data-rotate");  // Get the array of texts from 'data-rotate'
		var period = elements[i].getAttribute("data-period");    // Get the period from 'data-period'
		if (toRotate) {
			new TxtRotate(elements[i], JSON.parse(toRotate), period); // Initialize TxtRotate with parsed text array
		}
	}

	// Inject CSS into the page to add a blinking cursor effect for the rotating text
	var css = document.createElement("style");
	css.type = "text/css";
	css.innerHTML = ".txt-rotate > .wrap { border-right: 0.08em solid #666 }"; // Styling for the cursor
	document.body.appendChild(css); // Append the style to the document
};

// Function to handle the button animation for toggling menu visibility
function xButton() {
  const button = document.querySelector(".toggle"); // Get the toggle button element
  const isExpanded = button.getAttribute("aria-expanded") === "true"; // Check if the button is currently expanded
  button.setAttribute("aria-expanded", !isExpanded); // Toggle the 'aria-expanded' attribute
  button.classList.toggle("active"); // Toggle the 'active' class on the button

  // Get the three rectangles inside the button for the animation effect
  const rectOne = document.querySelector(".one");
  const rectTwo = document.querySelector(".two");
  const rectThree = document.querySelector(".three");

  // Add/remove animation classes for each rectangle
  rectOne.classList.toggle("animate");
  rectTwo.classList.toggle("animate");
  rectThree.classList.toggle("animate");
}

// Function to toggle the menu visibility and call additional functions if the menu is opened
function toggleMenu() {
  xButton(); // Call the xButton function to handle button animations
  const showcase = document.querySelector(".showcase"); // Get the menu element
  showcase.classList.toggle("active"); // Toggle the 'active' class on the menu

  // If the login form is visible after toggling, add the event listener
  if (showcase.classList.contains("active")) {
      addLoginFormListener();  // Call function to add event listener for login form
  }
}

// Function to add the login form submit event listener
function addLoginFormListener() {
  const loginForm = document.querySelector(".login"); // Get the login form element
  if (loginForm) {
      // Check if the listener was already added to prevent duplicates
      if (!loginForm.hasAttribute('listener-added')) {
          // Add event listener for form submission
          loginForm.addEventListener("submit", function (event) {
              event.preventDefault(); // Prevent default form submission behavior

              // Show loading indicator during the form submission
              const buttonText = document.querySelector(".login-button"); // Get the login button
              const loadingIndicator = document.getElementById("loading-indicator"); // Get loading spinner
              const errorContainer = document.querySelector(".error-messages"); // Get error message container

              buttonText.style.display = "none"; // Hide the button text
              loadingIndicator.style.display = "flex"; // Show the loading indicator

              // Gather form data to submit
              const formData = new FormData(loginForm);
              const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // CSRF token for security

              // Use AJAX to submit the form via POST request
              fetch(ajaxLoginUrl, {
                  method: "POST",
                  body: formData,
                  headers: {
                      "X-CSRFToken": csrfToken, // CSRF token header
                  },
              })
              .then((response) => response.json()) // Parse the JSON response
              .then((data) => {
                  // After receiving a response, hide the loading indicator
                  loadingIndicator.style.display = "none";
                  buttonText.style.display = "inline";

                  if (data.success) {
                      // Reload the page after a successful login
                      window.location.reload();
                  } else {
                      // If login fails, display error messages
                      errorContainer.innerHTML = ""; // Clear any previous errors
                      data.errors.forEach((error) => {
                          const errorMessage = document.createElement("p");
                          errorMessage.classList.add("error-text");
                          errorMessage.innerText = error; // Add error message
                          errorContainer.appendChild(errorMessage);
                      });
                  }
              })
              .catch((error) => {
                  // Handle error in login process
                  loadingIndicator.style.display = "none"; // Hide loading indicator
                  buttonText.style.display = "inline";
                  console.error("Error:", error); // Log error to the console
              });
          });

          // Mark the listener as added to avoid multiple listeners
          loginForm.setAttribute('listener-added', true);
      }
  }
}
