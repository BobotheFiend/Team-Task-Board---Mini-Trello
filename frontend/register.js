const registerForm = document.getElementById("register-form");
const registerMessage = document.getElementById("register-message");

registerForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;

    const selectedRole = document.querySelector(
        'input[name="role"]:checked'
    );

    if (password !== confirmPassword) {
        registerMessage.textContent = "Passwords do not match.";
        return;
    }

    if (selectedRole === null) {
        registerMessage.textContent = "Please select a role.";
        return;
    }

    const role = selectedRole.value;

    const userData = {
        name: name,
        email: email,
        password: password,
        role: role
    };

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/register",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(userData)
            }
        );

        const data = await response.json();

        if (!response.ok) {
            registerMessage.textContent = data.detail;
            return;
        }

        registerMessage.textContent = "Account created successfully!";

        registerForm.reset();

    } catch (error) {

        registerMessage.textContent =
            "Could not connect to the server.";

        console.log(error);
    }
});