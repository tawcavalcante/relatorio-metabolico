document.addEventListener("DOMContentLoaded", () => {
    const genderInput = document.getElementById("gender");
    const genderBtns = document.querySelectorAll(".gender-btn");
    const btnCalcular = document.getElementById("btn-calcular");

    genderBtns.forEach((btn) => {
        btn.addEventListener("click", () => {
            genderBtns.forEach((b) => b.classList.remove("active"));
            btn.classList.add("active");
            genderInput.value = btn.dataset.gender;
        });
    });

    if (btnCalcular) {
        btnCalcular.addEventListener("click", () => {
            const sexo = genderInput.value;
            const idade = parseFloat(document.getElementById("age").value) || 20;
            const peso = parseFloat(document.getElementById("weight").value) || 75;
            const altura = parseFloat(document.getElementById("height").value) || 172;
            const atividade = parseFloat(document.getElementById("activity").value) || 1.55;
            const protRatio = parseFloat(document.getElementById("prot_ratio").value) || 2.0;
            const fatRatio = parseFloat(document.getElementById("fat_ratio").value) || 1.0;

            const base = 10 * peso + 6.25 * altura - 5 * idade;
            const tmb = Math.round(sexo === "male" ? base + 5 : base - 161);
            const tdee = Math.round(tmb * atividade);
            const agua = ((peso * 40) / 1000).toFixed(1);

            document.getElementById("tmb-value").textContent = tmb;
            document.getElementById("tdee-value").textContent = tdee;
            document.getElementById("water-value").textContent = agua;

            const protG = Math.round(peso * protRatio);
            const gordG = Math.round(peso * fatRatio);

            const estrategias = [
                { nome: "Perder 500g/sem", delta: -500 },
                { nome: "Perder 250g/sem", delta: -250 },
                { nome: "Manter o Peso", delta: 0 },
                { nome: "Ganhar 250g/sem", delta: 250 },
                { nome: "Ganhar 500g/sem", delta: 500 },
            ];

            const tbody = document.getElementById("strategies-body");
            tbody.innerHTML = estrategias
                .map((est) => {
                    const kcal = tdee + est.delta;
                    const carb = Math.max(0, Math.round((kcal - (protG * 4 + gordG * 9)) / 4));
                    return `
                        <tr>
                            <td>${est.nome}</td>
                            <td>${kcal} kcal</td>
                            <td>${carb}g</td>
                            <td>${protG}g</td>
                            <td>${gordG}g</td>
                        </tr>
                    `;
                })
                .join("");
        });
    }
});