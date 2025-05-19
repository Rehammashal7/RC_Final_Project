
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");

  const alertBox = document.getElementById("customAlert");
  const alertMessage = document.getElementById("alertMessage");
  const closeBtn = document.getElementById("alertCloseBtn");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    const response = await fetch("/login", {
      method: "POST",
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
        // Show styled alert box
        alertMessage.textContent = "Email or password is incorrect.";
        alertBox.style.display = "flex";
      }
    } else {
      const text = await response.text();
      console.error("Unexpected response:", text);
      alertMessage.textContent = "Unexpected server error.";
      alertBox.style.display = "flex";
    }
  });

  // Close alert box on button click
  closeBtn.addEventListener("click", function () {
    alertBox.style.display = "none";
  });
});

