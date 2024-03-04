<!-- UpdateCustomer.vue -->

<template>
  <div class="container">
    <!-- Page Title -->
    <h2 class="mb-4">Update Customer</h2>

    <!-- Update Customer Form -->
    <form @submit.prevent="updateCustomer">
      <!-- Form Fields for Updating Customer Details -->
      <div class="form-group">
        <label for="firstName">First Name</label>
        <input
          v-model="customer.first_name"
          type="text"
          class="form-control"
          id="firstName"
          pattern="[a-zA-Z]{1,25}"
          oninvalid="this.setCustomValidity('Please enter the customer\'s first name')"
          oninput="setCustomValidity('')"
          required
        />
      </div>

      <div class="form-group">
        <label for="lastName">Last Name</label>
        <input
          v-model="customer.last_name"
          type="text"
          class="form-control"
          id="lastName"
          pattern="[a-zA-Z]{1,25}"
          oninvalid="this.setCustomValidity('Please enter the customer\'s last name.')"
          oninput="setCustomValidity('')"
          required
        />
      </div>

      <div class="form-outline mb-4">
        <label class="form-label" for="address">City</label>
        <!-- Select City Dropdown -->
        <select
          v-model="customer.address"
          id="address"
          class="form-select"
          autocomplete="true"
          oninvalid="this.setCustomValidity('Please select a city.')"
          oninput="setCustomValidity('')"
          required
        >
          <option value="" disabled>Select a city</option>
          <option
            v-for="city in cities"
            :key="city"
            :value="city"
            :selected="city === customer.address"
          >
            {{ city }}
          </option>
        </select>
        <div class="invalid-feedback">Please select a city.</div>
      </div>

      <div class="form-outline mb-4">
        <!-- Phone Number Input with Prefix -->
        <label class="form-label" for="phone_number">Phone number</label>
        <div class="input-group">
          <span class="input-group-text">+970</span>
          <input
            v-model="customer.phone_number"
            type="tel"
            id="phone_number"
            placeholder="i.e 551936142"
            pattern="[0-9]{9}"
            oninvalid="this.setCustomValidity('Please enter a valid phone number.')"
            oninput="setCustomValidity('')"
            class="form-control"
            required
          />
          <div class="invalid-feedback">Please enter a valid phone number.</div>
        </div>
      </div>

      <!-- Submit Button -->
      <button type="submit" class="btn btn-primary mt-4">
        Update Customer
      </button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import axiosAuthMixin from "../../mixins/axiosAuthMixin.js";
import { toast } from "vue3-toastify";

export default {
  name: "UpdateCustomer",
  mixins: [axiosAuthMixin],
  data() {
    return {
      // Customer object with initial values
      customer: {
        id: "",
        first_name: "",
        last_name: "",
        address: "",
        phone_number: "",
      },
      cities: [
        "Gaza",
        "Nablus",
        "Quds",
        "Al-Khalil",
        "Ramallah",
        "Bethlehem",
        "Tulkarem",
        "Jinen",
      ],
    };
  },
  beforeMount() {
    // Fetch existing customer details using axios on component mount
    this.fetchCustomerDetails();
  },
  methods: {
    // Fetch customer details from the backend
    async fetchCustomerDetails() {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.get(`customers/${this.$route.params.id}`);
        this.customer = { ...response.data };
      } catch (error) {
        // Handle errors and show a toast message
        toast.error("Something went wrong. Please try again.", {
          autoClose: 1000,
        });
        console.error("Error fetching customer details:", error);
      } finally {
        this.$store.commit("setIsLoading", false);
      }
    },
    // Update customer details on form submission
    async updateCustomer() {
      this.$store.commit("setIsLoading", true);
      try {
        // Send a PUT request to update customer details
        const response = await axios.put(
          `customers/${this.$route.params.id}/`,
          this.customer
        );
        // Optionally, you can redirect to the customer details page or perform other actions.
        this.$router.go(-1);
      } catch (error) {
        // Handle different error scenarios and show appropriate toast messages
        if (error.response.status === 400) {
          toast.error("Phone number already in use.", {
            autoClose: 1000,
          });
        } else {
          toast.error("Something went wrong. Please try again.", {
            autoClose: 1000,
          });
        }
        console.error("Error updating customer:", error);
      }
      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>

<style>
/* Add your custom styles here */
</style>
