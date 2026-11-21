// Limites Científicos
const limits = {
    protein: { min: 1.2, max: 3.0, optimalMin: 1.6, optimalMax: 2.2 },
    fat: { min: 0.5, max: 1.5, optimalMin: 0.7, optimalMax: 1.2 }
};

function validateMacros(protRatio, fatRatio) {
    const protWarning = document.getElementById('prot-warning');
    const fatWarning = document.getElementById('fat-warning');
    let isValid = true;

    // Validação de Proteína
    if (protRatio > limits.protein.max) {
        protWarning.textContent = "Acima do limite científico.";
        protWarning.className = "warning-msg warning-red";
        isValid = false;
    } else if (protRatio < limits.protein.min) {
        protWarning.textContent = "Abaixo do necessário.";
        protWarning.className = "warning-msg warning-red";
        isValid = false;
    } else if (protRatio >= limits.protein.optimalMin && protRatio <= limits.protein.optimalMax) {
        protWarning.textContent = "Faixa ideal hipertrofia.";
        protWarning.className = "warning-msg warning-green";
    } else {
        protWarning.textContent = "Aceitável, mas fora do ideal.";
        protWarning.className = "warning-msg warning-orange";
    }

    // Validação de Gordura
    if (fatRatio > limits.fat.max) {
        fatWarning.textContent = "Desnecessariamente alto.";
        fatWarning.className = "warning-msg warning-red";
        isValid = false;
    } else if (fatRatio < limits.fat.min) {
        fatWarning.textContent = "Risco hormonal (muito baixo).";
        fatWarning.className = "warning-msg warning-red";
        isValid = false;
    } else if (fatRatio >= limits.fat.optimalMin && fatRatio <= limits.fat.optimalMax) {
        fatWarning.textContent = "Faixa ideal.";
        fatWarning.className = "warning-msg warning-green";
    } else {
        fatWarning.textContent = "Aceitável.";
        fatWarning.className = "warning-msg warning-orange";
    }

    return isValid;
}

document.getElementById('calculate-btn').addEventListener('click', function() {
    const gender = document.querySelector('input[name="gender"]:checked').value;
    const age = parseFloat(document.getElementById('age').value);
    const weight = parseFloat(document.getElementById('weight').value);
    const height = parseFloat(document.getElementById('height').value);
    const activityMulti = parseFloat(document.getElementById('activity').value);
    const protRatio = parseFloat(document.getElementById('protein-ratio').value);
    const fatRatio = parseFloat(document.getElementById('fat-ratio').value);

    if (!age || !weight || !height) return;

    // Checa limites científicos antes de calcular
    const isValid = validateMacros(protRatio, fatRatio);
    if (!isValid) {
        // Se quiser impedir o cálculo ao errar a proporção, descomente a linha abaixo
        // return; 
    }

    // Fórmula Mifflin-St Jeor
    let tmb = (10 * weight) + (6.25 * height) - (5 * age);
    tmb += (gender === 'male') ? 5 : -161;

    const tdee = Math.round(tmb * activityMulti);
    const water = (weight * 0.040).toFixed(1); // Usando 40ml para rotina de treinos

    // Atualiza os Cards
    document.getElementById('tmb-result').innerText = Math.round(tmb);
    document.getElementById('tdee-result').innerText = tdee;
    document.getElementById('water-result').innerText = water;

    // Gramas fixas
    const protGrams = Math.round(weight * protRatio);
    const fatGrams = Math.round(weight * fatRatio);
    const fixedKcal = (protGrams * 4) + (fatGrams * 9);

    // Estratégias (Tabela)
    const scenarios = [
        { name: "Perder 500g/sem", kcal: tdee - 500, class: "" },
        { name: "Perder 250g/sem", kcal: tdee - 250, class: "" },
        { name: "Manter o Peso", kcal: tdee, class: "" },
        { name: "Ganhar 250g/sem", kcal: tdee + 250, class: "" },
        { name: "Ganhar 500g/sem", kcal: tdee + 500, class: "" }
    ];

    const tbody = document.getElementById('table-body');
    tbody.innerHTML = "";

    scenarios.forEach(scenario => {
        const carbKcal = scenario.kcal - fixedKcal;
        const carbGrams = carbKcal > 0 ? Math.round(carbKcal / 4) : 0;

        const tr = document.createElement('tr');
        if (scenario.class) tr.className = scenario.class;
        
        tr.innerHTML = `
            <td>${scenario.name}</td>
            <td>${scenario.kcal} kcal</td>
            <td>${carbGrams}g</td>
            <td>${protGrams}g</td>
            <td>${fatGrams}g</td>
        `;
        tbody.appendChild(tr);

        // Lógica de clique para destacar a linha selecionada
        tr.addEventListener('click', function() {
            const allRows = tbody.querySelectorAll('tr');
            allRows.forEach(row => row.classList.remove('selected-row'));
            this.classList.add('selected-row');
        });
    });
});

window.onload = () => {
    document.getElementById('calculate-btn').click();
};

const protInput = document.getElementById('protein-ratio');
const fatInput = document.getElementById('fat-ratio');

// Escuta a digitação e valida na hora
protInput.addEventListener('input', () => {
    validateMacros(parseFloat(protInput.value), parseFloat(fatInput.value));
});

fatInput.addEventListener('input', () => {
    validateMacros(parseFloat(protInput.value), parseFloat(fatInput.value));
});