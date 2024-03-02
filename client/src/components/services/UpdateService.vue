<template>
  <button
    @click="openEditModal(service)"
    class="btn btn-primary btn-sm me-2 mb-1"
  >
    Edit
  </button>
  <div v-if="showEditModal" class="overlay" @click="closeEditModal"></div>
  <!-- Edit Service Modal -->
  <div
    v-if="showEditModal"
    class="modal fade show"
    id="editServiceModal"
    tabindex="-1"
    aria-labelledby="editServiceModalLabel"
    aria-hidden="true"
    style="display: block"
    @click="closeEditModal"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg" @click.stop>
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="editServiceModalLabel">Edit Service</h5>
          <button
            type="button"
            class="btn-close"
            @click="closeEditModal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <!-- Service Edit Form -->
          <form @submit.prevent="submitEditForm">
            <div class="mb-3">
              <label for="editServiceName" class="form-label"
                >Service Name</label
              >
              <input
                v-model="selectedService.name"
                type="text"
                class="form-control"
                id="editServiceName"
                required
              />
            </div>
            <div class="mb-3">
              <label for="editServiceDescription" class="form-label"
                >Description</label
              >
              <textarea
                v-model="selectedService.description"
                class="form-control"
                id="editServiceDescription"
                rows="3"
              ></textarea>
            </div>
            <div class="mb-3">
              <label for="editServicePrice" class="form-label">Price</label>
              <input
                v-model="selectedService.price"
                type="number"
                class="form-control"
                id="editServicePrice"
                required
              />
            </div>
            <div class="mb-3">
              <label for="editServiceDuration" class="form-label"
                >Duration (months)</label
              >
              <input
                v-model="selectedService.duration_months"
                type="number"
                class="form-control"
                id="editServiceDuration"
                required
              />
            </div>
            <!-- Add other form fields as needed -->

            <button type="submit" class="btn btn-primary">Save Changes</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UpdateService",
  props: {
    selectedService: Object,
  },
  emits: ["update-services"],
  data() {
    return {
      showEditModal: false,
    };
  },
  methods: {
    openEditModal(service) {
      this.showEditModal = true;
    },

    closeEditModal() {
      this.showEditModal = false;
    },

    async submitEditForm() {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.put(
          `services/${this.selectedService.id}/`,
          this.selectedService
        );
        this.$emit("update-services", response.data);

        this.closeEditModal();
      } catch (error) {
        console.error("Error updating service:", error);
      }
      this.$store.commit("setIsLoading", false);
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
