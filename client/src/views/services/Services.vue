<template>
  <div class="container-fluid">
    <!-- Page Title -->
    <h2 class="mb-3">List of Services</h2>

    <!-- Add Service Button (Visible to Staff only) -->
    <router-link
      :to="{ name: 'AddService' }"
      v-if="$store.state.user && $store.state.user.is_staff"
    >
      <button type="button" class="btn btn-success mb-4">Add Service</button>
    </router-link>

    <!-- Search Bar -->
    <div class="container">
      <div class="mb-3">
        <!-- Search input -->
        <input
          v-model="searchQuery"
          type="text"
          style="max-width: 600px"
          class="form-control mx-auto"
          id="searchServices"
          placeholder="Search services..."
          @keyup.enter="fetchServices(1)"
        />
      </div>
    </div>
    <div class="mb-3">
      <!-- Display the number of services found -->
      <p>
        {{ paginationData ? paginationData.count : filteredServices.length }}
        <strong>services</strong> found.
      </p>
    </div>

    <!-- Services Table -->
    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
          <!-- Table headers -->
          <tr>
            <th>Name</th>
            <th>Price</th>
            <th>Duration (months)</th>
            <th>Added since</th>
            <th>Created By</th>
            <th v-if="$store.state.user && $store.state.user.is_staff">
              Actions
            </th>
          </tr>
        </thead>
        <tbody>
          <!-- Loop through services and display in the table -->
          <tr v-for="service in services" :key="service.id">
            <td>{{ service.name }}</td>
            <td>{{ service.price }}</td>
            <td>{{ service.duration_months }}</td>
            <td>{{ formattedDate(service.created_at) }}</td>
            <td>@{{ service.created_by.username }}</td>
            <td v-if="$store.state.user && $store.state.user.is_staff">
              <!-- Component for updating a service -->
              <UpdateService
                :selectedService="{ ...service }"
                @update-services="updateServices"
              />
              <!-- Component for deleting a service -->
              <DeleteService
                :selectedService="{ ...service }"
                @delete-services="deleteServices"
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
          @pagination-change-page="fetchServices"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import UpdateService from "../../components/services/UpdateService";
import DeleteService from "../../components/services/DeleteService";
import axiosAuthMixin from "../../mixins/axiosAuthMixin.js";
import Pagination from "../../components/Layout/Pagination";
import { toast } from "vue3-toastify";
import { formatDate } from "../../utils/formatDate.js";

export default {
  name: "Services",
  mixins: [axiosAuthMixin],
  components: {
    UpdateService,
    DeleteService,
    Pagination,
  },
  data() {
    return {
      services: [],
      searchQuery: "",
      paginationData: {
        count: 1,
        next: "",
        previous: "",
        currentPage: 1, // Add currentPage property
        totalPages: 1,
      },
    };
  },
  mounted() {
    // Fetch services on component mount
    document.title = "CRM | Services";
    this.fetchServices();
  },
  methods: {
    // Format ISO date to a human-readable format
    formattedDate(isoDate) {
      return formatDate(isoDate);
    },
    // Fetch services from the server
    async fetchServices(page = 1) {
      this.$store.commit("setIsLoading", true);
      try {
        // Make API request to fetch services
        const response = await axios.get("services/", {
          params: {
            search: this.searchQuery,
            page,
          },
        });
        // Update component data with fetched services and pagination info
        this.services = response.data.results;
        this.paginationData = {
          count: response.data.count,
          next: response.data.next,
          previous: response.data.previous,
          currentPage: page, // Add currentPage property
          totalPages: Math.ceil(response.data.count / 6), // 6 is a magic number yes, should MAKE constant, its the limit of the table
        };
      } catch (error) {
        // Handle errors and show a toast message
        toast.error("Something went wrong. Please try again.", {
          autoClose: 1000,
        });
        console.error("Error fetching services:", error);
      } finally {
        // Set loading state to false
        this.$store.commit("setIsLoading", false);
      }
    },
    // Update services array after a service is updated
    updateServices(service) {
      const index = this.services.findIndex((s) => s.id === service.id);
      if (index !== -1) {
        this.services[index] = service;
      }
    },
    // Fetch services after a service is deleted
    deleteServices(service_id) {
      if (this.services.length === 1 && this.paginationData.currentPage > 1)
        this.fetchServices(this.paginationData.currentPage - 1);
      else {
        this.fetchServices(this.paginationData.currentPage);
      }
    },
  },
};
</script>

<style>
/* Add your custom styles here */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Dark overlay with opacity */
  z-index: 1050; /* Higher than Bootstrap modal z-index */
}
</style>
