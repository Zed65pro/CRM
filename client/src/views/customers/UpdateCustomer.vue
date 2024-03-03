<!-- updateCustomer.vue -->
<template>
  <div class="container">
    <h2 class="mb-4">Update Customer</h2>
    <form @submit.prevent="updateCustomer">
      <!-- Add your form fields for updating customer details here -->
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
        <select
          v-model="customer.address"
          id="address"
          class="form-select form-select-sm"
          autocomplete="true"
          required
        >
          <option value="" disabled selected>Select a city</option>
          <option value="Nablus">Nablus</option>
          <option value="Haifa">Haifa</option>
          <option value="Al-Khalil">Al-Khalil</option>
          <option value="Ramallah">Ramallah</option>
          <option value="Bethlehem">Bethlehem</option>
          <option value="Tulkarem">Tulkarem</option>
          <option value="Gaza">Gaza</option>
          <option value="Jinen">Jinen</option>
        </select>
        <div class="invalid-feedback">Please select a city.</div>
      </div>

      <div class="form-outline mb-4">
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
      customer: {
        id: "",
        first_name: "",
        last_name: "",
        address: "",
        phone_number: "",
      },
    };
  },
  mounted() {
    // Fetch existing customer details using axios
    this.fetchCustomerDetails();
  },
  methods: {
    async fetchCustomerDetails() {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.get(`customers/${this.$route.params.id}`);
        this.customer = response.data;
      } catch (error) {
        toast.error("Something went wrong. Please try again.", {
          autoClose: 1000,
        });
        console.error("Error fetching customer details:", error);
      }
      this.$store.commit("setIsLoading", false);
    },
    async updateCustomer() {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.put(
          `customers/${this.$route.params.id}/`,
          this.customer
        );
        // Optionally, you can redirect to the customer details page or perform other actions.
        this.$router.go(-1);
      } catch (error) {
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
