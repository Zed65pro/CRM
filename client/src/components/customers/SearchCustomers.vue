<!-- SearchCustomers.vue -->

<template>
  <div
    class="mb-3 d-flex flex-column align-items-center justify-content-center"
  >
    <div class="d-flex mb-3">
      <!-- Search Input -->
      <input
        @input="$emit('update-search-query', $event.target.value)"
        @keyup.enter="fetchCustomers"
        type="text"
        class="form-control me-1"
        placeholder="Search..."
        style="width: 300px"
        id="searchCustomer"
      />

      <!-- Filter Dropdown -->
      <div class="dropdown">
        <button
          class="btn btn-secondary dropdown-toggle"
          type="button"
          id="filterDropdown"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          Filter
        </button>
        <ul class="dropdown-menu" aria-labelledby="filterDropdown">
          <li
            :class="{ active: filterType === 'first_name' }"
            @click="setFilter('first_name')"
            class="dropdown-item"
          >
            Search by First Name
          </li>
          <li
            :class="{ active: filterType === 'last_name' }"
            @click="setFilter('last_name')"
            class="dropdown-item"
          >
            Search by Last Name
          </li>

          <li
            :class="{ active: filterType === 'phone_number' }"
            @click="setFilter('phone_number')"
            class="dropdown-item"
          >
            Search by Phone number
          </li>
          <li
            :class="{ active: filterType === 'address' }"
            @click="setFilter('address')"
            class="dropdown-item"
          >
            Search by Address
          </li>
          <li
            :class="{ active: filterType === 'service' }"
            @click="setFilter('service')"
            class="dropdown-item"
          >
            Search by Service
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchCustomers",
  props: {
    filterType: String,
  },
  emits: ["fetch-customers", "set-filter", "update-search-query"],
  methods: {
    setFilter(filterType) {
      this.$emit("set-filter", filterType);
    },
    fetchCustomers() {
      this.$emit("fetch-customers");
    },
  },
};
</script>

<style>
/* Add your custom styles here */
</style>
