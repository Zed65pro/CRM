<template>
  <Navbar />
  <Loading />
  <router-view />
</template>

<script>
import Navbar from "@/components/Layout/Navbar";
import Loading from "@/components/Layout/Loading";
import axios from "axios";

export default {
  name: "App",
  components: {
    Navbar,
    Loading,
  },
  beforeCreate() {
    this.$store.commit("initializeStore");

    if (this.$store.state.token) {
      axios.defaults.headers.common["Authorization"] =
        "Token" + this.$store.state.token;
      {
        /* this.$router.push("/dashboard"); */
      }
    } else {
      axios.defaults.headers.common["Authorization"] = "";
      {
        /* this.$router.push("/login"); */
      }
    }
  },
};
</script>

<style>
body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  background-color: #f4f4f4;
}
#app {
  font-family: "Roboto Slab", Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0;
  padding: 0;
  height: 100vh;
  width: 100vw;
}
</style>
