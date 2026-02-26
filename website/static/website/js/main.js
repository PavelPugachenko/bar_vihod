const galleryButtons = document.querySelectorAll(".gallery-item");
const modal = document.getElementById("photoModal");
const modalImage = document.getElementById("modalImage");
const modalClose = document.getElementById("modalClose");
const revealElements = document.querySelectorAll(".reveal");
const yearEl = document.getElementById("year");

if (yearEl) {
  yearEl.textContent = new Date().getFullYear();
}

function openModal(src, alt) {
  if (!modal || !modalImage) {
    return;
  }

  modalImage.src = src;
  modalImage.alt = alt || "Фото бара";
  modal.classList.add("is-open");
  modal.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
}

function closeModal() {
  if (!modal || !modalImage) {
    return;
  }

  modal.classList.remove("is-open");
  modal.setAttribute("aria-hidden", "true");
  modalImage.src = "";
  document.body.style.overflow = "";
}

galleryButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const img = button.querySelector("img");
    if (!img) {
      return;
    }
    const fullSrc = button.dataset.full || img.src;
    openModal(fullSrc, img.alt);
  });
});

if (modalClose) {
  modalClose.addEventListener("click", closeModal);
}

if (modal) {
  modal.addEventListener("click", (event) => {
    if (event.target === modal) {
      closeModal();
    }
  });
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && modal && modal.classList.contains("is-open")) {
    closeModal();
  }
});

const revealObserver = new IntersectionObserver(
  (entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12 }
);

revealElements.forEach((element) => revealObserver.observe(element));
