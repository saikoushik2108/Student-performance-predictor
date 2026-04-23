let timeLeft = 30;
let timerInterval;

function startTimer() {
    timerInterval = setInterval(() => {
        timeLeft--;
        document.getElementById("timer").innerText = timeLeft;

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            alert("Time's up!");
            predict();
        }
    }, 1000);
}

window.onload = startTimer;

function calculateIQ() {
    let correct = 0;

    for (let i = 1; i <= 5; i++) {
        let selected = document.querySelector(`input[name="q${i}"]:checked`);
        if (selected) {
            correct += parseInt(selected.value);
        }
    }

    let timeBonus = Math.max(0, timeLeft / 30);
    let finalScore = correct + timeBonus;

    return {
        correct: correct,
        timeTaken: 30 - timeLeft,
        score: finalScore
    };
}

function getIQLevel(score) {
    if (score <= 2) return 0;
    else if (score <= 4) return 1;
    else return 2;
}

function predict() {
    clearInterval(timerInterval);

    const iqData = calculateIQ();
    const iqLevel = getIQLevel(iqData.score);

    const data = {
        iq: iqLevel,
        study: document.getElementById("study").value,
        attendance: document.getElementById("attendance").value,
        sleep: document.getElementById("sleep").value,
        motivation: document.getElementById("motivation").value,
        grades: document.getElementById("grades").value
    };

    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result => {
        document.getElementById("result").innerHTML = `
            🧠 IQ Score: ${iqData.score.toFixed(2)} <br>
            ✅ Correct: ${iqData.correct}/5 <br>
            ⏱️ Time Taken: ${iqData.timeTaken}s <br><br>
            🎯 Pass: ${result.pass} <br>
            ❌ Fail: ${result.fail}
        `;
    });
}