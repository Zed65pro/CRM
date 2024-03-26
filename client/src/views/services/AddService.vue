<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-lg-6">
        <!-- Heading and Subheading -->
        <div class="text-center mb-4">
          <h2 class="display-4 text-success">Add Service</h2>
          <p class="lead">Provide details for your new service.</p>
        </div>

        <!-- Service Form -->
        <form @submit.prevent="submitForm">
          <!-- Service Name input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="serviceName">Service Name</label>
            <input
              v-model="serviceName"
              type="text"
              id="serviceName"
              placeholder="Enter the service name..."
              class="form-control"
              required
              minlength="1"
              maxlength="25"
              oninvalid="this.setCustomValidity('Please enter the service\'s name.')"
              oninput="setCustomValidity('')"
            />
          </div>

          <!-- Service Description input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="serviceDescription"
              >Description</label
            >
            <textarea
              v-model="serviceDescription"
              id="serviceDescription"
              placeholder="Enter a description for your service..."
              class="form-control"
              minlength="1"
              maxlength="255"
              oninvalid="this.setCustomValidity('Please enter the service\'s description.')"
              oninput="setCustomValidity('')"
              rows="3"
              required
            ></textarea>
          </div>

          <!-- Price input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="servicePrice">Price</label>
            <input
              v-model="servicePrice"
              type="number"
              id="servicePrice"
              placeholder="Enter the service price..."
              class="form-control"
              step="0.01"
              min="0"
              max="10000"
              pattern="^\d{1,10000}(\.\d{1,2})?$"
              oninvalid="this.setCustomValidity('Please enter a valid service price. 2 max decimals')"
              oninput="setCustomValidity('')"
              required
            />
          </div>

          <!-- Duration input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="serviceDuration"
              >Duration (in months)</label
            >
            <input
              v-model="serviceDuration"
              type="number"
              id="serviceDuration"
              placeholder="Enter the service duration..."
              class="form-control"
              min="1"
              max="120"
              oninvalid="this.setCustomValidity('Please enter a valid service duration. upto a max of 10 years i.e 120 months.')"
              oninput="setCustomValidity('')"
              required
            />
          </div>

          <!-- Submit button -->
          <button type="submit" class="btn btn-success btn-block mb-4">
            Add Service
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "vue3-toastify";
import axiosAuthMixin from "../../mixins/axiosAuthMixin.js";

export default {
  name: "AddService",
  mixins: [axiosAuthMixin],
  data() {
    return {
      serviceName: "",
      serviceDescription: "",
      servicePrice: "",
      serviceDuration: "",
    };
  },
  mounted() {
    // Add a title to the page
    document.title = "CRM | Add Service";
  },
  methods: {
    async submitForm() {
      this.$store.commit("setIsLoading", true);

      // Create a new service object with the form data
      const newService = {
        name: this.serviceName,
        description: this.serviceDescription,
        price: this.servicePrice,
        duration_months: this.serviceDuration,
      };

      try {
        // Make a POST request to add the new service
        const response = await axios.post("services/", newService);

        toast.success("Service added successfully!", {
          autoClose: 1000,
        });

        // Redirect to the services page
        this.$router.push("/dashboard/services");
      } catch (error) {
        // Handle errors and show a toast message
        toast.error("Something went wrong. Please try again.", {
          autoClose: 1000,
        });
        console.error("Error adding service:", error);
      } finally {
        // Set loading state to false
        this.$store.commit("setIsLoading", false);
      }
    },
  },
};
</script>

<style>
/* Add your custom styles here */
</style>
