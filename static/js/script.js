// Flash message close functionality
document.addEventListener("DOMContentLoaded", function () {
  const closeButtons = document.querySelectorAll(".flash-close");
  closeButtons.forEach(button => {
    button.addEventListener("click", function () {
      this.parentElement.style.display = "none";
    });
  });

  // Filter Portfolio (optional enhancement)
  const filterButtons = document.querySelectorAll(".filter-btn");
  const portfolioItems = document.querySelectorAll(".portfolio-item");

  filterButtons.forEach(btn => {
    btn.addEventListener("click", function () {
      filterButtons.forEach(b => b.classList.remove("active"));
      this.classList.add("active");

      const category = this.getAttribute("data-filter");
      portfolioItems.forEach(item => {
        if (category === "all" || item.getAttribute("data-category") === category) {
          item.style.display = "block";
        } else {
          item.style.display = "none";
        }
      });
    });
  });
});
