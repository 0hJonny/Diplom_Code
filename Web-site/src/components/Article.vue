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
      author: "Jane Smith",
      publishedDate: "2022-03-15",
      title: "How to Bake the Perfect Chocolate Cake",
      description:
        "In this article, we explore the secrets to baking a moist and delicious chocolate cake.",
      imageLink: "https://example.com/cake.jpg",
      tags: ["baking", "chocolate", "desserts"],
      content:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    };
  },
});
</script>
<template>
  <div class="article-card-body flex flex-col">
    <img
      class="article-card-image"
      :src="article.imageLink"
      alt="article-image"
    />
    <div>
      <div class="card-meta flex gap-1 font-semibold text-sm text-violet-700">
        <h3 class="card-meta-author">{{ article.author }}</h3>
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
          {{ article.description }}
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
../models/index
