document.addEventListener("DOMContentLoaded", function () {
	//Modal Controls
	const createModal = document.querySelector("#createmodal");
	const updateModal = document.querySelector("#updatemodal");
	const openCreateModal = document.querySelector(".open-button");
	const closeCreateModal = document.querySelector(".close-create-button");
	const closeUpdateModal = document.querySelector(".close-update-button");

	//Event Listener Setup for Opening/Closing Modals
	setupModalEvents();



	//Password Button Click to Load Details in the Update Modal
	setupPasswordButtons();

	//Bulk Delete Mode Controls
	setupBulkDeleteMode();

	//Setup password reveal, copy, and generation actions
	function setupPasswordActions() {
		const togglePasswordButtonCreate = document.getElementById(
			"toggle-create-password"
		);
		const togglePasswordButtonUpdate = document.getElementById(
			"toggle-update-password"
		);
		const copyPasswordButton = document.getElementById(
			"copy-update-password"
		);
		const generatePasswordButtonCreate = document.getElementById(
			"generate-password-create"
		);
		const generatePasswordButtonUpdate = document.getElementById(
			"generate-password-update"
		);
		let passwordInput = document.getElementById("update-password");

		//Password Reveal
		if (togglePasswordButtonCreate || togglePasswordButtonUpdate) {
			passwordInput = document.getElementById("update-password").value;

			console.log(
				"passwordInput = document.getElementById(update-password).value: ",
				passwordInput
			);

			if (togglePasswordButtonCreate) {
				console.log("passwordInput: ", passwordInput);
				togglePasswordButtonCreate.addEventListener("click", function () {
					togglePasswordVisibility(
						document.getElementById("create-password"),
						togglePasswordButtonCreate.querySelector("i")
					);
				});
			}
			if (togglePasswordButtonUpdate) {
				console.log("passwordInput: ", passwordInput);
				togglePasswordButtonUpdate.addEventListener("click", function () {
					togglePasswordVisibility(
						document.getElementById("update-password"),
						togglePasswordButtonCreate.querySelector("i")
					);
					console.log("passwordInput: ", passwordInput);
				});
			}
		}

		//Copy Password
		if (copyPasswordButton && passwordInput) {
			copyPasswordButton.addEventListener("click", function () {
				copyPasswordToClipboard(passwordInput);
			});
		}

		//Generate Password
		if (generatePasswordButtonCreate || generatePasswordButtonUpdate) {
			if (generatePasswordButtonCreate) {
				generatePasswordButtonCreate.addEventListener("click", function () {
					passwordInput.value = generateRandomPassword(12);
				});
			}
			if (generatePasswordButtonUpdate) {
				generatePasswordButtonUpdate.addEventListener("click", function () {
					passwordInput.value = generateRandomPassword(12);
				});
			}
		}
	}
	//Setup event listeners for opening and closing modals
	function setupModalEvents() {
		//Open the Create Modal
		if (openCreateModal && createModal) {
			openCreateModal.addEventListener("click", function () {
				createModal.showModal();
				document.body.classList.add("modal-active");
			});
				//Password-Related Actions (Reveal, Copy, Generate)
	setupPasswordActions();

			if (closeCreateModal) {
				closeCreateModal.addEventListener("click", function () {
					createModal.close();
					document.body.classList.remove("modal-active");
				});
			}
		}

		//Close the Update Modal
		if (closeUpdateModal) {
			closeUpdateModal.addEventListener("click", function () {
				updateModal.close();
				document.body.classList.remove("modal-active");
			});
		}
	}
	
	//Setup password buttons to open the update modal with populated details
	function setupPasswordButtons() {
		const passwordButtons = document.querySelectorAll(".password-button");
		const passwordInput = document.getElementById("update-password");

		if (passwordButtons.length > 0) {
			passwordButtons.forEach((button) => {
				button.addEventListener("click", function (event) {
					event.preventDefault(); //Prevent any form action
					const passwordId = button.getAttribute("data-password-id");
					const appName = button.getAttribute("data-appname");
					const username = button.getAttribute("data-username");
					const password = button.getAttribute("data-password");
					const note = button.getAttribute("data-note");

					//Populate Update Modal
					populateUpdateModal(
						passwordId,
						appName,
						username,
						password,
						note
					);

					//Reset password visibility
					resetPasswordVisibility(passwordInput);

					//Show the modal
					updateModal.showModal();
					document.body.classList.add("modal-active");
				});
			});
		}
	}

	//Setup Bulk Delete Mode
	function setupBulkDeleteMode() {
		const bulkDeleteModeButton = document.getElementById(
			"bulk-delete-mode-button"
		);
		const deleteSelectedButton = document.getElementById(
			"delete-selected-button"
		);
		const checkboxes = document.querySelectorAll(".password-checkbox");
		const bulkDeleteForm = document.getElementById("bulk-delete-form");

		//Toggle bulk delete mode
		bulkDeleteModeButton.addEventListener("click", () => {
			checkboxes.forEach(
				(checkbox) =>
					(checkbox.style.display =
						checkbox.style.display === "none" ? "block" : "none")
			);
			deleteSelectedButton.style.display =
				deleteSelectedButton.style.display === "none"
					? "inline-block"
					: "none";
		});

		//Handle the delete confirmation prompt
		deleteSelectedButton.addEventListener("click", (event) => {
			event.preventDefault(); //Prevent form submission

			//Get the selected checkboxes
			const selectedCheckboxes = Array.from(checkboxes).filter(
				(checkbox) => checkbox.checked
			);
			const selectedCount = selectedCheckboxes.length;

			//Show confirmation if there are selected entries
			if (selectedCount > 0) {
				const confirmDelete = confirm(
					`Are you sure you want to delete ${selectedCount} entries?`
				);
				if (confirmDelete) {
					bulkDeleteForm.submit();
				}
			} else {
				alert("No entries selected.");
			}
		});
	}

	//Function: Copy Password to Clipboard
	function copyPasswordToClipboard(passwordInput) {
		passwordInput.select();
		document.execCommand("copy");
		alert("Password copied to clipboard!");
	}

	//Function: Generate Random Password
	function generateRandomPassword(length) {
		const charset =
			"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+~`|}{[]:;?><,./-=";
		let password = "";
		for (let i = 0; i < length; i++) {
			password += charset.charAt(Math.floor(Math.random() * charset.length));
		}
		return password;
	}

	//Function: Populate Update Modal with Password Details
	function populateUpdateModal(passwordId, appName, username, password, note) {
		document.getElementById("update-modal-appname").innerText = appName;
		document.getElementById("update-appname").value = appName;
		document.getElementById("update-username").value = username;
		document.getElementById("update-password").value = password;
		document.getElementById("update-note").value = note;
		document.getElementById("UpdateForm").setAttribute("data-id", passwordId);
		document.getElementById("update-password-id").value = passwordId;
	}

	//Function: Reset Password Visibility in Update Modal
	function resetPasswordVisibility(passwordInput) {
		passwordInput.type = "password";
		const eyeIcon = document.querySelector("#toggle-update-password i");
		if (eyeIcon) {
			eyeIcon.classList.replace("fa-eye-slash", "fa-eye");
		}
	}

	//Function to toggle password visibility for other modals
	function togglePasswordVisibility(passwordFieldId, toggleButton) {
		const passwordField = document.getElementById(passwordFieldId);
		console.log("This is the password field ID: ", passwordFieldId);
		console.log("This is the password field value is: ", passwordField.value);
		console.log("This is the password field type is: ", passwordField.type);

		if (passwordField.type === "password") {
			passwordField.type = "text";
			toggleButton.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
		} else {
			passwordField.type = "password";
			toggleButton.innerHTML = '<i class="fa-solid fa-eye"></i>';
		}
	}

	//Utility to retrieve CSRF token from cookies
	function getCSRFToken() {
		let cookieValue = null;
		const name = "csrftoken";
		if (document.cookie && document.cookie !== "") {
			const cookies = document.cookie.split(";");
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();
				if (cookie.substring(0, name.length + 1) === name + "=") {
					cookieValue = decodeURIComponent(
						cookie.substring(name.length + 1)
					);
					break;
				}
			}
		}
		return cookieValue;
	}

	//Toggle password visibility in the create password modal
	document
		.getElementById("toggle-create-password")
		.addEventListener("click", function () {
			togglePasswordVisibility("create-password", this);
		});

	//Toggle password visibility in the update password modal
	document
		.getElementById("toggle-update-password")
		.addEventListener("click", function () {
			const passwordField = document.getElementById("update-password");
			const passwordId = document.getElementById("update-password-id").value;

			if (passwordField.type === "password") {
				//Fetch plaintext password securely
				fetch("/reveal-password/", {
					method: "POST",
					headers: {
						"X-CSRFToken": getCSRFToken(), //Get CSRF token
						"Content-Type": "application/x-www-form-urlencoded",
					},
					body: new URLSearchParams({ password_id: passwordId }),
				})
					.then((response) => response.json())
					.then((data) => {
						if (data.password) {
							passwordField.type = "text";
							passwordField.value = data.password;
							this.innerHTML = '<i class="fa-solid fa-eye-slash"></i>'; //Change icon to 'hide'
						} else {
							alert(data.error || "Failed to retrieve password.");
						}
					})
					.catch((error) => console.error("Error:", error));
			} else {
				passwordField.type = "password";
				this.innerHTML = '<i class="fa-solid fa-eye"></i>'; //Change icon to 'show'
			}
		});
});
