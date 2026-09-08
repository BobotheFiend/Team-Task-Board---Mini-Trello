const currentUser = JSON.parse(
    localStorage.getItem("currentUser")
);


if (currentUser === null) {

    window.location.href = "index.html";

}


if (currentUser.role !== "Member") {

    window.location.href = "team_lead_dashboard.html";

}


/* Display user information */

document.getElementById("user-name").textContent =
    currentUser.name;

document.getElementById("welcome-name").textContent =
    currentUser.name;


/* Create avatar from first letter */

document.getElementById("user-avatar").textContent =
    currentUser.name.charAt(0).toUpperCase();


/* Logout */

document.getElementById("logout-button")
    .addEventListener("click", async function (event) {

        event.preventDefault();

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/logout",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        email: currentUser.email
                    })
                }
            );

            if (response.ok) {

                localStorage.removeItem("currentUser");

                window.location.href = "index.html";

            }

        } catch (error) {

            console.log(error);

        }

    });