<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import Home from "./views/Home.vue";
import Footer from "./components/Footer.vue";
</script>

<template>
  <div class="main-page bg-bkg container">
    <RouterView />
    <Footer />
  </div>
</template>

<style scoped></style>
