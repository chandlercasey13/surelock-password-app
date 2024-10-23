document.addEventListener("DOMContentLoaded", function () {
    // New password modal controls
    const createModal = document.querySelector("#createmodal");
    const openCreateModal = document.querySelector(".open-button");
    const closeCreateModal = document.querySelector(".close-create-button");

    if (openCreateModal && createModal) {
        openCreateModal.addEventListener("click", function () {
            createModal.showModal();
            document.body.classList.add("modal-active");
        });

        if (closeCreateModal) {
            closeCreateModal.addEventListener("click", function () {
                createModal.close();
                document.body.classList.remove("modal-active");
            });
        }
    }

    // Open update modal when password button is clicked
    const passwordButtons = document.querySelectorAll(".password-button");

    if (passwordButtons.length > 0) {
        passwordButtons.forEach((button) => {
            button.addEventListener("click", function () {
                const passwordId = button.getAttribute("data-password-id");
                const appName = button.getAttribute("data-appname");
                const username = button.getAttribute("data-username");
                const password = button.getAttribute("data-password");
                const note = button.getAttribute("data-note");

                // Populate the modal with the password details
                const updateModal = document.querySelector("#updatemodal");
                document.getElementById("update-appname").value = appName;
                document.getElementById("update-username").value = username;
                document.getElementById("update-password").value = password;
                document.getElementById("update-note").value = note;
                document.getElementById("UpdateForm").setAttribute("data-id", passwordId);

                // Show the modal
                updateModal.showModal();
                document.body.classList.add("modal-active");
            });
        });
    }

    // Close the update modal
    const closeUpdateModal = document.querySelector(".close-update-button");
    if (closeUpdateModal) {
        closeUpdateModal.addEventListener("click", function () {
            const updateModal = document.querySelector("#updatemodal");
            updateModal.close();
            document.body.classList.remove("modal-active");
        });
    }

    // Password reveal toggle for Create and Update forms
    function togglePasswordVisibility(inputId, toggleButtonId) {
        const passwordInput = document.getElementById(inputId);
        const toggleButton = document.getElementById(toggleButtonId);
        if (passwordInput && toggleButton) {
            const eyeIcon = toggleButton.querySelector("i");

            toggleButton.addEventListener("click", function () {
                if (passwordInput.type === "password") {
                    passwordInput.type = "text";
                    eyeIcon.classList.remove("fa-eye");
                    eyeIcon.classList.add("fa-eye-slash");
                } else {
                    passwordInput.type = "password";
                    eyeIcon.classList.remove("fa-eye-slash");
                    eyeIcon.classList.add("fa-eye");
                }
            });
        }
    }

    // Toggle password visibility for create and update forms
    togglePasswordVisibility("create-password", "toggle-create-password");
    togglePasswordVisibility("update-password", "toggle-update-password");

    // Generate random password for Update modal
    const generateUpdatePasswordBtn = document.getElementById("generate-update-password");
    const updatePasswordInput = document.getElementById("update-password");

    if (generateUpdatePasswordBtn && updatePasswordInput) {
        generateUpdatePasswordBtn.addEventListener("click", function () {
            const randomPassword = generateRandomPassword(12);
            updatePasswordInput.value = randomPassword;
        });
    }

    // Function to generate a random password
    function generateRandomPassword(length) {
        const charset =
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+~`|}{[]:;?><,./-=";
        let password = "";
        for (let i = 0; i < length; i++) {
            const randomIndex = Math.floor(Math.random() * charset.length);
            password += charset[randomIndex];
        }
        return password;
    }

    // Copy password to clipboard for Update modal
    const copyUpdatePasswordBtn = document.getElementById("copy-update-password");
    if (copyUpdatePasswordBtn && updatePasswordInput) {
        copyUpdatePasswordBtn.addEventListener("click", function () {
            updatePasswordInput.select();
            document.execCommand("copy");
            alert("Password copied to clipboard!");
        });
    }

    // Delete password functionality
    const deleteButton = document.getElementById("delete-button");
    if (deleteButton) {
        deleteButton.addEventListener("click", function (event) {
            event.preventDefault();

            const form = document.getElementById("UpdateForm");
            const passwordId = form.getAttribute("data-id");
            const appName = form.getAttribute("data-appname");

            if (appName && confirm(`Are you sure you want to delete ${appName}?`)) {
                fetch(`/passwords/${passwordId}/delete/`, {
                    method: "DELETE",
                    headers: {
                        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                        "Content-Type": "application/json",
                    },
                })
                    .then((response) => {
                        if (response.ok) {
                            window.location.href = "/passwords/";
                        } else {
                            alert("Failed to delete the password.");
                        }
                    })
                    .catch((err) => {
                        console.error("Error:", err);
                    });
            }
        });
    }
});
