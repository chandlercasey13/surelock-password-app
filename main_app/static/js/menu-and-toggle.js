//main_app/static/js/menu-and-toggle.js

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
                          errorMessage.classList.add("error-message");
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
