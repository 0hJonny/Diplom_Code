<script setup lang="ts">
import { RouterView } from "vue-router";
import Footer from "./components/Footer.vue";
</script>

<template>
  <div class="main-page bg-bkg">
    <RouterView />
    <div class="container mx-auto p-4">
      <Footer />
    </div>
  </div>
</template>

<style scoped></style>
