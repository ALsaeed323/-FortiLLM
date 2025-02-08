// ✅ Handle Sign-In 
const signInForm = document.querySelector(".sign-in-container form");
if (signInForm) {
    signInForm.addEventListener("submit", async (e) => {
        e.preventDefault();  // Prevents page reload on form submission

        const email = signInForm.querySelector('input[name="email"]').value;
        const password = signInForm.querySelector('input[name="password"]').value;

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
const signUpForm = document.querySelector(".sign-up-container form");
if (signUpForm) {
    signUpForm.addEventListener("submit", async (e) => {
        e.preventDefault();  // Prevents page reload on form submission

        const name = signUpForm.querySelector('input[name="name"]').value;
        const email = signUpForm.querySelector('input[name="email"]').value;
        const password = signUpForm.querySelector('input[name="password"]').value;

        // You can add additional validations here if needed

        try {
            const response = await fetch("http://127.0.0.1:5000/api/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    name,
                    email,
                    password
                })
            });

            const result = await response.json();

            if (response.ok) {
                alert("Registration successful! Redirecting to Sign In...");
                window.location.href = "#";
            } else {
                alert(result.error || "Sign-up failed! Please try again.");
            }
        } catch (err) {
            console.error("Sign-up error:", err);
        }
    });
}
