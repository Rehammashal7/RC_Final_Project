let currentFilter = null;

function filterPets(species) {
  const allCards = document.querySelectorAll(".card");

  // If the same category is clicked again, reset filter
  if (currentFilter === species) {
    currentFilter = null;

    allCards.forEach(card => {
      card.style.display = "block";
    });

    // Remove highlight
    document.querySelectorAll('.animal-card').forEach(card => {
      card.classList.remove("selected");
    });

    return;
  }

  currentFilter = species;

  allCards.forEach(card => {
    if (card.dataset.species === species) {
      card.style.display = "block";
    } else {
      card.style.display = "none";
    }
  });

  // Highlight the selected card
  document.querySelectorAll('.animal-card').forEach(card => {
    card.classList.remove("selected");
  });

  const targetCard = document.querySelector(`.animal-card.${species.toLowerCase()}-card`);
  if (targetCard) targetCard.classList.add("selected");
}

document.addEventListener("DOMContentLoaded", () => {
      const userId = localStorage.getItem("user_id");
      const username = localStorage.getItem("username");
console.log(localStorage.getItem("username"))
      const navbar = document.getElementById("navbarLinks");
      const welcome = document.getElementById("welcomeMessage");

      if (userId && username) {
        // Logged in: show logout and welcome message
        navbar.innerHTML = `<a href="#" id="logoutBtn">Logout</a>`;
        welcome.textContent = `Welcome, ${username}`;

       // welcome.style.display = "block";

        // Logout logic
        document.getElementById("logoutBtn").addEventListener("click", () => {
          localStorage.clear();
          window.location.href = "/";
        });
      } else {
        // Not logged in
        navbar.innerHTML = `
          <a href="/login">Login</a>
          <a href="/signup">Sign Up</a>
        `;
        welcome.style.display = "none";
      }
    });