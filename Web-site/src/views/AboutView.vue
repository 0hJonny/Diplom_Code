<template>
    <Header />
    <TitleHeader titleHeader="About" />
    <div class="container mx-auto py-8 px-10">
      <div class="flex flex-col gap-4">
        <p class="text-slate-300">
          This is a simple blog created with Vue.js, Vite, Tailwind CSS, and
          Go. The goal of this project is to practice these technologies and
          have a nice and clean blog.
        </p>
        <p class="text-slate-300">
          The blog is fully responsive and supports dark theme. The blog is
          multilingual (currently English and Russian are supported).
        </p>
        <p class="text-slate-300">
          Source code of this blog are available on
          <a class="link-ref" href="https://github.com/0hJonny/blog-vue" target="_blank">GitHub</a>
        </p>
      </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";

import Header from "../components/Header.vue";
import TitleHeader from "../components/TitleHeader.vue";
onMounted(() => {
  document.title = "About"
})
</script>

<style scoped>
p {
  color: var(--color-text-primary);
}
</style>
