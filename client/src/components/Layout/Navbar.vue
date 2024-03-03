<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light mb-3">
    <div class="container-fluid">
      <a
        class="navbar-brand fs-3 btn btn-outline-success"
        href="/dashboard"
        style="border: none"
        >CRM</a
      >
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item me-3 btn btn-light">
            <a class="nav-link active" aria-current="page" href="/dashboard"
              >Home</a
            >
          </li>
          <li class="nav-item me-3 btn btn-light">
            <a
              class="nav-link active"
              aria-current="page"
              href="/dashboard/customers"
              >Customers</a
            >
          </li>
          <li class="nav-item me-3 btn btn-light">
            <a
              class="nav-link active"
              aria-current="page"
              href="/dashboard/services"
              >Services</a
            >
          </li>
          <li
            v-if="$store.state.user && $store.state.user.is_staff"
            class="nav-item me-3 btn btn-light"
          >
            <a
              class="nav-link active"
              aria-current="page"
              href="/dashboard/add-service"
              >Add Service</a
            >
          </li>
        </ul>
        <div class="d-flex navbar-nav">
          <a
            v-if="!$store.state.token"
            href="/login"
            class="btn btn-outline-success me-2"
            >Login</a
          >
          <LogoutButton />
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import LogoutButton from "./LogoutButton";
export default {
  name: "Navbar",
  components: {
    LogoutButton,
  },
};
</script>

<style scoped>
/* Your CSS code here */
</style>
