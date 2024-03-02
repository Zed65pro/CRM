<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-lg-6">
        <div class="text-center mb-4">
          <h2 class="display-4 text-primary">Add Service</h2>
          <p class="lead">Provide details for your new service.</p>
        </div>
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
              rows="4"
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
            />
          </div>

          <!-- Submit button -->
          <button type="submit" class="btn btn-primary btn-block mb-4">
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
      servicePrice: 0,
      serviceDuration: 0,
    };
  },
  methods: {
    async submitForm() {
      this.$store.commit("setIsLoading", true);

      const newService = {
        name: this.serviceName,
        description: this.serviceDescription,
        price: this.servicePrice,
        duration_months: this.serviceDuration,
      };

      await axios
        .post("services/", newService)
        .then((response) => {
          console.log("Service added successfully:", response.data);
          toast.success("Service added successfuly!", {
            autoClose: 1000,
          });
          this.$router.push("/dashboard/services");
          // Optionally, you can redirect to the services page or perform other actions.
        })
        .catch((error) => {
          console.error("Error adding service:", error);
        });
      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>

<style>
/* Add your custom styles here */
</style>
