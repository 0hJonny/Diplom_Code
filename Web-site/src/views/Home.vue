<script setup lang="ts">
import Header from "../components/Header.vue";
import ArticlesList from "../components/ArticlesList.vue";
import TitleHeader from "../components/TitleHeader.vue";
</script>

<template>
  <div class="w-full h-full">
    <Header />
    <TitleHeader titleHeader="it news" />
  </div>
  <div class="container mx-auto p-4">
    <ArticlesList />
  </div>
</template>

<style scoped></style>
