function toggleMenuIcon(element) {
    element.classList.toggle("open");
    const navbarNav = document.getElementById("navbarNav");
    if (navbarNav.style.display === "block") {
      navbarNav.style.display = "none";
    } else {
      navbarNav.style.display = "block";
    }
  }
  function toggleMenuIcon() {
    var nav = document.querySelector(".navbar-nav");
    nav.classList.toggle("show");
  }
  // Initialization for ES Users
  import { Carousel, initMDB } from "mdb-ui-kit";

  initMDB({ Carousel });