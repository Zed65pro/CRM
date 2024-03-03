import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import "vue3-toastify/dist/index.css";
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";

// Inject the missing feature flag
window.__VUE_PROD_HYDRATION_MISMATCH_DETAILS__ = false;

axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL;

createApp(App).use(store).use(router, axios).mount("#app");
