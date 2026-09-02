const loginForm = document.getElementById("login-form");
const loginMessage = document.getElementById("login-message");

loginForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    loginMessage.textContent = "";

    const loginData = {
        email: email,
        password: password
    };

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/login",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(loginData)
            }
        );

        const data = await response.json();

        if (!response.ok) {

            if (Array.isArray(data.detail)) {

                const errors = data.detail.map(function (error) {

                    const field = error.loc[error.loc.length - 1];

                    return `${field}: ${error.msg}`;

                });

                loginMessage.textContent = errors.join(" | ");

            } else {

                loginMessage.textContent = data.detail;
            }

            return;
        }

        localStorage.setItem(
            "currentUser",
            JSON.stringify(data)
        );

        loginMessage.textContent = "Login successful!";

        window.location.href = "dashboard.html";

    } catch (error) {

        loginMessage.textContent =
            "Could not connect to the server.";

        console.log(error);
    }
});

