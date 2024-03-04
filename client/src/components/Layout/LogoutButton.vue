<template>
  <button v-if="$store.state.token" class="btn btn-danger" @click="logout()">
    Log out
  </button>
</template>

<script>
import axios from "axios";

export default {
  name: "LogoutButton",

  methods: {
    /**
     * Handles the logout process.
     */
    async logout() {
      // Set loading state to true
      this.$store.commit("setIsLoading", true);

      try {
        // Send POST request to logout
        await axios.post("token/logout");
        console.log("LOGGED OUT");

        // Remove token and user from the store and local storage
        this.$store.commit("removeToken");
        this.$store.commit("removeUser");
        localStorage.removeItem("token");
        localStorage.removeItem("user");

        // Clear authorization header
        axios.defaults.headers.common["Authorization"] = "";

        // Redirect to login page
        this.$router.push("/login");
      } catch (error) {
        // Handle errors
        console.error("Logout error:", error);
      } finally {
        // Set loading state back to false
        this.$store.commit("setIsLoading", false);
      }
    },
  },
};
</script>
