window.onload = async () => {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/get_results");
        const data = await response.json();

        let tableContent = "";
        data.forEach(attack => {
            tableContent += `
                <tr>
                    <td>${attack.attack_type}</td>
                    <td>${attack.target}</td>
                    <td>${attack.output}</td>
                    <td>${attack.error}</td>
                </tr>
            `;
        });

        document.getElementById("attackHistory").innerHTML = tableContent;
    } catch (err) {
        console.error("Error fetching attack history:", err);
    }
};
