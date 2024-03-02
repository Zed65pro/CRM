<!-- DeleteService.vue -->
<template>
  <div>
    <button
      @click="showConfirmation"
      class="btn btn-danger btn-with-icon btn-sm"
    >
      <BsTrashFill style="font-size: 22px" />
    </button>

    <!-- Confirmation Popup Modal -->
    <div v-if="showPopup" class="overlay" @click="cancelDelete"></div>
    <div
      v-if="showPopup"
      class="modal fade show"
      style="display: block"
      @click="cancelDelete"
    >
      <div class="modal-dialog" @click.stop>
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Delete Service</h5>
            <button
              type="button"
              class="btn-close"
              @click="cancelDelete"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <p>
              Are you sure you want to remove this service from the customer?
            </p>
          </div>
          <div class="modal-footer">
            <!-- Confirm deletion button -->
            <button @click="confirmDelete" class="btn btn-danger">
              Delete
            </button>
            <!-- Cancel button to close the popup -->
            <button @click="cancelDelete" class="btn btn-secondary">
              Cancel
            </button>
          </div>
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
  name: "DeleteCustomerService",
  components: {
    BsTrashFill,
  },
  props: {
    service_id: Number,
    fetchCustomerDetails: Function,
  },
  data() {
    return {
      showPopup: false,
    };
  },
  methods: {
    showConfirmation() {
      this.showPopup = true;
    },
    async confirmDelete() {
      this.$store.commit("setIsLoading", true);
      try {
        // Send PATCH request to disassociate the service from the customer
        await axios.patch(
          `customers/${this.$route.params.id}/remove-service/${this.service_id}`
        );
        this.fetchCustomerDetails(this.$route.params.id);
        // Close the popup after disassociation
        this.showPopup = false;
        // Optionally, you can update the local data or perform other actions
      } catch (error) {
        toast.error("Something went wrong. Please try again.", {
          autoClose: 1000,
        });
        console.error("Error removing service from customer:", error);
      }
      this.$store.commit("setIsLoading", false);
    },
    cancelDelete() {
      // Close the popup if canceled
      this.showPopup = false;
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
