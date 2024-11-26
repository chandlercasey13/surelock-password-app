
const createModal = document.querySelector('#createmodal');
const openCreateModal = document.querySelector('.open-button'); 
const closeCreateModal = document.querySelector('.close-create-button');

openCreateModal.addEventListener('click', function () {
    createModal.showModal();
})
closeCreateModal.addEventListener('click', function () {
    createModal.close();
})
const updateModal = document.querySelector('#updatemodal');
const allPasswords = document.querySelectorAll('.card')

{%if password_id%}

updateModal.showModal()
   
{%endif%}

function navigateToUrl(url) {
    // Show the loading spinner
    document.getElementById('loading-spinner').style.display = 'flex';
    // Simulate navigation (you would replace this with actual navigation)
        window.location.href = url;           
}      
// Hide the loading spinner on page load
window.addEventListener('load', function() {      
    document.getElementById('loading-spinner').style.display = 'none';     
});   
const closeUpdateModal = document.querySelector('.close-update-button')
closeUpdateModal.addEventListener('click', function () {
updateModal.close();
});
document.addEventListener("DOMContentLoaded", function() {
// Function to generate a random strong password
function generateRandomPassword(length) {
    const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+~`|}{[]:;?><,./-=";
    let password = "";
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * charset.length);
        password += charset[randomIndex];
    }
    return password;
}   
// Generate Password for Update Modal
const generateUpdatePasswordBtn = document.getElementById("generate-update-password");
const updatePasswordInput = document.getElementById("update-password");   
generateUpdatePasswordBtn.addEventListener("click", function() {
    const randomPassword = generateRandomPassword(12); // You can change the length as desired
    updatePasswordInput.value = randomPassword;
});   
// Toggle Password Visibility for Update Modal
const toggleUpdatePasswordBtn = document.getElementById('toggle-update-password');
const updateEyeIcon = toggleUpdatePasswordBtn.querySelector('i'); 
toggleUpdatePasswordBtn.addEventListener('click', function() {
    if (updatePasswordInput.type === 'password') {
        updatePasswordInput.type = 'text';
        updateEyeIcon.classList.remove("fa-eye");
        updateEyeIcon.classList.add("fa-eye-slash");
    } else {
        updatePasswordInput.type = 'password';
        updateEyeIcon.classList.remove("fa-eye-slash");
        updateEyeIcon.classList.add("fa-eye");
    }
});

// Copy Password for Update Modal
const copyUpdatePasswordBtn = document.getElementById("copy-update-password");

copyUpdatePasswordBtn.addEventListener("click", function() {
    updatePasswordInput.select();
    updatePasswordInput.setSelectionRange(0, 99999);

    navigator.clipboard.writeText(updatePasswordInput.value).then(() => {
        alert("Password copied to clipboard!");
    }).catch(err => {
        console.error("Failed to copy password: ", err)
    });
});

// Toggle Password Visibility for Create Modal
const createPasswordInput = document.getElementById('create-password');
const toggleCreatePasswordBtn = document.getElementById('toggle-create-password');
const createEyeIcon = toggleCreatePasswordBtn.querySelector('i');

toggleCreatePasswordBtn.addEventListener('click', function () {
    if (createPasswordInput.type === 'password') {
        createPasswordInput.type = 'text';
        createEyeIcon.classList.remove("fa-eye");
        createEyeIcon.classList.add("fa-eye-slash");
    } else {
        createPasswordInput.type = 'password';
        createEyeIcon.classList.remove("fa-eye-slash");
        createEyeIcon.classList.add("fa-eye");
    }
});

// Create Password Copy Button
const copyCreatePasswordBtn = document.getElementById('copy-create-password');

copyCreatePasswordBtn.addEventListener('click', function() {
    createPasswordInput.select();
    createPasswordInput.setSelectionRange(0, 99999);

    navigator.clipboard.writeText(createPasswordInput.value).then(() => {
        alert("Password copied to clipboard!");
    }).catch(err => {
        console.error("Failed to copy password: ", err);
    });
});
});





// Delete functionality
document.addEventListener("DOMContentLoaded", function() {

const deleteButton = document.getElementById("delete-button");

    deleteButton.addEventListener("click", function(event) {
        event.preventDefault();

        const form = document.getElementById("UpdateForm");
        const passwordId = form.getAttribute("data-id");
        const appName = document.getElementById("updatemodal").getAttribute("data-appname");

        if (confirm(`Are you sure you want to delete ${appName}?`)) {
            fetch(`/passwords/${passwordId}/delete/`, {
                method: "DELETE",
                headers: {
                    "X-CSRFToken": "{{ csrf_token }}",
                    "Content-Type": "application/json"
                },
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = "/passwords/";
                } else {
                    alert("Failed to delete the password.");
                }
            })
            .catch(err => {
                console.error("Error:", err);
            });
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
const createModal = document.querySelector('#createmodal');
const openCreateModal = document.querySelector('.open-button'); 
const closeCreateModal = document.querySelector('.close-create-button');

// Add event listener for opening the modal
openCreateModal.addEventListener('click', function () {
createModal.showModal();
document.body.classList.add('modal-active'); // Add blur effect
});

// Add event listener for closing the modal
closeCreateModal.addEventListener('click', function () {
createModal.close();
document.body.classList.remove('modal-active'); // Remove blur effect
});
});

        


{% endblock %}  