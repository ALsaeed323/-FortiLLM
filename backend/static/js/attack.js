document.addEventListener("DOMContentLoaded", () => {
    const runAttackButton = document.getElementById("runAttack");

    if (runAttackButton) {
        runAttackButton.addEventListener("click", async () => {
            const attackTypeElement = document.querySelector('select[name="application"]');
            const targetElement = document.querySelector('select[name="intention"]');
            const outputElement = document.getElementById("attackOutput");

            const attackType = attackTypeElement ? attackTypeElement.value : "default_attack";
            const target = targetElement ? targetElement.value : "default_target";

            console.log("Selected Application:", attackType);  // Debugging
            console.log("Selected Intention:", target);        // Debugging

            try {
                const response = await fetch("http://127.0.0.1:5000/api/run_attack", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ attack_type: attackType, target: target })
                });

                const result = await response.json();

                if (outputElement) {
                    outputElement.innerText = result.output || result.error || "No response from server.";
                } else {
                    alert(result.output || result.error || "No response from server.");
                }
            } catch (error) {
                console.error("Error running security test:", error);
                if (outputElement) {
                    outputElement.innerText = "An error occurred while running the security test.";
                } else {
                    alert("An error occurred while running the security test.");
                }
            }
        });
    } else {
        console.error("Run Attack button not found!");
    }
});