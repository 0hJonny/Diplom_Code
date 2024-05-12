<script setup lang="ts">
import { marked } from "marked";
import { ref, computed } from "vue";
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
  router.push({ name: "article", params: { id: props.article.id } });
};
</script>
<template>
  <div class="article-card-body flex flex-col">
    <img
      @click="routeToArticle"
      class="article-card-image"
      :src="article.imageSource"
      alt="article-image"
    />
    <div>
      <div class="card-meta flex gap-1 font-semibold text-sm text-violet-700">
        <h3 class="card-meta-author">{{ article.category }}</h3>
        <h3 class="card-meta-separator">•</h3>
        <h3 class="card-meta-date">{{ article.publishedDate }}</h3>
      </div>
      <div
        @click="routeToArticle"
        class="article-card-title flex justify-between"
      >
        <h2>{{ article.title }}</h2>
        <img
          class="invert dark:invert-0"
          src="/arrow-up-right.svg"
          alt="arrow-icon"
        />
      </div>
      <div>
        <p
          class="font-normal text-base text-slate-600 article-truncate-lines-2 line-clamp-3"
        >
         <!-- {{ markdown }} -->
         <div v-html="markdownToHtml"></div>
        </p>
      </div>
    </div>
    <div class="article-card-footer flex flex-wrap gap-2 mt-2">
      <ArticleTag
        v-for="(tag, index) in article.tags"
        :key="index"
        :tag="tag"
      />
    </div>
  </div>
</template>
<!-- ../models/index -->

<style scoped>



</style>
