<script setup lang="ts">
import { marked } from "marked"; //marked from "marked";
import { ref, computed, onMounted } from "vue";

import Header from "../components/Header.vue";
import ArticlesList from "../components/ArticlesList.vue";
import TitleHeader from "../components/TitleHeader.vue";

const markdown = ref(`### Главные факты и события:

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

"Нарастающая информация указывает на то, что технологии предсказательной полиции не сокращают преступность. Вместо этого они ухудшают равное обращение с гражданами цвета кожи со стороны правоохранительных органов."`);
const markdownToHtml = computed(() => marked.parse(markdown.value));

onMounted(() => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});
</script>

<template>
  <div id="header" class="w-full h-full">
    <Header />
  </div>
  <div class="container mx-auto">
    <div class="content">
      <div class="recomendation border-2 border-slate-300">
        <div>
          <h4>Recomendation</h4>
        </div>
      </div>
      <div class="card">
        <div v-if="1" class="title">
          <pre>Sunday , 1 Jan 2023</pre>
        </div>
        <h3>Article Title</h3>
        <img
          src="ImagePlace"
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
