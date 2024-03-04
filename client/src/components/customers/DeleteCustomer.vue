<!-- DeleteCustomer.vue -->
<template>
  <!-- Delete button -->
  <button @click="showConfirmation" class="btn btn-danger btn-with-icon btn-sm">
    <BsTrashFill style="font-size: 22px" />
  </button>

  <!-- Dark overlay when confirmation popup is displayed -->
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
        <!-- Modal Header -->
        <div class="modal-header">
          <h5 class="modal-title">Delete Customer</h5>
          <button
            type="button"
            class="btn-close"
            @click="cancelDelete"
            aria-label="Close"
          ></button>
        </div>

        <!-- Modal Body -->
        <div class="modal-body">
          <p>Are you sure you want to delete this customer?</p>
        </div>

        <!-- Modal Footer with Confirm and Cancel buttons -->
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
import { BsTrashFill } from "@kalimahapps/vue-icons";
import { toast } from "vue3-toastify";

export default {
  name: "DeleteCustomer",
  components: {
    BsTrashFill,
  },
  props: {
    customer: Object,
    fetchCustomers: Function,
  },
  emits: ["fetch-customers"],
  data() {
    return {
      showPopup: false,
    };
  },
  methods: {
    /**
     * Display the confirmation popup.
     */
    showConfirmation() {
      this.showPopup = true;
    },

    /**
     * Confirm the deletion and send a DELETE request to the backend.
     */
    async confirmDelete() {
      this.$store.commit("setIsLoading", true);
      try {
        // Send DELETE request to delete the customer
        await axios.delete(`customers/${this.customer.id}`);

        // Close the popup after deletion
        this.showPopup = false;

        // Navigate to the Customers page
        this.$router.push({ name: "Customers" });

        // Emit event to fetch updated customer list
        this.$emit("fetch-customers");

        // Optionally, redirect to the customer list page or perform other actions
      } catch (error) {
        toast.error("Something went wrong. Please try again.", {
          autoClose: 1000,
        });
        console.error("Error deleting customer:", error);
      } finally {
        this.$store.commit("setIsLoading", false);
      }
    },

    /**
     * Cancel the deletion and close the confirmation popup.
     */
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
