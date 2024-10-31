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

	// 6. Bulk Delete Mode Controls
	setupBulkDeleteMode();

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
		const togglePasswordButtonCreate = document.getElementById("toggle-create-password");
		const togglePasswordButtonUpdate = document.getElementById("toggle-update-password");
		const copyPasswordButton = document.getElementById("copy-update-password");
		const generatePasswordButtonCreate = document.getElementById("generate-password-create");
		const generatePasswordButtonUpdate = document.getElementById("generate-password-update");
		const updatePasswordInput = document.getElementById("update-password");

		// Password Reveal
		if (togglePasswordButtonCreate || togglePasswordButtonUpdate) {
			if (togglePasswordButtonCreate) {
				togglePasswordButtonCreate.addEventListener("click", function () {
					togglePasswordVisibility(updatePasswordInput, togglePasswordButtonCreate.querySelector("i"));
				});
			}
			if (togglePasswordButtonUpdate) {
				togglePasswordButtonUpdate.addEventListener("click", function () {
					togglePasswordVisibility(updatePasswordInput, togglePasswordButtonUpdate.querySelector("i"));
				});
			}
		}

		// Copy Password
		if (copyPasswordButton && updatePasswordInput) {
			copyPasswordButton.addEventListener("click", function () {
				copyPasswordToClipboard(updatePasswordInput);
			});
		}

		// Generate Password
		if (generatePasswordButtonCreate || generatePasswordButtonUpdate) {
			if (generatePasswordButtonCreate) {
				generatePasswordButtonCreate.addEventListener("click", function () {
					updatePasswordInput.value = generateRandomPassword(12);
				});
			}
			if (generatePasswordButtonUpdate) {
				generatePasswordButtonUpdate.addEventListener("click", function () {
					updatePasswordInput.value = generateRandomPassword(12);
				});
			}
		}
	}

	/**
	 * 4. Setup password buttons to open the update modal with populated details
	 */
	function setupPasswordButtons() {
		const passwordButtons = document.querySelectorAll(".password-button");
		const updatePasswordInput = document.getElementById("update-password");

		if (passwordButtons.length > 0) {
			passwordButtons.forEach((button) => {
				button.addEventListener("click", function (event) {
					event.preventDefault();  // Prevent any form action
					const passwordId = button.getAttribute("data-password-id");
					const appName = button.getAttribute("data-appname");
					const username = button.getAttribute("data-username");
					const password = button.getAttribute("data-password");
					const note = button.getAttribute("data-note");

					// Populate Update Modal
					populateUpdateModal(passwordId, appName, username, password, note);

					// Reset password visibility
					resetPasswordVisibility(updatePasswordInput);

					// Show the modal
					updateModal.showModal();
					document.body.classList.add("modal-active");
				});
			});
		}
	}

	/**
	 * 6. Setup Bulk Delete Mode
	 */
	function setupBulkDeleteMode() {
		const bulkDeleteModeButton = document.getElementById("bulk-delete-mode-button");
		const deleteSelectedButton = document.getElementById("delete-selected-button");
		const checkboxes = document.querySelectorAll(".password-checkbox");
		const bulkDeleteForm = document.getElementById("bulk-delete-form");

		// Toggle bulk delete mode
		bulkDeleteModeButton.addEventListener("click", () => {
			checkboxes.forEach(checkbox => checkbox.style.display = checkbox.style.display === "none" ? "block" : "none");
			deleteSelectedButton.style.display = deleteSelectedButton.style.display === "none" ? "inline-block" : "none";
		});

		// Handle the delete confirmation prompt
		deleteSelectedButton.addEventListener("click", (event) => {
			event.preventDefault();  // Prevent form submission

			// Get the selected checkboxes
			const selectedCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.checked);
			const selectedCount = selectedCheckboxes.length;

			// Show confirmation if there are selected entries
			if (selectedCount > 0) {
				const confirmDelete = confirm(`Are you sure you want to delete ${selectedCount} entries?`);
				if (confirmDelete) {
					bulkDeleteForm.submit();
				}
			} else {
				alert("No entries selected.");
			}
		});
	}

	/**
	 * Function: Toggle Password Visibility (Eye Icon)
	 */
	function togglePasswordVisibility(passwordInput, eyeIcon) {
		if (passwordInput.type === "password") {
			passwordInput.type = "text";
			eyeIcon.classList.replace("fa-eye", "fa-eye-slash");
		} else {
			passwordInput.type = "password";
			eyeIcon.classList.replace("fa-eye-slash", "fa-eye");
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
			password += charset.charAt(Math.floor(Math.random() * charset.length));
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
	function resetPasswordVisibility(passwordInput) {
		passwordInput.type = "password";
		const eyeIcon = document.querySelector("#toggle-update-password i");
		if (eyeIcon) {
			eyeIcon.classList.replace("fa-eye-slash", "fa-eye");
		}
	}
});
