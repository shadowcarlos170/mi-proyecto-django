document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");

    form.addEventListener("submit", (e) => {
        const username = form.username.value.trim();
        const password = form.password.value.trim();

        if (!username || !password) {
            e.preventDefault();
            alert("Por favor completa todos los campos.");
        }
    });

    const button = form.querySelector("button");
    button.addEventListener("mousedown", () => {
        button.style.transform = "scale(0.97)";
    });
    button.addEventListener("mouseup", () => {
        button.style.transform = "scale(1)";
    });
});
