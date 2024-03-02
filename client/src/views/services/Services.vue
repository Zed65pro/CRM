<template>
  <div class="container-fluid">
    <h2 class="mb-4">List of Services</h2>

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
        />
      </div>
    </div>

    <!-- Services Table -->
    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
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
          <tr v-for="service in filteredServices" :key="service.id">
            <td>{{ service.name }}</td>
            <td>{{ service.description }}</td>
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
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { formatDate } from "../../utils/formatDate.js";
import UpdateService from "../../components/services/UpdateService";
import DeleteService from "../../components/services/DeleteService";
import axiosAuthMixin from "../../mixins/axiosAuthMixin.js";

export default {
  name: "Services",
  mixins: [axiosAuthMixin],
  components: {
    UpdateService,
    DeleteService,
  },
  data() {
    return {
      services: [],
      searchQuery: "",
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
    async fetchServices() {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.get("services/");
        this.services = response.data;
      } catch (error) {
        console.error("Error fetching services:", error);
      }
      this.$store.commit("setIsLoading", false);
    },

    openDeleteModal(service) {
      this.selectedService = { ...service };
      this.showDeleteModal = true;
    },

    closeDeleteModal() {
      this.selectedService = null;
      this.showDeleteModal = false;
    },
    async confirmDelete() {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.delete(
          `services/${this.selectedService.id}/`
        );
        this.services = this.services.filter(
          (service) => service.id !== this.selectedService.id
        );
        this.closeDeleteModal();
      } catch (error) {
        console.error("Error deleting service:", error);
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
      this.services = this.services.filter(
        (service) => service.id !== service_id
      );
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
