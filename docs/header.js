function addHeader() {
  const TEMPLATE = `
      <a href="https://weareunder.design/" class="logo padding-xl mix-diff" href="/" style="display: flex; position: fixed; z-index: 99; width: 100%; justify-content: space-between;">
        <img src="https://weareunder.design/images/under-header-logo.svg" class="desktop"/>
        <img src="https://weareunder.design/images/under-header-logo-small.svg" class="mobile"/>
      </a>
    `;

  class UnderHeader extends HTMLElement {
    constructor() {
      super();
      this.innerHTML = TEMPLATE;
    }
  }
  customElements.define("under-header", UnderHeader);
}

addHeader();

const mediaQuery = window.matchMedia("(max-width: 992px)");
mediaQuery.addEventListener("change", handleMediaQueryChange);
handleMediaQueryChange(mediaQuery);

function handleMediaQueryChange(mediaQuery) {
  const mobileImg = document.querySelector("under-header img.mobile");
  const desktopImg = document.querySelector("under-header img.desktop");

  if (mediaQuery.matches) {
    mobileImg.style.display = "block";
    desktopImg.style.display = "none";
  } else {
    mobileImg.style.display = "none";
    desktopImg.style.display = "block";
  }
}
