import {
  LitElement,
  html,
  css,
} from "https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js";

class FetchWebComponent extends LitElement {
  static properties = {
    value: { type: String },
    // this is the component property name which matches the Mesop definition
    valueHandlerId: { type: String },
  };

  static styles = css`

    :host {
      --secondary-background-color: #fcf7f7;
    }

    .web-component-container {
      border: 1px solid #ccc; /* Light grey, thin border */
      position: relative; /* Needed for absolute positioning of the label */
      padding: 15px; /* Add some padding inside the border */
      background-color: var(--secondary-background-color);      
      border-radius: 8px;
    }

    .web-component-label {
      position: absolute;
      top: -8px; /* Adjust as needed to position above the border */
      left: 10px; /* Adjust as needed for horizontal positioning */
      background-color: white; /* Or a light grey if preferred */
      padding: 2px 5px; /* Small padding for the label */
      font-size: 12px; /* Adjust font size as needed */
      border-radius: 3px; /* Optional: Add rounded corners to the label */
      color: lightslategray;
    }
  `;

  constructor() {
    super();
    this.value = "";
  }

  updated(changedProperties) {
    if (changedProperties.has('input') && this.input) {
      this.fetchData();
    }
  }

  connectedCallback() {
    super.connectedCallback();
    this.fetchData();
  }

  async fetchData() {
    try {
      console.log("calling /hello from web component")
      const response = await fetch("/hello");
      this.value = await response.text();
      this.dispatchValue();
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }

  render() {
    return html`
      <div class="web-component-container">
        <span class="web-component-label">web component</span>
        Value from shared module: <code>${this.value}</code>
      </div> 
    `;
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
