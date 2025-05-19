document.addEventListener("DOMContentLoaded", () => {
  const aboutField = document.getElementById("about");

  // Create warning element
  const warning = document.createElement("div");
  warning.className = "warning";
  warning.textContent = "Maximum 100 characters allowed.";
  aboutField.parentNode.insertBefore(warning, aboutField.nextSibling);

  aboutField.addEventListener("input", () => {
    const maxChars = 100;
    const currentText = aboutField.value;

    if (currentText.length > maxChars) {
      aboutField.value = currentText.slice(0, maxChars);
      warning.style.display = "block";
    } else {
      warning.style.display = "none";
    }
  });
});