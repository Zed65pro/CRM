<template>
  <div class="container">
    <!-- Display customer information -->
    <h2 v-if="customer" class="mb-4">Customer Details</h2>
    <div v-if="!customer">User Not found</div>
    <div v-else class="card">
      <div class="card-body">
        <h5 class="card-title">Customer Details</h5>

        <div class="row mb-3">
          <div class="col-md-6">
            <p class="fw-bold mb-2">
              <strong>First Name:</strong> {{ customer.first_name }}
            </p>
            <p class="fw-bold mb-2">
              <strong>Last Name:</strong> {{ customer.last_name }}
            </p>
          </div>

          <div class="col-md-6">
            <p class="fw-bold mb-2">
              <strong>Address:</strong> {{ customer.address }}
            </p>
            <p class="fw-bold mb-2">
              <strong>Phone number:</strong> {{ customer.phone_number }}
            </p>
          </div>
        </div>

        <router-link
          :to="{
            name: 'UpdateCustomer',
            params: { id: $route.params.id },
          }"
          class="btn btn-primary btn-with-icon btn-sm me-1"
        >
          <AkEdit class="icon" style="font-size: 22px" />
        </router-link>

        <DeleteCustomer :customer="customer" />
        <!-- Add more customer details as needed -->
      </div>
    </div>
    <!-- Button to Add New Service -->
    <AddCustomerService
      :fetchCustomerDetails="fetchCustomerDetails"
      :customer="customer"
    />
    <!-- Display services associated with the customer -->

    <h2 v-if="customer.services && !customer.services.length" class="mt-5">
      Customer is not subscribed to any service
    </h2>
    <div v-else-if="customer">
      <h3 class="mt-4">Services</h3>
      <table class="table table-striped text-center">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Price</th>
            <th>Duration (months)</th>
            <th>Actions</th>
            <!-- Add more service details as needed -->
          </tr>
        </thead>
        <tbody class="align-middle">
          <tr v-for="service in customer.services" :key="service.id">
            <td>{{ service.id }}</td>
            <td>{{ service.name }}</td>
            <td>{{ service.description }}</td>
            <td>{{ service.price }}</td>
            <td>{{ service.duration_months }}</td>
            <td>
              <DeleteCustomerService
                :service_id="service.id"
                :fetchCustomerDetails="fetchCustomerDetails"
              />
            </td>
            <!-- Add more service details as needed -->
          </tr>
        </tbody>
      </table>
    </div>
    <h3>MANAGEMENT++</h3>
  </div>
</template>

<script>
import axios from "axios";
import DeleteCustomer from "../../components/customers/DeleteCustomer";
import DeleteCustomerService from "../../components/customers/DeleteCustomerService";
import AddCustomerService from "../../components/customers/AddCustomerService";
import axiosAuthMixin from "../../mixins/axiosAuthMixin.js";
import { AkEdit } from "@kalimahapps/vue-icons";
import { toast } from "vue3-toastify";

export default {
  name: "Customer",
  mixins: [axiosAuthMixin],
  data() {
    return {
      customer: {},
    };
  },
  components: {
    DeleteCustomer,
    DeleteCustomerService,
    AddCustomerService,
    AkEdit,
  },
  mounted() {
    // Fetch customer details from the backend based on the route parameter
    const customerId = this.$route.params.id;
    this.fetchCustomerDetails(customerId);
  },
  methods: {
    async fetchCustomerDetails(customerId) {
      this.$store.commit("setIsLoading", true);
      await axios
        .get(`customers/${customerId}/`)
        .then((response) => {
          this.customer = response.data;
        })
        .catch((error) => {
          this.customer = null;
          toast.error("Something went wrong. Please try again.", {
            autoClose: 1000,
          });
          console.error("Error fetching customer details:", error);
        });
      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>

<style>
/* Add your custom styles here */
</style>
