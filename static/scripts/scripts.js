//  Menu Icon Function


const icon = document.querySelector(".menu-icon");
const nav_mobile = document.getElementById('nav-mobile');

icon.addEventListener("click", () => {
  icon.classList.toggle("clicked");
  nav_mobile.classList.toggle("show");
});


// ----------------------------------------------------------------------------
