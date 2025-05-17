document.addEventListener("DOMContentLoaded", function () {
  const userId = localStorage.getItem("user_id");
  const username = localStorage.getItem("username");
  const role = localStorage.getItem("role");

  if (!userId) {
    window.location.href = "/login";
  }

  // Optionally show user info
  console.log("Logged in as:", username, "Role:", role);
});
