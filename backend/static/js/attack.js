document.getElementById("runAttack").addEventListener("click", async () => {
    const attackType = document.getElementById("attackType").value;
    const target = document.getElementById("target").value;

    const response = await fetch("http://127.0.0.1:5000/api/run_attack", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ attack_type: attackType, target: target })
    });

    const result = await response.json();
    document.getElementById("attackOutput").innerText = result.output || result.error;
});
