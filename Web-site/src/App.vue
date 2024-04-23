<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import Home from "./views/Home.vue";
import Footer from "./components/Footer.vue";

import { ref, onMounted } from "vue";
import { supportedLanguages } from "@/utils/supportedLanguages.ts";

const defaultLanguage = ref<string>(navigator.language.split("-")[0] || "en"); // Default language

onMounted(() => {
  document.documentElement.setAttribute(
    "lang",
    supportedLanguages[defaultLanguage.value] ? defaultLanguage.value : "en"
  );
});
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
