<script setup lang="ts">
import { onMounted, ref, watch } from "vue";

import urls from "@/utils/urls";
import service from "@/utils/https";
import { languageLocales } from "@/utils/languageLocales";
import ArticleVue from "./ArticleCard.vue";
import { mapToArticle, type Article } from "../models/index";

const props = defineProps({
  ignoreArticle: {
    type: String,
    default: ""
  },
  sideBar: {
    type: Boolean,
    default: false
  },
  lang: {
    type: String,
    default: "en"
  },
  pagesData: {
    type: Object,
    default: () => ({
      currentPage: NaN,
      elementsPerPage: 16
    })
  }
});

const articles = ref<Article[]>([]);

onMounted(async () => {
  await loadArticles();
});

async function loadArticles() {
  try {
    // Получаем данные от сервиса
    const { data: rawData } = await service.get(
      `${urls.articles}?page=${props.pagesData.currentPage}&limit=${props.pagesData.elementsPerPage}&language_code=${languageLocales[document.documentElement.getAttribute("lang") || "en"]}`
    );

    if (rawData === null) {
      articles.value = [];
      return;
    }

    // Преобразуем данные в объекты типа Article
    const parsedData: Article[] = rawData.map((article: any) =>
      mapToArticle(article)
    );

    // Обновляем значение реактивной переменной articles
    articles.value = parsedData;

    if (props.ignoreArticle !== "") {
      articles.value = articles.value.filter(
        (article) => article.id !== props.ignoreArticle
      );
      articles.value = articles.value.slice(
        0,
        props.pagesData.elementsPerPage - 1
      );
    }

    // Выводим полученные статьи
  } catch (error) {
    // Обрабатываем ошибку, если она возникла
    console.error(error);
  }
}
watch(
  () => (props.lang, props.ignoreArticle),
  async (newValue, oldValue) => {
    if (newValue !== oldValue) {
      // При изменении языка загружаем статьи
      await loadArticles();
    }
  }
);

// Следим за изменениями currentPage и загружаем статьи при изменении
watch(
  () => props.pagesData.currentPage,
  async (newPage) => {
    // При изменении страницы загружаем статьи
    await loadArticles();
  }
);

watch(
  () => props.lang,
  async (newValue, oldValue) => {
    if (newValue !== oldValue) {
      // При изменении языка загружаем статьи
      await loadArticles();
    }
  }
);
</script>
<template>
  <div>
    <div
      v-if="articles.length"
      class="articles-container-bottom flex grid"
      :class="sideBar ? 'grid-cols-1' : 'grid-cols-3'"
    >
      <ArticleVue
        v-for="article in articles"
        class="article-card-body"
        :key="article.id"
        :article="article"
      />
    </div>
    <div v-else>
      <h2
        class="flex text-3xl font-semibold mb-8 text-center"
        :class="sideBar ? '' : 'mt-24'"
      >
        {{
          sideBar ? "No recomendations yet" : "No data for current language 😣"
        }}
      </h2>
    </div>
  </div>

  <!-- <div class="left-pagination-side">
          <img src="/arrow-left.svg" alt="arrow-icon" />
        </div>
        <div class="center-pagination-side">
          <span>Paginator</span>
        </div>
        <div class="right-pagination-side">
          <img src="/arrow-right.svg" alt="right-icon" />
        </div> -->
</template>
