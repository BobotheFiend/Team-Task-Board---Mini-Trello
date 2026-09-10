const currentUser = JSON.parse(
    localStorage.getItem("currentUser")
);

if (currentUser === null) {

    window.location.href = "index.html";

}

if (currentUser.role !== "Lead") {

    window.location.href = "team_member_dashboard.html";

}

document.getElementById("user-name").textContent =
    currentUser.name;

document.getElementById("welcome-name").textContent =
    currentUser.name;

document.getElementById("user-avatar").textContent =
    currentUser.name.charAt(0).toUpperCase();

document.getElementById("create-task-button")
    .addEventListener("click", function () {

        alert("Create Task functionality will be added here.");

    });

document.getElementById("create-todo-button")
    .addEventListener("click", function () {

        alert("Create Todo functionality will be added here.");

    });

const approveButtons = document.querySelectorAll(
    ".approve-button"
);

approveButtons.forEach(function (button) {

    button.addEventListener("click", function () {

        alert("Approve functionality will be connected to the backend.");

    });

});

const rejectButtons = document.querySelectorAll(
    ".reject-button"
);

rejectButtons.forEach(function (button) {

    button.addEventListener("click", function () {

        alert("Reject functionality will be connected to the backend.");

    });

});


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


            if (!response.ok) {

                console.log("Logout failed.");
                return;

            }


            localStorage.removeItem("currentUser");

            window.location.href = "index.html";


        } catch (error) {

            console.log(error);

        }

    });