<script setup lang="ts">
const switchTheme = () => {
  // On page load or when changing themes, best to add inline in `head` to avoid FOUC
  if (
    localStorage.theme === "dark" ||
    (!("theme" in localStorage) &&
      window.matchMedia("(prefers-color-scheme: dark)").matches)
  ) {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }

  localStorage.theme = localStorage.theme === "dark" ? "light" : "dark";
};
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
