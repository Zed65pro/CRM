<template>
  <div class="container-fluid">
    <h2 class="mb-3">List of Services</h2>

    <!-- Add Service Button -->
    <router-link
      :to="{ name: 'AddService' }"
      v-if="$store.state.user && $store.state.user.is_staff"
    >
      <button type="button" class="btn btn-success mb-4">Add Service</button>
    </router-link>

    <!-- Search Bar -->
    <div class="container">
      <div class="mb-3">
        <input
          v-model="searchQuery"
          type="text"
          style="max-width: 600px"
          class="form-control mx-auto"
          placeholder="Search services..."
          @keyup.enter="fetchServices(1)"
        />
      </div>
    </div>
    <div class="mb-3">
      <p>
        {{ paginationData ? paginationData.count : this.services.length }}
        <strong>services</strong> found.
      </p>
    </div>

    <!-- Services Table -->
    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
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
          <tr v-for="service in services" :key="service.id">
            <td>{{ service.name }}</td>
            <td>{{ service.price }}</td>
            <td>{{ service.duration_months }}</td>
            <td>{{ formattedDate(service.created_at) }}</td>
            <td>@{{ service.created_by.username }}</td>
            <td v-if="$store.state.user && $store.state.user.is_staff">
              <UpdateService
                v-if="$store.state.user && $store.state.user.is_staff"
                :selectedService="{ ...service }"
                @update-services="updateServices"
              />
              <DeleteService
                v-if="$store.state.user && $store.state.user.is_staff"
                :selectedService="{ ...service }"
                @delete-services="deleteServices"
              />
            </td>
          </tr>
        </tbody>
      </table>
      <!-- Pagination -->
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
import { formatDate } from "../../utils/formatDate.js";
import UpdateService from "../../components/services/UpdateService";
import DeleteService from "../../components/services/DeleteService";
import axiosAuthMixin from "../../mixins/axiosAuthMixin.js";
import { toast } from "vue3-toastify";
import Pagination from "../../components/Layout/Pagination";

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
  computed: {
    filteredServices() {
      return this.services.filter(
        (service) =>
          service.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          service.description
            .toLowerCase()
            .includes(this.searchQuery.toLowerCase())
      );
    },
  },
  mounted() {
    this.fetchServices();
  },
  methods: {
    formattedDate(isoDate) {
      return formatDate(isoDate);
    },
    async fetchServices(page = 1) {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.get("services/", {
          params: {
            search: this.searchQuery,
            page,
          },
        });
        this.services = response.data.results;
        this.paginationData = {
          count: response.data.count,
          next: response.data.next,
          previous: response.data.previous,
          currentPage: page, // Add currentPage property
          totalPages: Math.ceil(response.data.count / 6),
        };
      } catch (error) {
        toast.error("Something went wrong. Please try again.", {
          autoClose: 1000,
        });
        console.error("Error fetching services:", error);
      }
      this.$store.commit("setIsLoading", false);
    },
    updateServices(service) {
      // Find the index of the modified service in this.services and update it
      const index = this.services.findIndex(
        (service) => service.id === service.id
      );

      // Update the array element directly
      if (index !== -1) {
        this.services[index] = service;
      }
    },
    deleteServices(service_id) {
      // Find the index of the modified service in this.services and update it
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
