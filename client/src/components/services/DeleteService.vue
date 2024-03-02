<template>
  <!-- Delete Service Popup -->
  <button @click="openDeleteModal(service)" class="btn btn-danger btn-sm mb-1">
    Delete
  </button>
  <div v-if="showDeleteModal" class="overlay" @click="closeDeleteModal"></div>
  <div
    v-if="showDeleteModal"
    class="modal fade show"
    style="display: block"
    @click="closeDeleteModal"
  >
    <div class="modal-dialog" @click.stop>
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Delete Service</h5>
          <button
            type="button"
            class="btn-close"
            @click="closeDeleteModal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete this service?</p>
        </div>
        <div class="modal-footer">
          <!-- Confirm deletion button -->
          <button @click="confirmDelete" class="btn btn-danger">Delete</button>
          <!-- Cancel button to close the popup -->
          <button @click="closeDeleteModal" class="btn btn-secondary">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "DeleteService",
  props: {
    selectedService: Object,
  },
  emits: ["delete-services"],
  data() {
    return {
      showDeleteModal: false,
    };
  },
  methods: {
    openDeleteModal(service) {
      this.showDeleteModal = true;
    },

    closeDeleteModal() {
      this.showDeleteModal = false;
    },
    async confirmDelete() {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.delete(
          `services/${this.selectedService.id}/`
        );
        this.$emit("delete-services", this.selectedService.id);
        this.closeDeleteModal();
      } catch (error) {
        console.error("Error deleting service:", error);
      }
      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>

<style>
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
