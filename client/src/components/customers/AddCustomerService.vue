<!-- AddService.vue -->
<template>
  <div class="container" style="max-width: 450px">
    <!-- Dropdown menu to select a service -->
    <div class="mb-3">
      <label for="serviceSelect" class="form-label">Select a Service</label>
      <select
        v-model="selectedService"
        aria-label="Select a Service"
        id="serviceSelect"
        class="form-select form-select-sm"
      >
        <option value="" disabled :selected="!selectedService">
          Select a Service
        </option>
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
    <button
      @click="addService"
      class="btn btn-primary"
      :disabled="!selectedService"
    >
      Add Service
    </button>
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
      selectedService: "",
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
        const response = await axios.get("services/all/");
        this.allServices = response.data;
      } catch (error) {
        console.error("Error fetching services:", error);
      }
      this.$store.commit("setIsLoading", false);
    },
    async addService() {
      if (!this.selectedService) {
        toast.error("Please select a service.", {
          autoClose: 1000,
        });
        return;
      }
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
        await axios.patch(
          `customers/${this.$route.params.id}/add-service/${this.selectedService}`
        );
        this.fetchCustomerDetails(this.$route.params.id);
      } catch (error) {
        toast.error("Something went wrong. Please try again.", {
          autoClose: 1000,
        });
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
