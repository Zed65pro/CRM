<template>
  <div
    class="loading-overlay"
    :style="{ display: $store.state.isLoading ? 'flex' : 'none' }"
  >
    <div class="loading-circle"></div>
  </div>
</template>

<script>
export default {
  name: "Loading",
};
</script>

<style>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.7); /* Semi-transparent white background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Ensure the overlay is on top of other elements */
}

.loading-circle {
  border: 8px solid #f3f3f3; /* Light gray border */
  border-top: 8px solid #3498db; /* Blue border for animation */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite; /* Spin animation */
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
