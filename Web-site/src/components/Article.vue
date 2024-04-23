<script setup lang="ts">
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
      id: "323132-32-3-14--3-453",
      title: "Example Article Title",
      publishedDate: "2022-01-01T12:00:00Z",
      imageLink: "https://example.com/example-article-image.jpg",
      category: "Example Category",
      tags: ["Tag 1", "Tag 2", "Tag 3"],
      languageCode: "en",
      content: `Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, justo ut convallis sollicitudin, magna diam tincidunt orci, ac vulputate purus turpis id est. Duis in lectus vel enim interdum lacinia. Nullam sed justo quis tortor ultrices malesuada. Sed at est sit amet odio mattis lacinia. Sed nec turpis quis purus lobortis consectetur. Sed varius, mauris vitae vulputate vehicula, est velit tincidunt eros, in porta leo felis id metus. Sed lacinia, purus id consectetur auctor, nunc magna pharetra ipsum, nec bibendum lorem turpis id diam.`
    };
  }
});
</script>
<template>
  <div class="article-card-body flex flex-col">
    <img
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
      <div class="article-card-title flex justify-between">
        <h2>{{ article.title }}</h2>
        <img
          class="invert dark:invert-0"
          src="/arrow-up-right.svg"
          alt="arrow-icon"
        />
      </div>
      <div>
        <p
          class="font-normal text-base text-slate-600 article-truncate-lines-2"
        >
          {{ article.content }}
        </p>
      </div>
    </div>
    <div class="article-card-footer flex flex-wrap gap-2">
      <ArticleTag
        v-for="(tag, index) in article.tags"
        :key="index"
        :tag="tag"
      />
    </div>
  </div>
</template>
<!-- ../models/index -->
