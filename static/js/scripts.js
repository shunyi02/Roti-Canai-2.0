function showSignUp() {
    document.getElementById('loginForm').classList.remove('active');
    document.getElementById('signUpForm').classList.add('active');
}

function showLogin() {
    document.getElementById('signUpForm').classList.remove('active');
    document.getElementById('loginForm').classList.add('active');
}

// Show login form by default
document.getElementById('loginForm').classList.add('active');

function toggleDropdown(event) {
    event.preventDefault();
    const dropdownContent = event.target.nextElementSibling;
    if (dropdownContent.style.display === "block") {
        dropdownContent.style.display = "none";
    } else {
        dropdownContent.style.display = "block";
    }
}

