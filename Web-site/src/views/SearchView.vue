<script setup lang="ts">
import { onBeforeUnmount, onMounted, reactive, watch } from "vue";
import { useRouter } from "vue-router";

import Header from "../components/Header.vue";
import ArticlesList from "../components/ArticlesListPage.vue";
import TitleHeader from "../components/TitleHeader.vue";
import WebSearchBar from "../components/WebSearchBar.vue";
import PaginationVue from "../components/Pagination.vue";
import router from "@/router";
onMounted(() => {
  document.title = "Search"
})
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
