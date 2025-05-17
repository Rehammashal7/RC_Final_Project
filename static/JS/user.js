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
