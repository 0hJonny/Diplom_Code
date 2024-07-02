<script setup lang="ts">
import { onBeforeUnmount, onMounted, reactive, ref, watch } from "vue";
import { useRouter } from "vue-router";

import Header from "../components/Header.vue";
import ArticlesList from "../components/ArticlesListPage.vue";
import TitleHeader from "../components/TitleHeader.vue";
import PaginationVue from "../components/Pagination.vue";
import urls from "@/utils/urls";
import service from "@/utils/https";
import { languageLocales } from "@/utils/languageLocales";

const router = useRouter();

const pagesData = reactive({
  totalItems: 0,
  elementsPerPage: 12,
  currentPage: Number(router.currentRoute.value.query.page) || 1
});

const lang = ref(document.documentElement.getAttribute("lang") || "en");

watch(lang, async (newValue, oldValue) => {
  if (newValue !== oldValue) {
    // При изменении языка загружаем статьи
    await get_articles_count();
  }
});

// Следим за изменениями атрибута языка на html и обновляем реактивную переменную lang при изменении
onMounted(() => {
  const observer = new MutationObserver((mutationsList) => {
    for (const mutation of mutationsList) {
      if (mutation.type === "attributes" && mutation.attributeName === "lang") {
        lang.value = document.documentElement.getAttribute("lang") || "en";
      }
    }
  });

  const config = { attributes: true };
  observer.observe(document.documentElement, config);

  onBeforeUnmount(() => {
    observer.disconnect();
  });
});

onMounted(async () => {
  await get_articles_count();
});

// Следим за изменениями в router.currentRoute и обновляем currentPage при изменении query.page
watch(
  () => router.currentRoute.value.query.page,
  (newValue, oldValue) => {
    if (newValue !== oldValue) {
      // Обновляем currentPage в соответствии со значением из маршрута
      pagesData.currentPage = Number(newValue) || 1;
      // console.log("currentPage: ", pagesData.currentPage);
    }
  }
);

async function get_articles_count() {
  const { data }: any = await service.get(
    `${urls.articles_count}?language_code=${languageLocales[document.documentElement.getAttribute("lang") || "en"]}&category=technology`
  );
  pagesData.totalItems = data["count"];
  // console.log("pagesData.totalItems: ", pagesData.totalItems);
}
onMounted(() => {
  document.title = "Technology"
})
</script>

<template>
  <div class="w-full h-full">
    <Header />
    <TitleHeader titleHeader="Technology" />
  </div>
  <div class="container mx-auto p-4">
    <div class="articles-container">
      <div class="mb-8">
        <h2 class="font-semibold text-2xl">All blog posts</h2>
      </div>

      <div class="px-8">
        <ArticlesList :lang="lang" :pagesData="pagesData" category="technology" />
      </div>
      <div class="border-t-2 border-slate-300 p-9">
        <PaginationVue
          :totalItems="pagesData.totalItems"
          :elementsPerPage="pagesData.elementsPerPage"
          :currentPage="pagesData.currentPage"
        />
      </div>
    </div>
  </div>
</template>
