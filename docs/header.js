function addHeader() {
  const TEMPLATE = `
      <div class="padding-xl" href="/" style="display: flex; flex-direction: row; position: fixed; z-index: 99; width: 100%;">
        <a href="https://weareunder.design/" target="_blank">
        <img src="./images/under_logo.svg">
        </a>
        <img src="https://rnbw.design/images/under/handy.svg">
      </div>
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


