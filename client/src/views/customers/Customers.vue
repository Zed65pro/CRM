<!-- Customers.vue -->

<template>
  <div class="container-fluid">
    <div class="container">
      <!-- Page Title and Add Customer Button -->
      <h1 class="mb-3">Customer List</h1>
      <router-link :to="{ path: '/dashboard/add-customer' }">
        <button type="button" class="btn btn-success mb-4">Add Customer</button>
      </router-link>
      <!-- Search Customers Component -->
      <SearchCustomers
        :searchQuery="searchQuery"
        :filterType="filterType"
        @fetch-customers="fetchCustomers"
        @set-filter="setFilter"
        @update-search-query="updateSearchQuery"
      />
    </div>

    <!-- Display Total Number of Customers -->
    <div class="mb-3">
      <p>
        {{ paginationData ? paginationData.count : this.customers.length }}
        <strong>customers</strong> found.
      </p>
    </div>

    <!-- Table of Customer Details -->
    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Address</th>
            <th>Phone number</th>
            <th>Added since</th>
            <th>Created By</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody class="align-middle">
          <!-- Loop through customers and display details -->
          <tr v-for="customer in customers" :key="customer.id">
            <td>{{ customer.first_name }}</td>
            <td>{{ customer.last_name }}</td>
            <td>{{ customer.address }}</td>
            <td>{{ customer.phone_number }}</td>
            <td>{{ formattedDate(customer.created_at) }}</td>
            <td>@{{ customer.created_by.username }}</td>
            <td>
              <!-- Edit and Delete buttons for each customer -->
              <router-link
                :to="{ name: 'Customer', params: { id: customer.id } }"
                class="btn btn-primary btn-with-icon btn-sm me-1"
              >
                <AkEdit class="icon" style="font-size: 22px" />
              </router-link>
              <DeleteCustomer
                :customer="customer"
                @fetch-customers="fetchCustomers"
              />
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination Component -->
      <div class="d-flex justify-content-center">
        <Pagination
          :current-page="paginationData.currentPage"
          :total-pages="paginationData.totalPages"
          @pagination-change-page="fetchCustomers"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import DeleteCustomer from "../../components/customers/DeleteCustomer";
import SearchCustomers from "../../components/customers/SearchCustomers";
import { filters } from "../../utils/searchCustomersUtils.js";
import { formatDate } from "../../utils/formatDate.js";
import axiosAuthMixin from "../../mixins/axiosAuthMixin.js";
import { AkEdit } from "@kalimahapps/vue-icons";
import Pagination from "../../components/Layout/Pagination";

export default {
  name: "Customers",
  components: {
    DeleteCustomer,
    SearchCustomers,
    AkEdit,
    Pagination,
  },
  mixins: [axiosAuthMixin],
  data() {
    return {
      customers: [],
      searchQuery: "",
      filterType: "first_name",
      paginationData: {
        count: 1,
        next: "",
        previous: "",
        currentPage: 1, // Add currentPage property
        totalPages: 1,
      },
    };
  },
  computed: {
    totalCount() {
      return this.paginationData ? this.paginationData.count : 0;
    },
  },
  mounted() {
    // Fetch customers on component mount
    this.fetchCustomers();
  },
  methods: {
    // Format ISO date to a more readable format
    formattedDate(isoDate) {
      return formatDate(isoDate);
    },
    // Fetch customers from the backend with optional page parameter
    async fetchCustomers(page = 1) {
      this.$store.commit("setIsLoading", true);
      try {
        // Use axios to fetch customers with search, filter, and pagination parameters
        const response = await axios.get("customers/", {
          params: {
            search: this.searchQuery,
            filter_type: this.filterType,
            page,
          },
        });
        // Update component data with fetched customers and pagination information
        this.customers = response.data.results;
        this.paginationData = {
          count: response.data.count,
          next: response.data.next,
          previous: response.data.previous,
          currentPage: page, // Add currentPage property
          totalPages: Math.ceil(response.data.count / 6), // Assuming 6 customers per page
        };
      } catch (error) {
        // Handle errors and log them to the console
        console.error("Error fetching customers:", error);
      }
      // Unset loading state
      this.$store.commit("setIsLoading", false);
    },
    // Set the filter type for searching customers
    setFilter(filterType) {
      this.filterType = filterType;
    },
    // Update the search query for searching customers
    updateSearchQuery(value) {
      this.searchQuery = value;
    },
  },
};
</script>

<style>
/* Add your custom styles here */
</style>
