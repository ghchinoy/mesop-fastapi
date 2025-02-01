import {
  LitElement,
  html,
} from "https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js";

class FetchWebComponent extends LitElement {
  static properties = {
    value: { type: String },
    valueHandlerId: { type: String },
  };

  constructor() {
    super();
    this.value = "";
  }

  connectedCallback() {
    super.connectedCallback();
    this.fetchData();
  }

  async fetchData() {
    try {
      const response = await fetch("/hello");
      this.value = await response.text();
      this.dispatchValue();
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }

  render() {
    return html` <div>Value from shared module: <code>${this.value}</code></div> `;
  }

  dispatchValue() {
    this.dispatchEvent(
      new MesopEvent(this.valueHandlerId, {
        value: this.value,
      })
    );
  }
}

customElements.define("fetch-web-component", FetchWebComponent);
