<script setup lang="ts">
import { onMounted, reactive, ref, watch } from "vue";
import { useRouter } from "vue-router";

import urls from "@/utils/urls";
import service from "@/utils/https";
import ArticleVue from "./Article.vue";
import PaginationVue from "./Pagination.vue";
import type { Article } from "../models/index";

const router = useRouter();

const pagesData = reactive({
  currentPage: Number(router.currentRoute.value.query.page) || 1,
  elementsPerPage: 12,
  totalItems: 400,
});

const articles = ref<Article[]>([]);

onMounted(async () => {
  await loadArticles();
  await get_articles_count();
});

async function get_articles_count() {
  const data: any = await service.get(`${urls.articles_count}`);
  pagesData.totalItems = data["count"];
  console.log("pagesData.totalItems: ", pagesData.totalItems);
}

async function loadArticles() {
  try {
    // Получаем данные от сервиса
    const rawData: any[] = await service.get(`${urls.articles}?page=${pagesData.currentPage}&limit=${pagesData.elementsPerPage}`);
    // console.log("currentPage: ", pagesData.currentPage);
    // Преобразуем данные в объекты типа Article
    const parsedData: Article[] = rawData.map((article: any) => ({
      id: article[0],
      title: article[1],
      publishedDate: article[2],
      imageLink: article[3],
      category: article[4],
      tags: article[5],
      content: article[6]
    }));

    // Обновляем значение реактивной переменной articles
    articles.value = parsedData;

    // Выводим полученные статьи
  } catch (error) {
    // Обрабатываем ошибку, если она возникла
    console.error(error);
  }
};

// Следим за изменениями currentPage и загружаем статьи при изменении
watch(() => pagesData.currentPage, async (newPage) => {
  // При изменении страницы загружаем статьи
  await loadArticles();
});

// Следим за изменениями в router.currentRoute и обновляем currentPage при изменении query.page
watch(() => router.currentRoute.value.query.page,
  (newValue, oldValue) => {
    if (newValue !== oldValue) {
      // Обновляем currentPage в соответствии со значением из маршрута
      pagesData.currentPage = Number(newValue) || 1; 
      console.log("currentPage: ", pagesData.currentPage);
    }
});

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
            v-for="(article) in articles"
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
