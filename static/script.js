//create pop-up form in studentGrades
const openModalBtns = document.querySelectorAll(".open-modal-btn");
const closeModalBtns = document.querySelectorAll(".close-modal-btn");

openModalBtns.forEach((btn, index) => {
    btn.addEventListener("click", () => {
        const overlay = document.querySelector(`#overlay${index + 1}`);
        overlay.style.display = "block";
    });
});

closeModalBtns.forEach((btn, index) => {
    btn.addEventListener("click", () => {
        const overlay = document.querySelector(`#overlay${index + 1}`);
        overlay.style.display = "none";
    });
});

const submitBtns = document.querySelectorAll(".submit-btn");

submitBtns.forEach((btn, index) => {
    btn.addEventListener("click", () => {
        submitBtns.disabled = true;
    });
});
