// ✅ Handle Sign-In
const signinForm = document.getElementById("signinForm");
if (signinForm) {
    signinForm.addEventListener("submit", async (e) => {
        e.preventDefault();  // Prevents page reload on form submission

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch("http://127.0.0.1:5000/api/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            const result = await response.json();

            if (response.ok) {
                // Save token to localStorage
                localStorage.setItem("token", result.token);

                // Redirect user to dashboard
                window.location.href = "dashboard.html";
            } else {
                alert(result.error || "Login failed! Please try again.");
            }
        } catch (err) {
            console.error("Login error:", err);
        }
    });
}

// ✅ Handle Sign-Up
const signupForm = document.getElementById("signupForm");
if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
        e.preventDefault();  // Prevents page reload on form submission

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;
        const termsAccepted = document.getElementById("terms").checked;

        // Check if passwords match
        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }

        // Ensure terms are accepted
        if (!termsAccepted) {
            alert("You must agree to the Terms & Conditions.");
            return;
        }

        // Get selected LLMs
        const llmChoices = [];
        document.querySelectorAll("input[name='llm']:checked").forEach((checkbox) => {
            llmChoices.push(checkbox.value);
        });

        try {
            const response = await fetch("http://127.0.0.1:5000/api/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    email,
                    password,
                    llm_choices: llmChoices
                })
            });

            const result = await response.json();

            if (response.ok) {
                alert("Registration successful! Redirecting to Sign In...");
                window.location.href = "signin.html";
            } else {
                alert(result.error || "Sign-up failed! Please try again.");
            }
        } catch (err) {
            console.error("Sign-up error:", err);
        }
    });
}
