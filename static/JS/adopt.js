 function showCustomAlert(message, redirectUrl = null) {
      const alertBox = document.getElementById("customAlert");
      const alertMessage = document.getElementById("alertMessage");
      const alertCloseBtn = document.getElementById("alertCloseBtn");

      alertMessage.textContent = message;
      alertBox.style.display = "flex";

      alertCloseBtn.onclick = () => {
        alertBox.style.display = "none";
        if (redirectUrl) {
          window.location.href = redirectUrl;
        }
      };
    }

    async function submitAdoptionRequest() {
      const petId = document.getElementById("pet_id_input").value;

      const sessionRes = await fetch("/get-session-user");
      const sessionData = await sessionRes.json();
      const userId = sessionData.user_id;
      const email=sessionData.email;
      if (!userId) {
        showCustomAlert("You must be logged in to adopt a pet.", "/login");
        return;
      }

      const formData = new FormData();
      formData.append("user_id", userId);
      formData.append("pet_id", petId);
      formData.append("email", email); 
      

      try {
        const response = await fetch("/submit-adoption", {
          method: "POST",
          body: formData
        });

        const data = await response.json();

        if (data.status === "success") {
          showCustomAlert(data.message, "/");
        } else {
          showCustomAlert(data.message);
        }

      } catch (error) {
        console.error("Error:", error);
        showCustomAlert("Something went wrong. Please try again.");
      }
    }