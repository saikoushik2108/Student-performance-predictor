function predict() {
    const data = {
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
    .then(data => {
        document.getElementById("result").innerHTML =
            `✅ Pass: ${data.pass} <br> ❌ Fail: ${data.fail}`;
    });
}