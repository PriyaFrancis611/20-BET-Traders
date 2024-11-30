// Burger Items
const iconMenu = document.querySelector(".menu-icon");
const menuBody = document.querySelector(".menu-body");

export default function closeBurgerModal() {
  const iconMenu = document.querySelector(".menu-icon");
  const menuBody = document.querySelector(".menu-body");
  document.body.classList.remove("lock");
  iconMenu.classList.remove("activem");
  menuBody.classList.remove("activem");
}

// Header nav

const goTopBtn = document.querySelector(".go-to-top-button");

// Header Scrolling Position
let scrollOff = window.pageYOffset;
let headerNav = document.querySelector(".header-nav");

// Scroll blocks & buttons

const managersBlock = document.querySelector(".managers-block");
const contactButtons = document.querySelectorAll(".contact-button");

const termsBlock = document.querySelector(".coop-terms-block");
const termsButtons = document.querySelectorAll(".terms-button");

// Burger logic toggler
if (iconMenu) {
  iconMenu.addEventListener("click", (e) => {
    document.body.classList.toggle("lock");
    iconMenu.classList.toggle("activem");
    menuBody.classList.toggle("activem");
  });
}

function removeAnchor() {
  if (window.location.hash) {
    history.replaceState(
      null,
      null,
      window.location.pathname + window.location.search
    );
  }
}

// Scroll to block handler
window.addEventListener("load", () => {
  if (window.location.hash === "#contacts") {
    removeAnchor();
    closeBurgerModal();
    managersBlock.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  if (window.location.hash === "#terms") {
    removeAnchor();
    closeBurgerModal();
    termsBlock.scrollIntoView({ behavior: "smooth", block: "start" });
  }
});

if (contactButtons) {
  contactButtons.forEach((e) => {
    e.addEventListener("click", (e) => {
      e.preventDefault();
      managersBlock.scrollIntoView({ behavior: "smooth", block: "start" });
      removeAnchor();
      closeBurgerModal();
    });
  });
}
if (termsButtons) {
  termsButtons.forEach((e) => {
    e.addEventListener("click", (e) => {
      e.preventDefault();
      termsBlock.scrollIntoView({ behavior: "smooth", block: "start" });
      removeAnchor();
      closeBurgerModal();
    });
  });
}

if (goTopBtn) {
  goTopBtn.addEventListener("click", (e) => {
    e.preventDefault();
    document
      .querySelector(".wrapper")
      .scrollIntoView({ behavior: "smooth", block: "start" });
  });
}
let isScrolling = false;

function throttle(func, delay) {
  let timeoutId;

  return function () {
    if (!timeoutId) {
      timeoutId = setTimeout(() => {
        func();
        timeoutId = null;
      }, delay);
    }
  };
}

function handleScroll() {
  if (window.scrollY > 500 && !isScrolling) {
    goTopBtn.classList.add("visible-go-button");
    isScrolling = true;
  } else if (window.scrollY <= 500 && isScrolling) {
    goTopBtn.classList.remove("visible-go-button");
    isScrolling = false;
  }
}

window.addEventListener("scroll", throttle(handleScroll, 500));

const aboutProductButton = document.querySelector(".about-product");
const styleContactButton = document.querySelector(".style-contact-button");
const styleTermsButton = document.querySelector(".style-terms-button");

const termsObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      aboutProductButton.classList.remove("active-item");
      styleContactButton.classList.remove("active-item");
      styleTermsButton.classList.add("active-item");
    } else {
      styleTermsButton.classList.remove("active-item");
      aboutProductButton.classList.add("active-item");
    }
  });
});

const contactsObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      aboutProductButton.classList.remove("active-item");
      styleTermsButton.classList.remove("active-item");
      styleContactButton.classList.add("active-item");
    } else {
      styleContactButton.classList.remove("active-item");
      aboutProductButton.classList.add("active-item");
    }
  });
});

if (document.querySelector(".coop-terms-block")) {
  termsObserver.observe(document.querySelector(".coop-terms-block"));
}

if (managersBlock) {
  contactsObserver.observe(managersBlock);
}