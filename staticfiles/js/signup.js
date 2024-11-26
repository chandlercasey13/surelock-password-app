// main_app/static/js/signup.js

document.addEventListener("DOMContentLoaded", function() {
    const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone; // Detect user's timezone
    console.log(userTimezone);
    const timezoneOption = document.getElementById("user-timezone-option");
    if (userTimezone) {
        timezoneOption.value = userTimezone; // Set value of the user's timezone
        timezoneOption.textContent = userTimezone; // Display user's timezone
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const errorContainer = document.getElementById('error-container');
    if (errorContainer && errorContainer.querySelectorAll('.error-message').length > 0) {
        errorContainer.style.visibility = 'visible';
    }
});