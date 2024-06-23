<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";

import ArticleCard from "@/components/ArticleCard.vue";
import ArticleTag from "@/components/ArticleTag.vue";
import { mapToArticle, type Article } from "@/models/data/ArticleStructure";
import urls from "@/utils/urls";
import service from "@/utils/https";
import { languageLocales } from "@/utils/languageLocales";

const router = useRouter();

const pagesData = reactive({
  totalItems: 0,
  elementsPerPage: 12,
  currentPage: Number(router.currentRoute.value.query.page) || 1
});

const articles = ref<Article[]>([]);
const searchText = ref("");
const tags = ref<string[]>([]);
const isFocused = ref(false);
const placeholder = "Use '#' for tags. Search articles...";

const handleFocus = () => {
  isFocused.value = true;
};

const handleBlur = () => {
  isFocused.value = false;
};

const handleKeyup = (event: KeyboardEvent) => {
  if (event.key === " " && searchText.value.startsWith("#")) {
    addTag(searchText.value.trim());
  }
};

const handleDelete = () => {
  if (searchText.value === "" && tags.value.length > 0) {
    tags.value.pop();
  }
};

const addTag = (tag: string) => {
  tags.value.push(tag);
  searchText.value = "";
};

const removeTag = (index: number) => {
  tags.value.splice(index, 1);
};

const clearSearch = () => {
  searchText.value = "";
  tags.value = [];
};

onMounted(() => {
  const routeQueryTags = router.currentRoute.value.query.tag;
  if (routeQueryTags) {
    if (Array.isArray(routeQueryTags)) {
      tags.value = routeQueryTags;
    } else {
      tags.value.push(routeQueryTags);
    }
    getSearch();
  }
});

async function getSearch() {
  try {
    let query = "";
    if (searchText.value !== "") {
      query += "\\".concat(searchText.value) + "\\";
    }
    if (tags.value.length > 0) {
      tags.value.forEach((tag, index) => {
        if (index >= 0 && query != "") {
          query += "+";
        }
        query += "!!".concat(tag.replace("#", "").concat("!!"));
      });
      console.log(query);
    }
    const response = await service.get(
      `${urls.search}?page=${pagesData.currentPage}&limit=${pagesData.elementsPerPage}&language_code=${languageLocales[document.documentElement.getAttribute("lang") || "en"]}&query=${query}`
    );
    console.log(response);
    if (response.data) {
      articles.value = response.data.map((article: any) =>
        mapToArticle(article)
      );
      console.log(articles.value);
    } else {
      articles.value = [];
    }
    console.log(articles.value);
  } catch (error) {
    console.error(error);
  }
  console.log("Search:", searchText.value, "Tags:", tags.value);
}
</script>

<template>
  <div class="search-bar" :class="{ focused: isFocused }">
    <div class="input-wrapper">
      <div v-for="(tag, index) in tags" :key="index" class="tag">
        <ArticleTag :tag="tag" @click="removeTag(index)" />
        <!-- {{ tag }} -->
        <!-- <span class="remove-tag" @click="removeTag(index)">x</span> -->
      </div>
      <input
        ref="input"
        v-model="searchText"
        @focus="handleFocus"
        @blur="handleBlur"
        @keyup="handleKeyup"
        @keydown.delete="handleDelete"
        :placeholder="placeholder"
      />
    </div>
    <button
      v-if="searchText || tags.length > 0"
      class="clear-button"
      @click="clearSearch"
    >
      ❌
    </button>
    <button @click="getSearch" class="search-button">Search</button>
  </div>
  <div
    class="card articles-container article-card-body"
    v-if="articles"
    v-for="article in articles"
    :key="article.id"
  >
    <ArticleCard :article="article" />
  </div>
</template>

<style scoped>
input {
  background-color: var(--color-bkg);
  transition: var(--transition);
}

.search-bar {
  font-family: "Noto Sans", sans-serif;
  font-size: 16px;
  max-width: min(
    1100px,
    calc(2.5 / 5 * (100vw - 32px))
  ); /* 3/5 of display size */
  margin: 0 auto; /* center card horizontally */

  display: flex;
  align-items: center;
  padding: 0.5rem;
  border: 2px solid var(--color-text-primary);
  border-radius: 10px;
  transition:
    border-color 0.3s,
    box-shadow 0.3s;
  /* flex-wrap: wrap; */
}
.search-bar.focused {
  border-color: var(--color-text-title);
  box-shadow: 0 0 5px var(--color-text-title);
}
.input-wrapper {
  display: flex;
  align-items: center;
  flex-grow: 1;
  color: var(--color-text-primary);
  flex-wrap: wrap;
}
input {
  flex-grow: 1;
  border: none;
  outline: none;
  padding: 0.5rem;
  font-size: 1rem;
  flex-basis: 0;
  flex-grow: 1;
}
input::placeholder {
  color: var(--color-text-sub);
}
.clear-button {
  border: none;
  background: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: var(--color-text-primary);
  margin: 0 1vw;
}
.search-button {
  border: none;
  background: var(--color-text-title);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.search-button:hover {
  background-color: darkviolet;
}
.tag {
  display: flex;
  align-items: center;
  margin: 0.2rem;
  font-size: 0.9rem;
  /* flex-basis: 0;
  flex-grow: 1; */

  /* padding: 0.2rem 0.5rem; */
  /* margin-right: 0.5rem; */
  /* background-color: lightgrey; */
  /* border-radius: 5px; */
}
.remove-tag {
  margin-left: 0.3rem;
  cursor: pointer;
}

.card {
  max-width: min(
    1100px,
    calc(2.5 / 5 * (100vw - 32px))
  ); /* 3/5 of display size */

  margin: 1rem auto; /* center card horizontally */
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
}
</style>
