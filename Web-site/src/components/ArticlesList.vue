<script setup lang="ts">
import { reactive } from "vue";
import { useRouter } from "vue-router";

import ArticleVue from "./Article.vue";
import PaginationVue from "./Pagination.vue";
import type { Article } from "../models/index";

const router = useRouter();

const pagesData = reactive({
  currentPage: Number(router.currentRoute.value.query.page) || 1,
  elementsPerPage: 12,
  totalItems: 400,
});

/// Test data

const data = <Article[]>[
  {
    author: "Jane Smith",
    publishedDate: "2022-03-15",
    title: "How to Bake the Perfect Chocolate Cake",
    description:
      "In this article, we explore the secrets to baking a moist and delicious chocolate cake.",
    imageLink:
      "https://www.lascimmiapensa.com/wp-content/uploads/2022/03/GigaChad.jpg",
    tags: ["baking", "chocolate", "desserts"],
    content:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
  },
  {
    author: "John Doe & Jane Smith",
    publishedDate: "2022-04-15",
    title: "Applying AI in Baking: Creating Innovative Recipes",
    description:
      "Exploring the fusion of technology and baking to create unique and innovative recipes using AI.",
    imageLink:
      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.redd.it%2Fnqxk9l0jn1t61.jpg&f=1&nofb=1&ipt=8557f318dd8dbed1f1908f2c8f26bf8e35b6515a36063e972f6cf25c83f769f8&ipo=images",
    tags: ["AI", "Baking", "Innovation"],
    content:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
  },
  {
    author: "Jane Smith",
    publishedDate: "2022-03-15",
    title: "How to Bake the Perfect Chocolate Cake",
    description:
      "In this article, we explore the secrets to baking a moist and delicious chocolate cake.",
    imageLink: "/Refactory.png",
    tags: ["Baking", "Chocolate", "Desserts"],
    content:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
  },
  {
    author: "John Doe",
    publishedDate: "2022-04-01",
    title: "The Impact of Artificial Intelligence on Cybersecurity",
    description:
      "Exploring the role of AI in enhancing cybersecurity measures.",
    imageLink:
      "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.kindpng.com%2Fpicc%2Fm%2F107-1078121_transparent-pepe-classic-5-sticker-gif-by-streamlabs.png&f=1&nofb=1&ipt=e87613c859b3f343f4eb1d2f8bde76761153f20b89dc6fcb9a4730c7654c6140&ipo=images",
    tags: ["AI", "Cybersecurity", "Technology"],
    content:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
  },
  {
    author: "John Doe",
    publishedDate: "2022-04-01",
    title: "The Impact of Artificial Intelligence on Cybersecurity",
    description:
      "Exploring the role of AI in enhancing cybersecurity measures.",
    imageLink: "/img_01.png",
    tags: ["AI", "Cybersecurity", "Technology"],
    content:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
  },
];
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
            v-for="(article, index) in data"
            :key="index"
            :article="article"
          />
          <ArticleVue
            v-for="(article, index) in data"
            :key="index"
            :article="article"
          />
          <ArticleVue
            v-for="(article, index) in data"
            :key="index"
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
../models/index
