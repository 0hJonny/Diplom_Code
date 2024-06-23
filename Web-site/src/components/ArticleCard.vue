<script setup lang="ts">
import { marked } from "marked";
import { computed } from "vue";
import { useRouter } from "vue-router";

import ArticleTag from "./ArticleTag.vue";
import type { Article } from "../models/index";

const props = withDefaults(defineProps<{ article: Article }>(), {
  /**
   * Returns an article object with author, published date, title, description, image link, tags, and content.
   *
   * @return {Object} The article object
   */
  article: () => {
    return {
      id: "40f0b678-2597-479f-b9f2-f34b35253660",
      title:
        "Предвзятое предсказательное патрулирование, финансируемое правительством США, говорят законодатели",
      publishedDate: "2024-04-29T13:12:42.095278Z",
      category: "technology",
      tags: [
        "Civil Rights",
        "Biased",
        "Policing",
        "Algorithms",
        "Discrimination"
      ],
      neuralNetworks: {
        translator: "",
        annotator: ""
      },
      content: `### Главные факты и события:

- Демократические политики требуют от правительства США прекратить финансирование систем предсказательной полиции из-за их предполагаемой склонности к предрассудкам и дискриминации.

- Эти системы были показаны преувеличивать преступность в чёрных и латинских районах на основании фальсифицированных алгоритмами.

- Системы часто питаются предрассудками, что приводит к дискриминаторным прогнозам.

- Департамент юстиции финансировал гранты на системы предсказательной полиции с 2009 года.

- ЕС недавно запретило использование систем предсказательной полиции.

### Ключевые идеи:

- Системы предсказательной полиции поддерживают расовую дискриминацию и предрассудки в практиках полицейской службы.

- Использование этих систем было показано, что увеличивает полицейское мучительство меньшинств.

- Правительство должно решать дискриминационные практики, заложенные в этих алгоритмах, и установить меры предосторожности для предотвращения их неправильного использования.

### Дальнейшие интересы:

- Статья выражает озабоченность более широким использованием технологий надзорной деятельности со стороны правительства.

- Отсутствие прозрачности и отчетности в развертывании этих технологий поднимают вопросы этики и прав человека.

### Ключевые слова:

- Предиктивная полиция
- Бias
- Дискриминация
- Алгоритм
- Данные сбора
- Закон о гражданских правах

### Выделенный текст:

"Нарастающая информация указывает на то, что технологии предсказательной полиции не сокращают преступность. Вместо этого они ухудшают равное обращение с гражданами цвета кожи со стороны правоохранительных органов."`,
      languageCode: "ru-RU",
      imageSource: "/images/40f0b678-2597-479f-b9f2-f34b35253660.png"
    };
  }
});
const router = useRouter();

const markdownToHtml = computed(() => {
  return marked(props.article.content);
});

const routeToArticle = () => {
  const currentLang = document.documentElement.getAttribute('lang') || 'en'
  router.push({
    name: "article",
    params: { id: props.article.id },
    query: { lang: currentLang }
  });
};
</script>

<template>
  <div class="article-card-container md:max-w-full max-w-lg mx-auto">
    <div class="article-card-container__inner">
      <img
        @click="routeToArticle"
        class="article-card-image"
        :src="article.imageSource"
        alt="article-image"
      />
      <div class="article-card-content">
        <div class="card-meta flex gap-1 font-semibold text-sm text-violet-700">
          <h3 class="card-meta-author">{{ article.category }}</h3>
          <h3 class="card-meta-separator">•</h3>
          <h3 class="card-meta-date">{{ article.publishedDate }}</h3>
        </div>
        <div
          @click="routeToArticle"
          class="article-card-title flex justify-between"
        >
          <h2 class="text-xl font-semibold">{{ article.title }}</h2>
          <img
            class="invert dark:invert-0"
            src="/arrow-up-right.svg"
            alt="arrow-icon"
          />
        </div>
        <div>
          <p class="font-normal text-base text-slate-600 article-truncate-lines-2 line-clamp-3">
           <!-- {{ markdown }} -->
           <div v-html="markdownToHtml"></div>
          </p>
        </div>
        <div class="article-card-footer tags__container">
          <div v-for="(tag, index) in article.tags" :key="index">
            <a :href="`/search?tag=${tag}`">
            <ArticleTag :tag="tag" />
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<!-- ../models/index -->

<style scoped>
.tags__container {
  display: flex;
  flex-wrap: wrap;
  /* justify-content: space-between; */
  gap: 0.5rem;
 margin-top: 1rem;
}
  @media (min-width: 768px) {
    h2 {
      font-size: min(1.2rem, calc(1.2vw + 1rem));
    }

    p {
      font-size: min(0.9rem, calc(0.9vw + 0.9rem));
    }

    .card-meta-author {
      font-size: min(0.7rem, calc(0.7vw + 0.7rem));
    }

    .card-meta-date {
      font-size: min(0.7rem, calc(0.7vw + 0.7rem));
    }
  }
</style>