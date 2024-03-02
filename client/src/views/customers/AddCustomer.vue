<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-lg-6">
        <div class="text-center mb-4">
          <h2 class="display-4 text-primary">Add Customer</h2>
          <p class="lead">Provide details to add a new customer..</p>
        </div>
        <form @submit.prevent="submitForm">
          <!-- Customer Name input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="first_name">First Name</label>
            <input
              v-model="first_name"
              type="text"
              id="first_name"
              placeholder="Enter the Customer's First name..."
              class="form-control"
            />
          </div>
          <div class="form-outline mb-4">
            <label class="form-label" for="last_name">Last Name</label>
            <input
              v-model="last_name"
              type="text"
              id="last_name"
              placeholder="Enter the Customer's last name..."
              class="form-control"
            />
          </div>

          <!-- Customer Description input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="address">Address</label>
            <textarea
              v-model="address"
              id="address"
              placeholder="Enter the customer's address..."
              class="form-control"
              rows="4"
            ></textarea>
          </div>

          <!-- Price input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="phone_number">Phone number</label>
            <input
              v-model="phone_number"
              type="number"
              id="phone_number"
              placeholder="Enter the customer's phone number..."
              pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
              class="form-control"
            />
          </div>

          <!-- Submit button -->
          <button type="submit" class="btn btn-primary btn-block mb-4">
            Add Customer
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
  name: "AddCustomer",
  mixins: [axiosAuthMixin],
  data() {
    return {
      first_name: "",
      last_name: "",
      address: "",
      phone_number: null,
    };
  },
  methods: {
    async submitForm() {
      this.$store.commit("setIsLoading", true);
      const newCustomer = {
        first_name: this.first_name,
        last_name: this.last_name,
        address: this.address,
        phone_number: this.phone_number,
      };

      await axios
        .post("customers/", newCustomer)
        .then((response) => {
          console.log("Service added successfully:", response.data);
          toast.success("Service added successfuly!", {
            autoClose: 1000,
          });
          this.$router.push("/dashboard/customers");
          // Optionally, you can redirect to the services page or perform other actions.
        })
        .catch((error) => {
          console.error("Error adding customer:", error);
        });
      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>

<style>
/* Add your custom styles here */
</style>
