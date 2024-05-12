<script setup lang="ts">
import { onMounted, watch } from "vue";

const switchTheme = () => {
  if (localStorage.theme === "dark") {
    document.documentElement.classList.remove("dark");
    localStorage.theme = "light";
  } else {
    document.documentElement.classList.add("dark");
    localStorage.theme = "dark";
  }
};

onMounted(() => {
  if (localStorage.theme === "dark") {
    document.documentElement.classList.add("dark");
  }
});
</script>

<template>
  <div class="dark-switcher">
    <button
      @click="switchTheme"
      class="group theme-switcher-light dark:theme-switcher-dark relative"
    >
      <div
        class="theme-switcher-icon group-hover:scale-110 absolute bg-white rounded-full z-10 dark:translate-x-10 dark:bg-black transition-all"
      />
      <img class="theme-switcher-icon" src="/moon.svg" alt="moon-theme-icon" />
      <img class="theme-switcher-icon" src="/sun.svg" alt="sun-theme-icon" />
    </button>
  </div>
</template>
