<template>
  <div class="container mt-5">
    <!-- Character rendering effect (fancy) -->
    <h2 class="fw-bold">
      {{ animatedWelcomeMessage }}
    </h2>

    <div class="mt-5">
      <h3 class="mb-3">About us</h3>
      <p>
        Our Customer Relationship Manager (CRM) application provides a seamless
        experience for managing customer data, services, and employee
        activities. Users can log in, search, add, edit, and delete customers
        with ease. Additionally, the system enables the management of customer
        services, including adding new services, stopping services, and listing
        active services. Super admins have the privilege of adding new services
        to the company and viewing a comprehensive list of customers with their
        active services.
      </p>
    </div>

    <!-- Section 1: Customer Management -->
    <div class="mt-5 py-4">
      <h3 class="mb-3">Customer Management</h3>
      <ul class="list-unstyled d-flex justify-content-center">
        <li class="me-3">
          <router-link
            :to="{
              name: 'Customers',
            }"
            class="btn btn-outline-primary"
            >View Customers
          </router-link>
        </li>
        <li>
          <router-link
            :to="{ name: 'AddCustomer' }"
            class="btn btn-outline-success"
            >Add Customer</router-link
          >
        </li>
      </ul>
    </div>

    <!-- Section 2: Services Management -->
    <div class="mt-5">
      <h3 class="text mb-3">Services Management</h3>
      <ul class="list-unstyled d-flex justify-content-center">
        <li class="me-3">
          <router-link
            :to="{ name: 'Services' }"
            class="btn btn-outline-primary"
            >View Services</router-link
          >
        </li>
        <li>
          <router-link
            v-if="$store.state.user.is_staff"
            :to="{ name: 'AddService' }"
            class="btn btn-outline-success"
            >Add Service</router-link
          >
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axiosAuthMixin from "../mixins/axiosAuthMixin.js";
export default {
  name: "Dashboard",
  data() {
    return {
      welcomeMessage: "Welcome, " + this.$store.state.user.username,
      animatedWelcomeMessage: "",
    };
  },
  mixins: [axiosAuthMixin],
  mounted() {
    // Fancy character rendering effect
    document.title = "CRM | Dashboard";
    this.animateWelcomeMessage();
  },
  methods: {
    animateWelcomeMessage() {
      const welcomeChars = this.welcomeMessage.split("");
      let animatedMessage = "";
      let delay = 0;

      welcomeChars.forEach((char) => {
        setTimeout(() => {
          animatedMessage += char;
          this.animatedWelcomeMessage = animatedMessage;
        }, delay);
        delay += 100; // Adjust the delay as needed
      });
    },
  },
};
</script>

<style scoped>
/* Add custom styles here */
/* Adjust color theme */
.text-primary {
  color: #007bff;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
}

.btn-success {
  background-color: #28a745;
  color: #fff;
}

/* Add more styles as needed */
</style>
