// axiosMixin.js
import axios from "axios";

export default {
  created() {
    // Set the Authorization header when the component is created
    axios.defaults.headers.common["Authorization"] =
      "Token " + this.$store.state.token;
  },
};
