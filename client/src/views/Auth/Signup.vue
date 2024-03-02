<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-lg-6">
        <div class="text-center mb-4">
          <h2 class="display-4 text-success">Sign up</h2>
          <p class="lead">Create your new account here and now.</p>
        </div>
        <form @submit.prevent="SubmitForm">
          <!-- Username input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="username">Username</label>
            <input
              type="text"
              id="username"
              placeholder="Enter your username..."
              class="form-control"
              v-model="username"
            />
          </div>

          <!-- Email input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="email">Email address</label>
            <input
              type="email"
              id="email"
              placeholder="Enter your email address..."
              class="form-control"
              v-model="email"
            />
          </div>

          <!-- Password input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="password1">Password</label>
            <input
              type="password"
              placeholder="Enter your password..."
              id="password1"
              class="form-control"
              v-model="password"
            />
          </div>

          <!-- Repeat Password input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="password2">Confirm Password</label>
            <input
              type="password"
              placeholder="Repeat you password..."
              id="password2"
              class="form-control"
              v-model="confirmPassword"
            />
          </div>
          <div
            class="alert alert-danger mt-3"
            role="alert"
            v-if="errors.length"
          >
            <ul>
              <li v-for="error in errors" :key="error">{{ error }}</li>
            </ul>
          </div>

          <!-- Submit button -->
          <button type="submit" class="btn btn-primary btn-block mb-4">
            Sign up
          </button>

          <!-- Login button -->
          <div class="text-center">
            <p>Already have an account? <a href="/login">Sign in</a></p>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "vue3-toastify";

export default {
  name: "Signup",
  data() {
    return {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
      errors: [],
    };
  },
  methods: {
    // Your methods here
    async SubmitForm() {
      this.$store.commit("setIsLoading", true);
      this.errors = [];

      if (!this.username) {
        this.errors.push("Username required.");
      }
      if (!this.email) {
        this.errors.push("Invalid email");
      }
      if (!this.password) {
        this.errors.push("Password required");
      }
      if (!this.confirmPassword || this.confirmPassword != this.password) {
        this.errors.push("Passwords do not match");
      }

      if (!this.errors.length) {
        const form = {
          username: this.username,
          email: this.email,
          password: this.password,
        };

        axios
          .post("users/", form)
          .then((response) => {
            //success,error,warning,info
            toast.success("Signup successful!", {
              autoClose: 1000,
            });
            this.$router.push("login");
          })
          .catch((error) => {
            if (error.response) {
              for (const property in error.response.data) {
                this.errors.push(
                  `${property}: ${error.response.data[property]}`
                );
              }
            } else if (error.message) {
              toast.error("Something Went wrong please try again.", {
                autoClose: 1000,
              });
              this.errors.push("Something Went wrong please try again.");
            }
            console.log(error);
          });
      }
      this.$store.commit("setIsLoading", false);
    },
  },
  mounted() {
    // Your mounted hook code here
    if (this.$store.state.token) {
      this.$router.push({ name: "Customers" });
    }
  },
};
</script>

<style scoped>
/* Your component styles here */
</style>
