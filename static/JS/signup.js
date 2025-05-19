document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("signupForm");
  const passwordInput = document.getElementById("signupPassword");
  const emailInput = document.getElementById("signupEmail");
  const emailError = document.getElementById("emailError");

  const alertBox = document.getElementById("customAlert");
  const alertMessage = document.getElementById("alertMessage");
  const closeBtn = document.getElementById("alertCloseBtn");

  // Handle password length alert
  form.addEventListener("submit", function (event) {
    if (passwordInput.value.length < 8) {
      event.preventDefault();
      alertMessage.textContent = "Password must be at least 8 characters long.";
      alertBox.style.display = "flex";
    }
  });

  closeBtn.addEventListener("click", function () {
    alertBox.style.display = "none";
  });

  // Handle email error
  const params = new URLSearchParams(window.location.search);
  const error = params.get("error");
  const emailValue = params.get("email");

  if (error === "email_exists") {
    emailInput.classList.add("input-error-border");
    emailError.textContent = "This email is already registered.";
    if (emailValue) {
      emailInput.value = emailValue;
    }
  }

  // Clear error when user starts typing
  emailInput.addEventListener("input", () => {
    emailInput.classList.remove("input-error-border");
    emailError.textContent = "";
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("signupForm");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(form);

    const response = await fetch("/signup", {
      method: "POST",
      body: formData,
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
        alert("Signup failed");
      }
    } else {
      const text = await response.text();
      console.error("Unexpected response:", text);
      alert("Unexpected server error");
    }
  });
});
 document.getElementById("signupName").addEventListener("keypress", function (e) {
    const char = String.fromCharCode(e.which);
    if (!/^[a-zA-Z\s]*$/.test(char)) {
      e.preventDefault();
    }
  });