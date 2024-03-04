<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-lg-6">
        <!-- Heading and Subheading -->
        <div class="text-center mb-4">
          <h2 class="display-4 text-success">Add Customer</h2>
          <p class="lead">Provide details to add a new customer.</p>
        </div>

        <!-- Customer Form -->
        <form @submit.prevent="submitForm">
          <!-- Customer Name inputs -->
          <div class="form-outline mb-4">
            <label class="form-label" for="first_name">First Name</label>
            <input
              v-model="first_name"
              type="text"
              id="first_name"
              placeholder="Enter the Customer's First name..."
              class="form-control"
              pattern="[a-zA-Z]{1,25}"
              oninvalid="this.setCustomValidity('Please enter the customer\'s first name.')"
              oninput="setCustomValidity('')"
              required
            />
          </div>

          <!-- Last Name input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="last_name">Last Name</label>
            <input
              v-model="last_name"
              type="text"
              id="last_name"
              placeholder="Enter the Customer's last name..."
              class="form-control"
              required
              pattern="[a-zA-Z]{1,25}"
              oninvalid="this.setCustomValidity('Please enter the customer\'s last name.')"
              oninput="setCustomValidity('')"
            />
          </div>

          <!-- Customer Address input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="address">City</label>
            <select
              v-model="address"
              id="address"
              class="form-select form-select-sm"
              oninvalid="this.setCustomValidity('Please select a city.')"
              oninput="setCustomValidity('')"
              required
            >
              <option value="" disabled selected>Select a city</option>
              <option v-for="city in cities" :key="city" :value="city">
                {{ city }}
              </option>
            </select>
          </div>

          <!-- Phone Number input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="phone_number">Phone number</label>
            <div class="input-group">
              <span class="input-group-text">+970</span>
              <input
                v-model="phone_number"
                type="tel"
                id="phone_number"
                placeholder="e.g., 551936142"
                pattern="[0-9]{9}"
                oninvalid="this.setCustomValidity('Please enter a valid phone number.')"
                oninput="setCustomValidity('')"
                class="form-control"
                required
              />
              <div class="invalid-feedback">
                Please enter a valid phone number.
              </div>
            </div>
          </div>

          <!-- Submit button -->
          <button type="submit" class="btn btn-success btn-block mb-4">
            Add Customer
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "vue3-toastify";
import axiosAuthMixin from "../../mixins/axiosAuthMixin.js";

export default {
  name: "AddCustomer",
  mixins: [axiosAuthMixin],
  data() {
    return {
      first_name: "",
      last_name: "",
      address: "",
      phone_number: null,
      isSubmitForm: false,
      cities: [
        "Gaza",
        "Nablus",
        "Quds",
        "Al-Khalil",
        "Ramallah",
        "Bethlehem",
        "Tulkarem",
        "Jinen",
      ],
    };
  },
  methods: {
    async submitForm() {
      // Set a flag to indicate form submission is in progress
      this.isSubmitForm = true;
      this.$store.commit("setIsLoading", true);

      // Create a new customer object with the form data
      const newCustomer = {
        first_name: this.first_name,
        last_name: this.last_name,
        address: this.address,
        phone_number: this.phone_number,
      };

      try {
        // Make a POST request to add the new customer
        const response = await axios.post("customers/", newCustomer);

        console.log("Customer added successfully:", response.data);
        toast.success("Customer added successfully!", {
          autoClose: 1000,
        });

        // Redirect to the customers page
        this.$router.push("/dashboard/customers");
      } catch (error) {
        // Handle different error scenarios
        if (error.response && error.response.status === 400) {
          toast.error("Phone number already in use.", {
            autoClose: 1000,
          });
        } else {
          toast.error("Something went wrong. Please try again.", {
            autoClose: 1000,
          });
        }
        console.error("Error adding customer:", error);
      } finally {
        // Reset the flag and set loading state to false
        this.isSubmitForm = false;
        this.$store.commit("setIsLoading", false);
      }
    },
  },
};
</script>

<style>
/* Add your custom styles here */
select {
  margin-top: -3px;
  background-color: white;
  height: 30px;
}
</style>
