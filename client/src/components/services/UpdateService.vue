<template>
  <!-- Edit Service Button -->
  <button
    @click="openEditModal(service)"
    class="btn btn-primary btn-sm me-1 mb-1 btn-with-icon"
  >
    <AkEdit class="icon" style="font-size: 18px" />
  </button>

  <!-- Overlay for the Edit Service Modal -->
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
    <!-- Modal Dialog -->
    <div class="modal-dialog modal-dialog-centered modal-lg" @click.stop>
      <div class="modal-content">
        <!-- Modal Header -->
        <div class="modal-header">
          <h5 class="modal-title" id="editServiceModalLabel">Edit Service</h5>
          <button
            type="button"
            class="btn-close"
            @click="closeEditModal"
            aria-label="Close"
          ></button>
        </div>

        <!-- Modal Body with Edit Form -->
        <div class="modal-body">
          <form @submit.prevent="submitEditForm">
            <!-- Service Name Input -->
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
                minlength="1"
                maxlength="25"
                oninvalid="this.setCustomValidity('Please enter the service\'s name.')"
                oninput="setCustomValidity('')"
              />
            </div>

            <!-- Description Textarea -->
            <div class="mb-3">
              <label for="editServiceDescription" class="form-label"
                >Description</label
              >
              <textarea
                v-model="selectedService.description"
                class="form-control"
                id="editServiceDescription"
                pattern="[a-zA-Z]{1,255}"
                oninvalid="this.setCustomValidity('Please enter the service\'s description.')"
                oninput="setCustomValidity('')"
                rows="3"
                required
              ></textarea>
            </div>

            <!-- Price Input -->
            <div class="mb-3">
              <label for="editServicePrice" class="form-label">Price</label>
              <input
                v-model="selectedService.price"
                type="number"
                class="form-control"
                id="editServicePrice"
                step="0.01"
                min="0"
                max="10000"
                oninvalid="this.setCustomValidity('Please enter a valid service price. 2 max decimals')"
                oninput="setCustomValidity('')"
                required
              />
            </div>

            <!-- Duration Input -->
            <div class="mb-3">
              <label for="editServiceDuration" class="form-label"
                >Duration (in months)</label
              >
              <input
                v-model="selectedService.duration_months"
                type="number"
                class="form-control"
                id="editServiceDuration"
                min="1"
                max="120"
                oninvalid="this.setCustomValidity('Please enter a valid service duration. Up to a max of 10 years i.e., 120 months.')"
                oninput="setCustomValidity('')"
                required
              />
            </div>

            <!-- Add other form fields as needed -->

            <!-- Save Changes Button -->
            <button type="submit" class="btn btn-primary">Save Changes</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { AkEdit } from "@kalimahapps/vue-icons";
import { toast } from "vue3-toastify";

export default {
  name: "UpdateService",
  components: {
    AkEdit,
  },
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
    // Open the Edit Service Modal
    openEditModal(service) {
      this.showEditModal = true;
    },

    // Close the Edit Service Modal
    closeEditModal() {
      this.showEditModal = false;
    },

    // Submit the Edit Service Form
    async submitEditForm() {
      this.$store.commit("setIsLoading", true);
      try {
        // Send a PUT request to update the service
        const response = await axios.put(
          `services/${this.selectedService.id}/`,
          this.selectedService
        );
        // Emit the event to notify parent components about the update
        this.$emit("update-services", response.data);

        // Close the Edit Service Modal
        this.closeEditModal();
      } catch (error) {
        // Handle errors and show a toast message
        toast.error("Something went wrong. Please try again.", {
          autoClose: 1000,
        });
        console.error("Error updating service:", error);
      }
      // Set loading state to false after the operation
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
