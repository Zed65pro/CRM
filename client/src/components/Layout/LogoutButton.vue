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
    async logout() {
      this.$store.commit("setIsLoading", true);

      await axios
        .post("token/logout")
        .then((response) => {
          console.log("LOGGED OUT");
        })
        .catch((error) => {
          console.log(error);
        });

      this.$store.commit("removeToken");
      this.$store.commit("removeUser");
      axios.defaults.headers.common["Authorization"] = "";
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      this.$router.push("/login");
      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>
