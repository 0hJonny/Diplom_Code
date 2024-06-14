<script setup lang="ts">
import { onBeforeUnmount, onMounted, watch } from "vue";
import { useRouter } from "vue-router";

import Header from "../components/Header.vue";
import ArticlesList from "../components/ArticlesListPage.vue";
import TitleHeader from "../components/TitleHeader.vue";
import WebSearchBar from "../components/WebSearchBar.vue";
import PaginationVue from "../components/Pagination.vue";
</script>

<template>
  <div class="w-full h-full">
    <Header />
    <TitleHeader titleHeader="Search" />
  </div>
  <div class="container mx-auto p-4">
    <div class="px-8"></div>
    <WebSearchBar />
  </div>
</template>

<style scoped>
.search__form {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 50vh;
}

.search__input {
  width: 60%;
  padding: var(--space-m);
  font-size: var(--text-size-regular);
  border-radius: 25px;
  border: 1px solid var(--color-text-secondary);
  transition: border-color 0.3s;
}

.search__input:focus {
  border-color: var(--color-palette-main);
}

.search__button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  color: var(--color-text-primary);
  background-color: var(--color-white);
  border: none;
  border-radius: 25px;
  transition: background-color 0.3s;
}

.search__button:hover {
  background-color: var(--color-palette-main);
}
</style>
