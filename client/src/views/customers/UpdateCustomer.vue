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
          required
        />
      </div>

      <div class="form-group">
        <label for="address">Address</label>
        <input
          v-model="customer.address"
          type="text"
          class="form-control"
          id="address"
          required
        />
      </div>

      <div class="form-group">
        <label for="phoneNumber">Phone Number</label>
        <input
          v-model="customer.phone_number"
          type="tel"
          class="form-control"
          id="phoneNumber"
          required
        />
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
