/* eslint-disable vue/multi-word-component-names */
<template>
  <div>
    <!-- Your template code here -->
    Hello
  </div>
</template>

<script>
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Home",
  data() {
    return {
      // Your data properties here
    };
  },
  methods: {
    // Your methods here
  },
  mounted() {
    // Your mounted hook code here
    this.$router.push({ name: "Customers" });
  },
};
</script>

<style scoped>
/* Your scoped styles here */
</style>
