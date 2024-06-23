<!-- <script setup lang="ts">
import { ref, onMounted, watch, reactive } from "vue";
import { useRouter } from "vue-router";

import urls from "@/utils/urls";
import service from "@/utils/https";
import { languageLocales } from "@/utils/languageLocales";
import { mapToArticle, type Article } from "@/models/index";
import ArticleCard from "./ArticleCard.vue";

const router = useRouter();

const input = ref("");
const status = ref("");
const articles = ref<Article[]>([]);

const pagesData = reactive({
  totalItems: 0,
  elementsPerPage: 12,
  currentPage: Number(router.currentRoute.value.query.page) || 1
});

const lang = ref(document.documentElement.getAttribute("lang") || "en");
watch(lang, async (newValue, oldValue) => {
  if (newValue !== oldValue) {
    // При изменении языка загружаем статьи
    await get_search();
  }
});

const inputTimeout = ref(null);
watch(input, (newValue, oldValue) => {
  if (inputTimeout.value) {
    clearTimeout(inputTimeout.value);
  }

  if (newValue) {
    inputTimeout.value = setTimeout(async () => {
      await get_search();
    }, 1000);
  }
});

async function get_search() {
  try {
    const response = await service.get(
      `${urls.search}?page=${pagesData.currentPage}&limit=${pagesData.elementsPerPage}&language_code=${languageLocales[document.documentElement.getAttribute("lang") || "en"]}&query=${input.value}`
    );
    console.log(response);
    if (response.data) {
      articles.value = response.data.map((article: any) =>
        mapToArticle(article)
      );
      console.log(articles.value);
      status.value = response.data.results;
    } else {
      articles.value = [];
      status.value = "failed";
    }
    console.log(articles.value);
  } catch (error) {
    console.error(error);
  }
}

onMounted(async () => {
  await get_search();
});
</script>

<template>
  <div class="search">
    <input
      type="text"
      v-model="input"
      placeholder="Search articles..."
      @keyup.enter="get_search"
    />
    <div
      class="card articles-container article-card-body"
      v-if="articles"
      v-for="article in articles"
      :key="article.id"
    >
      <ArticleCard :article="article" />
    </div>
    <div
      class="item error"
      v-if="
        (input && status === 'success' && articles.length === 0) ||
        status === 'failed'
      "
    >
      <p>No results found!</p>
    </div>
  </div>
</template>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Montserrat&display=swap");

* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  font-family: "Montserrat", sans-serif;
}

body {
  padding: 20px;
  min-height: 100vh;
  background-color: rgb(234, 242, 255);
}

.search {
  max-width: calc(2 / 5 * (100vw - 32px)); /* 3/5 of display size */
  margin: 0 auto;
}

input {
  display: block;
  width: 100%;
  margin: 20px 0;
  padding: 10px 45px;
  background: white url("assets/search-icon.svg") no-repeat 15px center;
  background-size: 15px 15px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  box-shadow:
    rgba(50, 50, 93, 0.25) 0px 2px 5px -1px,
    rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
}

.card {
  width: 100%;
  margin: 0 0 10px 0;
  padding: 20px;

  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;

  margin-bottom: 16px;
}

.item {
  width: 100%;
  margin: 0 0 10px 0;
  padding: 10px 20px;
  border-radius: 5px;
  background-color: var(--color-bkg);
  box-shadow: var(--color-text-title);

  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;

  margin-bottom: 10px;
}

.error {
  background-color: tomato;
}
</style> -->
