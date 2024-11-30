import en from "./translations_en.js";
import ru from "./translations_ru.js";

import closeBurgerModal from "./main.js";

// Language buttons
let currentLang = document.querySelectorAll(".cur-lang");
const languages = document.querySelectorAll(".language");

// Language handling
function applyTranslations(lang) {
  let elements = document.querySelectorAll("[data-translate]");
  elements.forEach(function (element) {
    let key = element.getAttribute("data-translate");
    element.innerHTML = lang[key] || key;
  });
}

if (currentLang) {
  currentLang.forEach((e) => {
    e.addEventListener("click", (e) => {
      e.preventDefault();
    });
  });
}

// Images translate handler
const partnersIcon1 = document.querySelector(".bottom-partners-icon1");
const partnersIcon3 = document.querySelector(".bottom-partners-icon3");

function imgTranslate(lang) {
  if (lang === "EN" && partnersIcon1 && partnersIcon3) {
    partnersIcon1.src = "./assets/images/bottom-partners-icon1-eng.png";
    partnersIcon3.src = "./assets/images/bottom-partners-icon3-eng.png";
  } else {
    partnersIcon1.src = "./assets/images/bottom-partners-icon1.webp";
    partnersIcon3.src = "./assets/images/bottom-partners-icon3.webp";
  }
}

if (languages) {
  languages.forEach((l) => {
    l.addEventListener("click", (e) => {
      e.preventDefault();
      currentLang.forEach((lang) => {
        lang.innerHTML = l.innerHTML;
      });
      closeBurgerModal();
      if (partnersIcon1 && partnersIcon3) {
        imgTranslate(l.innerHTML);
      }
      if (l.innerHTML === "RU") {
        applyTranslations(ru);
        localStorage.setItem("lang", "ru");
      }
      if (l.innerHTML === "EN") {
        applyTranslations(en);
        localStorage.setItem("lang", "en");
      }
    });
  });
}
let language = window.navigator.userLanguage || window.navigator.language;

const equalToRuLanguages = [
  "ru",
  "hy",
  "az",
  "be",
  "ka",
  "ky",
  "kk",
  "tg",
  "tk",
  "uk",
  "uz",
];

const startsWithEqualToRuLanguages = equalToRuLanguages.some((lang) =>
  language.startsWith(lang)
);

window.addEventListener("DOMContentLoaded", () => {
  if (localStorage.getItem("lang") !== null) {
    if (localStorage.getItem("lang") === "ru") {
      applyTranslations(ru);
      currentLang.forEach((lang) => {
        lang.innerHTML = "RU";
      });
      if (partnersIcon1 && partnersIcon3) {
        imgTranslate("RU");
      }
    }
    if (localStorage.getItem("lang") === "en") {
      applyTranslations(en);
      currentLang.forEach((lang) => {
        lang.innerHTML = "EN";
      });
      if (partnersIcon1 && partnersIcon3) {
        imgTranslate("EN");
      }
    }
  } else {
    if (startsWithEqualToRuLanguages) {
      applyTranslations(ru);
      currentLang.forEach((lang) => {
        lang.innerHTML = "RU";
      });
      if (partnersIcon1 && partnersIcon3) {
        imgTranslate("RU");
      }
    } else {
      applyTranslations(en);
      currentLang.forEach((lang) => {
        lang.innerHTML = "EN";
      });
      if (partnersIcon1 && partnersIcon3) {
        imgTranslate("EN");
      }
    }
  }
});