<template>
  <div class="language-switcher">
    <select v-model="selectedLanguage" @change="handleChangeLanguage">
      <option
        v-for="(value, key) in languageLocales"
        :key="key"
        :value="key"
        :selected="key === selectedLanguage"
      >
        {{ key + " - " + languageLocaleNames[value] }}
      </option>
    </select>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { languageLocales } from "@/utils/languageLocales.js";
import { languageLocaleNames } from "@/utils/languageLocaleNames.js";

const router = useRouter();
const route = useRoute();

const selectedLanguage = ref("");

onMounted(() => {
  selectedLanguage.value = getSelectedLanguage();
});

function handleChangeLanguage() {
  document.documentElement.setAttribute("lang", selectedLanguage.value);
  localStorage.setItem("lang", selectedLanguage.value);
  router.push({
    query: { ...route.query, lang: selectedLanguage.value }
  });
}

function getSelectedLanguage(): string {
  return (
    (route.query.lang as string) ||
    (document.documentElement.getAttribute("lang") as string) ||
    "en"
  );
}
</script>

<style scoped>
.language-switcher {
  display: flex;
  align-items: center;
  margin-right: 16px;
  border: none;
  border-radius: 16px;
  padding: 4px 16px;
  background-color: var(--color-text-primary);
  color: var(--color-black);
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
}

.language-switcher :deep(select) {
  font-family: "Noto Sans", sans-serif;
}

.language-switcher :deep(select) {
  color: var(--color-bkg);
  background: var(--color-text-primary);
}

.language-switcher :deep(option) {
  color: var(--color-bkg);
  background: var(--color-text-primary);
}

&:hover {
  background-color: var(--color-palette-dark-dynamic);
}
</style>
