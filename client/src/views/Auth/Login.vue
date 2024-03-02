<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-lg-6">
        <div class="text-center mb-4">
          <h2 class="display-4 text-success">Login</h2>
          <p class="lead">Enter your username and password my dear user.</p>
        </div>
        <form @submit.prevent="SubmitForm">
          <!-- Username input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="username">Username</label>
            <input
              type="text"
              id="username"
              placeholder="Enter your Username..."
              class="form-control"
              v-model="username"
              oninvalid="this.setCustomValidity('Please enter your username')"
              oninput="setCustomValidity('')"
              required
            />
          </div>

          <!-- Password input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="password">Password</label>
            <input
              type="password"
              placeholder="Enter your password..."
              id="password"
              class="form-control"
              v-model="password"
              oninvalid="this.setCustomValidity('Please enter your password')"
              oninput="setCustomValidity('')"
              required
            />
          </div>

          <!-- Submit button -->
          <button type="submit" class="btn btn-primary btn-block mb-4">
            Sign in
          </button>
          <div
            class="alert alert-danger mt-3"
            role="alert"
            v-if="errors.length"
          >
            <ul>
              <li v-for="error in errors" :key="error">{{ error }}</li>
            </ul>
          </div>

          <!-- Register buttons
          <div class="text-center">
            <p>
              Not a member? <router-link to="/signup">Register</router-link>
            </p>
          </div>-->
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { toast } from "vue3-toastify";
import axios from "axios";
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Login",
  data() {
    return {
      // Your data properties here
      username: "",
      password: "",
      errors: [],
    };
  },
  methods: {
    handleBackendErrors(error) {
      if (error.response) {
        // Handle known errors
        if (error.response.status === 400) {
          // Bad Request (validation error)
          //this.errors.push("User not available!");
          toast.error("Invalid Username or Password", {
            autoClose: 1000,
          });
        } else if (error.response.status === 401) {
          // Unauthorized
          /*this.errors.push(
            "Invalid credentials. Please check your username and password."
          );*/
          toast.warning("Unauthorized access", {
            autoClose: 1000,
          });
        } else if (error.response.status === 404) {
          // User not found
          //this.errors.push("User not found. Please check your username.");
          toast.error("Invalid Username or Password", {
            autoClose: 1000,
          });
        } else {
          // Handle other HTTP errors
          /*this.errors.push(
            `Error: ${error.response.status} - ${error.response.statusText}`
          );*/
          toast.error("Something went wrong. Please try again.", {
            autoClose: 1000,
          });
        }
      } else if (error.message) {
        // Handle network errors or other exceptions
        toast.error("Something went wrong. Please try again.", {
          autoClose: 1000,
        });
        this.errors.push("Something went wrong. Please try again.");
      }

      console.error(error);
    },
    // Your methods here
    async SubmitForm() {
      this.errors = [];
      this.$store.commit("setIsLoading", true);

      if (!this.errors.length) {
        const form = {
          username: this.username,
          password: this.password,
        };

        try {
          const response = await axios.post("token/login/", form);

          const token = response.data.auth_token;
          this.$store.commit("setToken", token);
          localStorage.setItem("token", token);
          axios.defaults.headers.common["Authorization"] = "Token " + token;

          const response_user = await axios.get("user/me/");
          const user = response_user.data;
          console.log(user);
          this.$store.commit("setUser", user); // Store user details in Vuex store
          localStorage.setItem("user", JSON.stringify(user)); // Store user details in localStorage

          toast.success("Login successful!", {
            autoClose: 1000,
          });

          this.$router.push("/dashboard");
        } catch (error) {
          this.handleBackendErrors(error);
        }
      }

      this.$store.commit("setIsLoading", false);
    },
  },
  mounted() {
    // Your mounted hook code here
    if (localStorage.getItem("token")) {
      this.$router.push({ name: "Customers" });
    }
  },
};
</script>

<style scoped>
/* Your component styles here */
</style>
