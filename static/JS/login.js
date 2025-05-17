document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const response = await fetch('/login', {
        method: 'POST',
        body: formData
    });

    const contentType = response.headers.get("content-type");

    if (contentType && contentType.includes("application/json")) {
        const data = await response.json();

        if (data.status === "success") {
            localStorage.setItem("user_id", data.id);
            localStorage.setItem("username", data.name);
            localStorage.setItem("role", data.role);

            if (data.role === "shelter") {
                window.location.href = "/dashboard";
            } else {
                window.location.href = "/";
            }
        } else {
            alert("Login failed");
        }
    } else {
        const text = await response.text();
        console.error("Unexpected response:", text);
        alert("Unexpected server error");
    }
});
