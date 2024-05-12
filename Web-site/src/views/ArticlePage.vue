<script setup lang="ts">
import { marked } from "marked"; //marked from "marked";
import { ref, computed, onMounted, watch } from "vue";

import Header from "../components/Header.vue";
import ArticlesList from "../components/ArticlesList.vue";
import TitleHeader from "../components/TitleHeader.vue";
import urls from "@/utils/urls";
import { useRoute, useRouter } from "vue-router";
import { languageLocales } from "@/utils/languageLocales";
import { mapToArticle, type Article } from "@/models";
import service from "@/utils/https";

const router = useRouter();
const route = useRoute();

const article = ref<Article>();

const markdownToHtml = computed(() =>
  marked.parse(article.value?.content || "")
);

async function loadArticle() {
  try {
    // Получаем данные от сервиса
    const { data: rawData } = await service.get(
      `${urls.articles_detail}?article_id=${route.params.id}&language_code=${languageLocales[document.documentElement.getAttribute("lang") || "en"]}`
    );

    // Преобразуем данные в объекты типа Article
    article.value = mapToArticle(rawData);
    console.log("article.value: ", article.value);

    // Обновляем значение реактивной переменной articles

    // Выводим полученные статьи
  } catch (error) {
    // Обрабатываем ошибку, если она возникла
    if (error) {
      router.push({ name: "not-found" });
    } else {
      console.error(error);
    }
  }
}

watch(
  () => route.params.id,
  async (newValue, oldValue) => {
    if (newValue !== oldValue) {
      // При изменении страницы загружаем статьи
      await loadArticle();
    }
  }
);

onMounted(async () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
  await loadArticle();
});
</script>

<template>
  <div id="header" class="w-full h-full">
    <Header />
  </div>
  <div v-if="article" class="container mx-auto">
    <div class="content">
      <div class="recomendation border-2 border-slate-300">
        <div>
          <h4>Recomendation</h4>
        </div>
      </div>
      <div class="card">
        <div v-if="1" class="title">
          <pre>{{ article.publishedDate }}</pre>
        </div>
        <h3>{{ article.title }}</h3>
        <img
          :src="article.imageSource"
          class="dark:shadow-violet-900 rounded-xl shadow-lg"
        />
        <div id="context" class="context">
          <!-- {{ markdown }} -->
          <div v-html="markdownToHtml"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  position: static;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 0px 32px 0px 32px;
  margin-top: 30px;
  scrollbar-width: thin;
  scrollbar-color: var(--color-scrollbar-thumb) var(--color-scrollbar-track);
}
.content {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 0px;
}
.recomendation {
  color: var(--color-text-primary);
  width: 400px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  max-width: min(100vw / 5, 100%);
  margin: 0px 64px;
}

.recomendation h4 {
  margin: 0px;
  color: var(--color-text-primary);
  font-size: 16px;
  font-weight: 600;
  line-height: 20px;
  letter-spacing: 0%;
  text-align: left;
}

.card {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 0px;
  margin: 0px 32px;
}

.card img {
  max-width: 100%; /* or stock image size */
  height: auto;
  margin: 0px;
  border-radius: 12px;
  margin-bottom: 12px;
}

.title {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 0px;

  color: var(--color-text-title);
  font-size: 14px;
  font-weight: 600;
  line-height: 20px;
  letter-spacing: 0%;
  text-align: left;
}

.context {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 0px;
  margin: 32px 0px;
  color: var(--color-text-primary);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 0px;
  flex: none;
  order: 27;
  align-self: stretch;
  flex-grow: 0;
  margin: 12px 0px;
}

.context >>> h3 {
  font-size: 18px;
  font-weight: 700;
  line-height: 24px;
  letter-spacing: 0%;
  text-align: left;
  flex: none;
  order: 14;
  align-self: stretch;
  flex-grow: 0;
  margin: 12px 0px;
}

.context >>> p {
  font-size: 16px;
  font-weight: 400;
  line-height: 24px;
  letter-spacing: 0%;
  text-align: left;
}

.context >>> li:not(:has(> p))::before {
  content: "•";
  margin-right: 8px;
  color: var(--color-text-secondary);
}

.card h3 {
  /* Heading and icon */
  width: 100%;
  color: var(--color-text-primary);
  font-size: 36px;
  font-weight: 700;
  line-height: 32px;
  letter-spacing: 0%;
  text-align: left;

  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 0px;

  margin: 32px 0px;
}
</style>
