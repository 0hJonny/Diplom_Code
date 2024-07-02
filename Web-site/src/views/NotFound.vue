<script setup lang="ts">
import { onMounted } from "vue";
import Header from "../components/Header.vue";
onMounted(() => {
  document.title = "Oops..."
})
</script>

<template>
  <Header />
  <div class="container mx-auto mt-8">
    <div class="flex items-center justify-center">
      <h1 class="text-8xl font-bold text">4😴4</h1>
    </div>
    <div class="mt-4 flex items-center justify-center">
      <p class="text-3xl text">Page not found</p>
    </div>
  </div>
</template>

<style scoped>
.text {
  color: var(--color-text-primary);
}
</style>
