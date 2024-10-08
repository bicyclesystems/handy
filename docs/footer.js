const footerTemplate = `
<footer class="padding-xl box-l">
  <div class="gap-s row align-start box-l">
    <div class="gap-l column align-start box" style="display: none;">
      <a href="https://rnbw.design">
        <svg-icon src="https://rnbw.design/images/rnbw.svg"></svg-icon>
      </a>
      <div class="text-s">
        © <span id="year"></span> Rainbow Design, Ltd.
      </div>
    </div>


    <div class="gap-xl row align-start box-l">
      <a style="width: 4vw; height 4vw;" href="https://weareunder.design/">
        <svg-icon src="https://weareunder.design/images/underfooter.svg"></svg-icon>
      </a>
      <p class="box">
        under creates high-quality,<br>
        well-designed, creative brands <br>
        and products for creative people.
      </p>
      <div class="column gap-xs">
        <a href="https://weareunder.design/blog/">
          <p style="margin:0; padding: 0;">blog</p>
        </a>
        <a href="https://store.weareunder.design/pages/newsletter" target="_blank">
          <p style="margin:0; padding: 0;">newsletter</p>
        </a>
        <a href="mailto:hello@weareunder.design">
          <p style="margin:0; padding: 0;">contact</p>
        </a>
        <a href="https://weareunder.design/legal">
          <p style="margin:0; padding: 0;">legal</p>
        </a>
      </div>
      <div class="column align-start gap-xs">
        <a href="https://www.instagram.com/under.design/" target="_blank">
          <p style="margin:0; padding: 0;">instagram</p>
        </a>
        <a href="https://x.com/underdesign_" target="_blank">
          <p style="margin:0; padding: 0;">twitter</p>
        </a>
        <a href="https://github.com/weareunderdesign" target="_blank">
          <p style="margin:0; padding: 0;">github</p>
        </a>
      </div>
      <div>

        </div>
    </div>
    
  </div>
</footer>
`;

function updateThemeElementsVisibility() {
  const theme = document.documentElement.getAttribute("data-theme");
  const lightElements = document.querySelectorAll(".light");
  const darkElements = document.querySelectorAll(".dark");

  lightElements.forEach((element) => {
    element.style.display = theme === "dark" ? "none" : "";
  });

  darkElements.forEach((element) => {
    element.style.display = theme === "dark" ? "" : "none";
  });
  try {
    updateThemeImageNew(theme); 
  } catch (error) {
    console.error('Error in updateThemeImageNew:', error); 
  } finally {
    updateThemeImage(theme); 
  }
}

function handleSystemThemeChange(e) {
  let theme;
  if (e.matches) {
    theme = "dark";
    document.documentElement.setAttribute("data-theme", "dark");
  } else {
    theme = "light";
    document.documentElement.setAttribute("data-theme", "light");
  }
  updateThemeElementsVisibility();
  switchFavicon(theme);
}

const setSystemTheme = () => {
  if (
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
  ) {
    handleSystemThemeChange({ matches: true });
  } else {
    handleSystemThemeChange({ matches: false });
  }
};

class underFooter extends HTMLElement {
  constructor() {
    super();
    this.innerHTML = footerTemplate;
  }

  connectedCallback() {
    updateThemeElementsVisibility();
    handleSystemThemeChange(
      window.matchMedia("(prefers-color-scheme: dark)")
    );
  }
}

customElements.define("under-footer", underFooter);

window
  .matchMedia("(prefers-color-scheme: dark)")
  .addEventListener("change", handleSystemThemeChange);

const currentYear = new Date().getFullYear();
document.getElementById("year").innerHTML += currentYear;

var body = document.querySelector("body");
var themeName = document.querySelector("#theme-name");

themeName.textContent = "system";

function toggleTheme() {
  let theme;
  switch (themeName.textContent) {
    case "system":
      theme = "light";
      document.documentElement.setAttribute("data-theme", "light");
      themeName.textContent = "light";
      localStorage.setItem("theme", "light");
      break;
    case "light":
      theme = "dark";
      document.documentElement.setAttribute("data-theme", "dark");
      themeName.textContent = "dark";
      localStorage.setItem("theme", "dark");
      break;
    case "dark":
      theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? "dark" : "light";
      document.documentElement.removeAttribute("data-theme");
      themeName.textContent = "system";
      localStorage.removeItem("theme");
      setSystemTheme();
      break;
  }
  updateThemeElementsVisibility();
}

var storedTheme = localStorage.getItem("theme");

if (storedTheme) {
  document.documentElement.setAttribute("data-theme", storedTheme);
  themeName.textContent = storedTheme;
  updateThemeElementsVisibility();
} else {
  setSystemTheme();
  updateThemeElementsVisibility();
}

function switchFavicon(theme) {
  const link = document.querySelector("link[rel*='icon']") || document.createElement('link');
  link.type = 'image/png';
  link.rel = 'shortcut icon';
  link.href = `https://rnbw.design/images/favicon-${theme}.png`;

  document.getElementsByTagName('head')[0].appendChild(link);
}

function updateThemeImage(theme) {
  const image = document.getElementById('theme-image');
  if (theme === 'dark') {
    image.src = 'images/guide-dark.png';
  } else {
    image.src = 'images/guide-light.png';
  }
}

function updateThemeImageNew(theme) {
  const image = document.getElementById('theme-image-new');
  if (theme === 'dark') {
    image.src = 'images/new-dark.svg';
  } else {
    image.src = 'images/new-light.svg';
  }
}

setSystemTheme();