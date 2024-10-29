document.addEventListener("DOMContentLoaded", function () {
	// 1. Modal Controls
	const createModal = document.querySelector("#createmodal");
	const updateModal = document.querySelector("#updatemodal");
	const openCreateModal = document.querySelector(".open-button");
	const closeCreateModal = document.querySelector(".close-create-button");
	const closeUpdateModal = document.querySelector(".close-update-button");

	// 2. Event Listener Setup for Opening/Closing Modals
	setupModalEvents();

	// 3. Password-Related Actions (Reveal, Copy, Generate)
	setupPasswordActions();

	// 4. Password Button Click to Load Details in the Update Modal
	setupPasswordButtons();

	// 5. Delete Password Functionality
	// setupDeleteFunction();

	/**
	 * 2. Setup event listeners for opening and closing modals
	 */
	function setupModalEvents() {
		// Open the Create Modal
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

		// Close the Update Modal
		if (closeUpdateModal) {
			closeUpdateModal.addEventListener("click", function () {
				updateModal.close();
				document.body.classList.remove("modal-active");
			});
		}
	}

	/**
	 * 3. Setup password reveal, copy, and generation actions
	 */
	function setupPasswordActions() {
		const togglePasswordBtn = document.getElementById("toggle-update-password");
		const copyPasswordBtn = document.getElementById("copy-update-password");
		const generatePasswordBtn = document.getElementById("generate-update-password");
		const updatePasswordInput = document.getElementById("update-password");

		// Password Reveal
		if (togglePasswordBtn && updatePasswordInput) {
			togglePasswordBtn.addEventListener("click", function () {
				togglePasswordVisibility(updatePasswordInput, togglePasswordBtn.querySelector("i"));
			});
		}

		// Copy Password
		if (copyPasswordBtn && updatePasswordInput) {
			copyPasswordBtn.addEventListener("click", function () {
				copyPasswordToClipboard(updatePasswordInput);
			});
		}

		// Generate Password
		if (generatePasswordBtn && updatePasswordInput) {
			generatePasswordBtn.addEventListener("click", function () {
				updatePasswordInput.value = generateRandomPassword(12);
			});
		}
	}

	/**
	 * 4. Setup password buttons to open the update modal with populated details
	 */
	function setupPasswordButtons() {
		const passwordButtons = document.querySelectorAll(".password-button");
        const updatePasswordInput = document.getElementById("update-password");
        const togglePasswordBtn = document.getElementById("toggle-update-password");
		if (passwordButtons.length > 0) {
			passwordButtons.forEach((button) => {
				button.addEventListener("click", function () {
					const passwordId = button.getAttribute("data-password-id");
					const appName = button.getAttribute("data-appname");
					const username = button.getAttribute("data-username");
					const password = button.getAttribute("data-password");
					const note = button.getAttribute("data-note");

					// Populate Update Modal
					populateUpdateModal(passwordId, appName, username, password, note);

					// Reset password visibility
					resetPasswordVisibility(updatePasswordInput, togglePasswordBtn.querySelector("i"));

					// Show the modal
					updateModal.showModal();
					document.body.classList.add("modal-active");
				});
			});
		}
	}

	/**
	 * 5. Setup the delete button functionality
	 */
	// function setupDeleteFunction() {
	// 	const deleteButton = document.getElementById("delete-button");

	// 	if (deleteButton) {
	// 		deleteButton.addEventListener("click", function (event) {
	// 			event.preventDefault();

	// 			const form = document.getElementById("UpdateForm");
	// 			const passwordId = form.getAttribute("data-id");
	// 			const appName = form.getAttribute("data-appname");

	// 			if (appName && confirm(`Are you sure you want to delete ${appName}?`)) {
	// 				deletePassword(passwordId);
	// 			}
	// 		});
	// 	}
	// }

	/**
	 * Function: Toggle Password Visibility (Eye Icon)
	 */
	function togglePasswordVisibility(passwordInput, eyeIcon) {
		if (passwordInput.type === "password") {
			passwordInput.type = "text"; // Show the password
			eyeIcon.classList.remove("fa-eye"); // Change icon to eye-slash
			eyeIcon.classList.add("fa-eye-slash");
		} else {
			passwordInput.type = "password"; // Hide the password
			eyeIcon.classList.remove("fa-eye-slash"); // Change icon to eye
			eyeIcon.classList.add("fa-eye");
		}
	}

	/**
	 * Function: Copy Password to Clipboard
	 */
	function copyPasswordToClipboard(passwordInput) {
		passwordInput.select();
		document.execCommand("copy");
		alert("Password copied to clipboard!");
	}

	/**
	 * Function: Generate Random Password
	 */
	function generateRandomPassword(length) {
		const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+~`|}{[]:;?><,./-=";
		let password = "";
		for (let i = 0; i < length; i++) {
			const randomIndex = Math.floor(Math.random() * charset.length);
			password += charset[randomIndex];
		}
		return password;
	}

	/**
	 * Function: Populate Update Modal with Password Details
	 */
	function populateUpdateModal(passwordId, appName, username, password, note) {
        document.getElementById("update-modal-appname").innerText = appName;
		document.getElementById("update-appname").value = appName;
		document.getElementById("update-username").value = username;
		document.getElementById("update-password").value = password;
		document.getElementById("update-note").value = note;
		document.getElementById("UpdateForm").setAttribute("data-id", passwordId);
        document.getElementById("update-password-id").value = passwordId;
	}

	/**
	 * Function: Reset Password Visibility in Update Modal
	 */
	function resetPasswordVisibility(passwordInput, eyeIcon) {
		passwordInput.type = "password";
		eyeIcon.classList.remove("fa-eye-slash");
		eyeIcon.classList.add("fa-eye");
	}

	/**
	 * Function: Delete Password via Fetch Request
	 */
	// function deletePassword(passwordId) {
	// 	fetch(`/passwords/${passwordId}/delete/`, {
	// 		method: "DELETE",
	// 		headers: {
	// 			"X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
	// 			"Content-Type": "application/json",
	// 		},
	// 	})
	// 		.then((response) => {
	// 			if (response.ok) {
	// 				window.location.href = "/passwords/";
	// 			} else {
	// 				alert("Failed to delete the password.");
	// 			}
	// 		})
	// 		.catch((err) => {
	// 			console.error("Error:", err);
	// 		});
	// }
});
