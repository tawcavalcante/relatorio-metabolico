document.addEventListener("DOMContentLoaded", () => {
    const tabLogin = document.getElementById("tab-login");
    const tabRegister = document.getElementById("tab-register");
    const formLogin = document.getElementById("form-login");
    const formRegister = document.getElementById("form-register");

    tabLogin.addEventListener("click", () => {
        tabLogin.classList.add("active");
        tabRegister.classList.remove("active");
        formLogin.classList.add("active");
        formRegister.classList.remove("active");
    });

    tabRegister.addEventListener("click", () => {
        tabRegister.classList.add("active");
        tabLogin.classList.remove("active");
        formRegister.classList.add("active");
        formLogin.classList.remove("active");
    });

    document.querySelectorAll(".toggle-pass").forEach((btn) => {
        btn.addEventListener("click", () => {
            const input = document.getElementById(btn.dataset.target);
            if (input.type === "password") {
                input.type = "text";
                btn.textContent = "Ocultar";
            } else {
                input.type = "password";
                btn.textContent = "Mostrar";
            }
        });
    });
});