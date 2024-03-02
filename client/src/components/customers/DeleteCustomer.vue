<!-- DeleteCustomer.vue -->
<template>
  <button @click="showConfirmation" class="btn btn-danger btn-sm">
    Delete
  </button>

  <div v-if="showPopup" class="overlay" @click="cancelDelete"></div>
  <!-- Confirmation Popup Modal -->
  <div
    v-if="showPopup"
    class="modal fade show"
    style="display: block"
    @click="cancelDelete"
  >
    <div class="modal-dialog" @click.stop>
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Delete Customer</h5>
          <button
            type="button"
            class="btn-close"
            @click="cancelDelete"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete this customer?</p>
        </div>
        <div class="modal-footer">
          <!-- Confirm deletion button -->
          <button @click="confirmDelete" class="btn btn-danger">Delete</button>
          <!-- Cancel button to close the popup -->
          <button @click="cancelDelete" class="btn btn-secondary">
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
  name: "DeleteCustomer",
  props: {
    customer: Object,
    fetchCustomers: Function,
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
        // Send DELETE request to delete the customer
        await axios.delete(`customers/${this.customer.id}`);
        // Close the popup after deletion
        this.showPopup = false;
        this.$router.push({ name: "Customers" });
        this.fetchCustomers();
        // Optionally, redirect to the customer list page or perform other actions
      } catch (error) {
        console.error("Error deleting customer:", error);
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
