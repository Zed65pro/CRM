<template>
  <!-- Delete Service Popup -->
  <button
    @click="openDeleteModal(service)"
    class="btn btn-danger btn-with-icon btn-sm mb-1"
  >
    <BsTrashFill style="font-size: 18px" />
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
import { BsTrashFill } from "@kalimahapps/vue-icons";
import { toast } from "vue3-toastify";

export default {
  name: "DeleteService",
  components: {
    BsTrashFill,
  },
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
    // Open the delete modal
    openDeleteModal(service) {
      this.showDeleteModal = true;
    },

    // Close the delete modal
    closeDeleteModal() {
      this.showDeleteModal = false;
    },

    // Confirm the deletion of the service
    async confirmDelete() {
      this.$store.commit("setIsLoading", true);
      try {
        // Send a DELETE request to delete the service
        const response = await axios.delete(
          `services/${this.selectedService.id}/`
        );
        // Emit the event to notify parent components about the deletion
        this.$emit("delete-services", this.selectedService.id);
        // Close the delete modal
        this.closeDeleteModal();
      } catch (error) {
        // Handle errors and show a toast message
        toast.error("Something went wrong. Please try again.", {
          autoClose: 1000,
        });
        console.error("Error deleting service:", error);
      }
      // Set loading state to false after the operation
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
