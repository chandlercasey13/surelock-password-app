//main_app/static/js/typewriter.js

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