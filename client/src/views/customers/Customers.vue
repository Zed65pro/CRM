<!-- Customers.vue -->

<template>
  <div class="container-fluid">
    <div class="container">
      <h1 class="mb-4">Customer List</h1>
      <router-link :to="{ path: '/dashboard/add-customer' }">
        <button type="button" class="btn btn-success mb-4">Add Customer</button>
      </router-link>
      <SearchCustomers
        :searchQuery="searchQuery"
        :filterType="filterType"
        @set-filter="setFilter"
        @update-search-query="updateSearchQuery"
      />
    </div>
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
          <tr v-for="customer in filteredCustomers" :key="customer.id">
            <td>{{ customer.first_name }}</td>
            <td>{{ customer.last_name }}</td>
            <td>{{ customer.address }}</td>
            <td>{{ customer.phone_number }}</td>
            <td>{{ formattedDate(customer.created_at) }}</td>
            <td>@{{ customer.created_by.username }}</td>
            <td>
              <router-link
                :to="{ name: 'Customer', params: { id: customer.id } }"
                class="btn btn-primary btn-sm me-1"
              >
                Edit
              </router-link>
              <DeleteCustomer
                :customer="customer"
                :fetchCustomers="fetchCustomers"
              />
            </td>
          </tr>
        </tbody>
      </table>
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

export default {
  name: "Customers",
  components: {
    DeleteCustomer,
    SearchCustomers,
  },
  mixins: [axiosAuthMixin],
  data() {
    return {
      customers: [],
      searchQuery: "",
      filterType: "first_name",
    };
  },
  computed: {
    filteredCustomers() {
      switch (this.filterType) {
        case "first_name":
          return filters.filterByFirstName(this.customers, this.searchQuery);
        case "last_name":
          return filters.filterByLastName(this.customers, this.searchQuery);
        case "phone_number":
          return filters.filterByPhoneNumber(this.customers, this.searchQuery);
        case "address":
          return filters.filterByAddress(this.customers, this.searchQuery);
        case "service":
          return filters.filterByService(this.customers, this.searchQuery);
        default:
          return this.customers;
      }
    },
  },
  mounted() {
    this.fetchCustomers();
  },
  methods: {
    formattedDate(isoDate) {
      return formatDate(isoDate);
    },
    async fetchCustomers() {
      this.$store.commit("setIsLoading", true);
      await axios
        .get("customers/")
        .then((response) => {
          this.customers = response.data;
        })
        .catch((error) => {
          console.error("Error fetching customers:", error);
        });
      this.$store.commit("setIsLoading", false);
    },
    setFilter(filterType) {
      this.filterType = filterType;
    },
    updateSearchQuery(value) {
      this.searchQuery = value;
    },
  },
};
</script>

<style>
/* Add your custom styles here */
</style>
