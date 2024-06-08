<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import Home from "./views/Home.vue";
import Footer from "./components/Footer.vue";

import { ref, onMounted } from "vue";
import { supportedLanguages } from "@/utils/supportedLanguages.js";

const defaultLanguage = ref<string>(
  localStorage.getItem("lang") || navigator.language.split("-")[0] || "en"
); // Default language

onMounted(() => {
  const storedLanguage = localStorage.getItem("lang");
  const lang = supportedLanguages[defaultLanguage.value]
    ? defaultLanguage.value
    : "en";
  if (!storedLanguage) {
    localStorage.setItem("lang", lang);
  }
  document.documentElement.setAttribute("lang", lang);
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
