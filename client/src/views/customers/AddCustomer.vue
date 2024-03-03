<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-lg-6">
        <div class="text-center mb-4">
          <h2 class="display-4 text-success">Add Customer</h2>
          <p class="lead">Provide details to add a new customer..</p>
        </div>
        <form @submit.prevent="submitForm">
          <!-- Customer Name input -->
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
          <!-- Last name input -->
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
              required
            >
              <option value="" disabled selected>Select a city</option>
              <option value="Nablus">Nablus</option>
              <option value="Haifa">Haifa</option>
              <option value="Al-Khalil">Al-Khalil</option>
              <option value="Ramallah">Ramallah</option>
              <option value="Bethlehem">Bethlehem</option>
              <option value="Tulkarem">Tulkarem</option>
              <option value="Gaza">Gaza</option>
              <option value="Jinen">Jinen</option>
            </select>
            <div class="invalid-feedback">Please select a city.</div>
          </div>

          <!-- Phone number input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="phone_number">Phone number</label>
            <div class="input-group">
              <span class="input-group-text">+970</span>
              <input
                v-model="phone_number"
                type="tel"
                id="phone_number"
                placeholder="i.e 551936142"
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
    };
  },
  methods: {
    async submitForm() {
      console.log(this.isSubmitForm);
      this.isSubmitForm = true;
      this.$store.commit("setIsLoading", true);

      const newCustomer = {
        first_name: this.first_name,
        last_name: this.last_name,
        address: this.address,
        phone_number: this.phone_number,
      };

      await axios
        .post("customers/", newCustomer)
        .then((response) => {
          console.log("Service added successfully:", response.data);
          toast.success("Service added successfuly!", {
            autoClose: 1000,
          });
          this.$router.push("/dashboard/customers");
          // Optionally, you can redirect to the services page or perform other actions.
        })
        .catch((error) => {
          if (error.response.status === 400) {
            toast.error("Phone number already in use.", {
              autoClose: 1000,
            });
          } else {
            toast.error("Something went wrong. Please try again.", {
              autoClose: 1000,
            });
          }
          console.error("Error adding customer:", error);
        });
      this.$store.commit("setIsLoading", false);
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
