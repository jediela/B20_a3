// Get references to the buttons and overlay
const showModalBtn = document.getElementById("show-modal-btn");
const closeModalBtn = document.getElementById("close-modal-btn");
const overlay = document.getElementById("overlay");

// Function to show the modal window
function showModal() {
    overlay.style.display = "block";
}

// Function to hide the modal window
function hideModal() {
    overlay.style.display = "none";
}

// Event listener for the "Show Modal" button
showModalBtn.addEventListener("click", showModal);

// Event listener for the "Close Modal" button
closeModalBtn.addEventListener("click", hideModal);
