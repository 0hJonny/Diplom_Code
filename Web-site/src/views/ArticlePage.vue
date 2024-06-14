<script setup lang="ts">
import { marked } from "marked"; //marked from "marked";
import { ref, computed, onMounted, watch, onBeforeUnmount } from "vue";

import Header from "../components/Header.vue";
import ArticlesList from "../components/ArticlesListPage.vue";
import TitleHeader from "../components/TitleHeader.vue";
import urls from "@/utils/urls";
import ArticleTag from "@/components/ArticleTag.vue";
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

function openSourceLink(url: string) {
  window.open(url, "_blank");
}
// Загружаем статью
async function loadArticle() {
  try {
    // Получаем данные от сервиса
    const { data: rawData } = await service.get(
      `${urls.articles_detail}?article_id=${route.params.id}&language_code=${languageLocales[document.documentElement.getAttribute("lang") || "en"]}`
    );

    // Преобразуем данные в объекты типа Article
    article.value = mapToArticle(rawData);
    if (article.value.id === "") {
      router.push({ name: "not-found" });
    }
    // console.log("article.value: ", article.value);

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

// Следим за изменениями атрибута языка на html и обновляем реактивную переменную lang при изменении

const observer = new MutationObserver((mutationsList) => {
  for (const mutation of mutationsList) {
    if (mutation.type === "attributes" && mutation.attributeName === "lang") {
      // При изменении языка загружаем статьи
      loadArticle();
    }
  }
});

const config = { attributes: true };
observer.observe(document.documentElement, config);

onBeforeUnmount(() => {
  observer.disconnect();
});
</script>

<template>
  <div id="header" class="w-full h-full">
    <Header />
  </div>
  <div v-if="article" class="container mx-auto">
    <div class="content">
      <div class="recomendation">
        <div class="mb-4">
          <h4>Recomendation</h4>
        </div>
        <ArticlesList
          class="mb-4"
          :sideBar="true"
          :ignoreArticle="article.id"
          :pagesData="{ currentPage: 1, elementsPerPage: 4 }"
        />
      </div>

      <!-- Article -->
      <div class="card">
        <div class="title">
          <pre>{{ article.publishedDate }}</pre>
        </div>
        <h3>{{ article.title }}</h3>
        <img
          :src="article.imageSource"
          class="dark:shadow-violet-900 rounded-xl shadow-lg w-full"
        />
        <!-- Container -->
        <div class="justify-between flex w-full">
          <!-- {{ article.neuralNetworks }} -->
          <div class="tags-container-neural">
            <div class="tags">
              <div
                v-for="(tag, key) in article.neuralNetworks"
                :key="key"
                class="tag-popup"
              >
                <div class="tooltip rounded-lg p-2">
                  {{ key }}
                </div>
                <ArticleTag :tag="tag" />
              </div>
            </div>
          </div>
          <!-- SourceUrl -->
          <div
            v-if="'article.sourceUrl'"
            class="tags-container-tag"
            @click="openSourceLink(article.sourceLink)"
          >
            <div class="tags">
              <div class="tag-popup">
                <div class="tooltip rounded-lg p-2 cursor-pointer">
                  {{ article.sourceLink }}
                </div>
                <ArticleTag :tag="'Source'" />
              </div>
            </div>
          </div>
        </div>
        <div id="context" class="context">
          <!-- {{ markdown }} -->
          <div v-html="markdownToHtml" />
          <div class="tags-container-tag">
            <div class="tags">
              <div v-for="(tag, key) in article.tags" :key="key">
                <ArticleTag :tag="tag" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tag-popup {
  position: relative;
  margin-right: 5px;
}

.tag-popup .tooltip {
  position: absolute;
  top: calc(100% + 5px);
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.3s;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  background-color: var(--color-text-title);
}
.tag-popup:hover .tooltip {
  opacity: 1;
  z-index: 1;
  display: block;
  visibility: visible;
  transition:
    opacity 0.3s,
    visibility 0s;
}
.tag-popup:not(:hover) .tooltip {
  opacity: 0;
  visibility: hidden;
  transition:
    opacity 0.3s,
    visibility 0.3s;
}
.tooltip {
  position: absolute;
  top: -100%;
  left: 50%;
  transform: translateX(-50%);
  color: var(--color-white);
  background-color: var(--color-text-title);
  text-overflow: ellipsis;
  /* white-space: nowrap; */
  /* overflow: hidden; */
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  opacity: 0;
  transition: opacity 0.3s;
}

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
  max-width: calc(2.5 / 5 * (100vw - 32px)); /* 3/5 of display size */
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

.tags {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 0px;
  margin: 16px 0px;
  gap: 10px;
}
</style>
