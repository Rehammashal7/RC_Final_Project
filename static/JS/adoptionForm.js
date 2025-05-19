const urlParams = new URLSearchParams(window.location.search);
  const petId = urlParams.get("id");
  if (petId) {
    document.getElementById("pet_id_input").value = petId;
  }

  fetch("/get-session-user")
    .then(res => res.json())
    .then(data => {
      if (data.user_id) {
        document.getElementById("user_id_input").value = data.user_id;
      }
    });



document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("adoptionForm");
  const customAlert = document.getElementById("customAlert");
  const alertMessage = document.getElementById("alertMessage");
  const alertCloseBtn = document.getElementById("alertCloseBtn");

  // Match background color of page
  alertCloseBtn.style.backgroundColor = getComputedStyle(document.body).backgroundColor;

  function showCustomAlert(message, redirectUrl = null) {
  alertMessage.textContent = message;
  customAlert.style.display = "flex";

  alertCloseBtn.onclick = () => {
    customAlert.style.display = "none";
    if (redirectUrl) {
      window.location.href = redirectUrl;
    }
  };
}
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(form);

  try {
    const response = await fetch("/submit-adoption", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.status === "success") {
      showCustomAlert(data.message, "/");
    } else if (data.message === "You must be logged in to submit an adoption request.") {
      showCustomAlert(data.message, "/login");
    } else {
      showCustomAlert(data.message, "/"); // No redirect
    }

  } catch (error) {
    console.error("Error submitting form:", error);
    showCustomAlert("An unexpected error occurred.");
  } 
  });
});
