<script setup lang="ts">
import { onBeforeUnmount, onMounted, reactive, ref, watch } from "vue";
import { useRouter } from "vue-router";

import urls from "@/utils/urls";
import service from "@/utils/https";
import { languageLocales } from "@/utils/languageLocales";
import ArticleVue from "./Article.vue";
import PaginationVue from "./Pagination.vue";
import { mapToArticle, type Article } from "../models/index";

const router = useRouter();

const pagesData = reactive({
  currentPage: Number(router.currentRoute.value.query.page) || 1,
  elementsPerPage: 16,
  totalItems: 0
});

const lang = ref(document.documentElement.getAttribute("lang") || "en");
const articles = ref<Article[]>([]);

onMounted(async () => {
  await loadArticles();
  await get_articles_count();
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

async function get_articles_count() {
  const { data }: any = await service.get(
    `${urls.articles_count}?language_code=${languageLocales[document.documentElement.getAttribute("lang") || "en"]}`
  );
  pagesData.totalItems = data["count"];
  // console.log("pagesData.totalItems: ", pagesData.totalItems);
}

async function loadArticles() {
  try {
    // Получаем данные от сервиса
    const { data: rawData } = await service.get(
      `${urls.articles}?page=${pagesData.currentPage}&limit=${pagesData.elementsPerPage}&language_code=${languageLocales[document.documentElement.getAttribute("lang") || "en"]}`
    );

    // Преобразуем данные в объекты типа Article
    const parsedData: Article[] = rawData.map((article: any) =>
      mapToArticle(article)
    );

    // Обновляем значение реактивной переменной articles
    articles.value = parsedData;

    // Выводим полученные статьи
  } catch (error) {
    // Обрабатываем ошибку, если она возникла
    console.error(error);
  }
}

// Следим за изменениями currentPage и загружаем статьи при изменении
watch(
  () => pagesData.currentPage,
  async (newPage) => {
    // При изменении страницы загружаем статьи
    await loadArticles();
  }
);

watch(lang, async (newValue, oldValue) => {
  if (newValue !== oldValue) {
    // При изменении языка загружаем статьи
    await loadArticles();
    await get_articles_count();
  }
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
</script>
<template>
  <div class="articles-container">
    <div class="px-8">
      <div>
        <div class="mb-8">
          <h2 class="font-semibold text-2xl">All blog posts</h2>
        </div>
        <div class="articles-container-bottom">
          <ArticleVue
            v-for="article in articles"
            :key="article.id"
            :article="article"
          />
        </div>
      </div>
      <div class="border-t-2 border-slate-300 p-9">
        <PaginationVue
          :totalItems="pagesData.totalItems"
          :elementsPerPage="pagesData.elementsPerPage"
          :currentPage="pagesData.currentPage"
        />
        <!-- <div class="left-pagination-side">
          <img src="/arrow-left.svg" alt="arrow-icon" />
        </div>
        <div class="center-pagination-side">
          <span>Paginator</span>
        </div>
        <div class="right-pagination-side">
          <img src="/arrow-right.svg" alt="right-icon" />
        </div> -->
      </div>
    </div>
  </div>
</template>
