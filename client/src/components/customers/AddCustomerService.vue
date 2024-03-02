<!-- AddService.vue -->
<template>
  <div class="container">
    <!-- Dropdown menu to select a service -->
    <div class="mb-3">
      <label for="serviceSelect" class="form-label">Select a Service</label>
      <select
        v-model="selectedService"
        aria-label="Default select example"
        id="serviceSelect"
        class="form-select"
      >
        <option value="" disabled selected>Select a Service</option>
        <option
          v-for="service in allServices"
          :key="service.id"
          :value="service.id"
        >
          {{ service.name }}
        </option>
      </select>
    </div>

    <!-- Add Service button -->
    <button @click="addService" class="btn btn-primary">Add Service</button>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "vue3-toastify";
export default {
  name: "AddCustomerService",
  props: {
    fetchCustomerDetails: Function,
    customer: Object,
  },
  data() {
    return {
      selectedService: null,
      allServices: [], // To store all available services
    };
  },
  mounted() {
    this.fetchAllServices();
  },
  methods: {
    async fetchAllServices() {
      this.$store.commit("setIsLoading", true);

      try {
        const response = await axios.get("services/");
        this.allServices = response.data;
      } catch (error) {
        console.error("Error fetching services:", error);
      }
      this.$store.commit("setIsLoading", false);
    },
    async addService() {
      if (this.selectedService === null || this.selectedService === "") {
        toast.error("Please select a service.", {
          autoClose: 1000,
        });
        return;
      }
      const isValidService = this.customer.services.some(
        (service) => service.id === this.selectedService
      );
      if (isValidService) {
        // Display an error message or handle it as needed
        console.error("Invalid service selected.");
        toast.error("Service Already added.", {
          autoClose: 1000,
        });
        return;
      }

      this.$store.commit("setIsLoading", true);
      try {
        // Send POST request to add the selected service to the customer
        await axios.patch(
          `customers/${this.$route.params.id}/add-service/${this.selectedService}`
        );
        this.fetchCustomerDetails(this.$route.params.id);
        // Optionally, redirect to the customer detail page or perform other actions
      } catch (error) {
        console.error("Error adding service to customer:", error);
      }
      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>

<style>
/* Add your custom styles here */
</style>
