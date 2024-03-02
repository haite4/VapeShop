const navbarBottom = document.querySelector(".navbar-bottom");

function handleScroll() {
  if (window.scrollY > 800) {
    navbarBottom.classList.add("fixed-top");
  } else {
    navbarBottom.classList.remove("fixed-top");
  }
}

window.addEventListener("scroll", handleScroll);

// Вызовем handleScroll() сразу после загрузки страницы
handleScroll();