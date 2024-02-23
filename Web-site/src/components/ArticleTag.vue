<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  tag: string;
}>();

const tagStyles: string[] = [
  "tag-card-violet",
  "tag-card-gray",
  "tag-card-orange",
  "tag-card-green",
  "tag-card-red",
  "tag-card-yellow",
  "tag-card-blue",
  "tag-card-cyan",
  "tag-card-pink",
  "tag-card-purple",
  "tag-card-teal",
];

/**
 * Returns a random style from the tagStyles array.
 *
 * @return {string} A random style from the tagStyles array
 */
const getRandomStyle = () => {
  const randomIndex = Math.floor(Math.random() * tagStyles.length);
  return tagStyles[randomIndex];
};

const randomTagStyle = computed(() => {
  return getRandomStyle();
});
</script>

<template>
  <div
    class="cursor-pointer motion-reduce:transition-none motion-reduce:hover:transform-none duration-100 hover:scale-110"
  >
    <div :class="randomTagStyle">
      {{ tag }}
    </div>
  </div>
</template>
