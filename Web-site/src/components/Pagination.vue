<script setup lang="ts">
import { computed, reactive } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();

const props = defineProps<{
  totalItems: number;
  elementsPerPage: number;
  currentPage: number;
  category?: string;
}>();

const pagesData = reactive({
  currentPage: props.currentPage,
  // currentPage: Number(router.currentRoute.value.query.page) || 1,
  totalPages: 0
});

const setCurrentPage = (page: number) => {
  if (page >= 1 && page <= pagesData.totalPages) {
    pagesData.currentPage = page;
    router.replace({
      path: router.currentRoute.value.path,
      query: { ...router.currentRoute.value.query, page: pagesData.currentPage }
    });
  }
};

/**
 * Calculate the total number of pages based on the total items and elements per page.
 *
 * @return {number} The total number of pages.
 */
const visiblePages = computed(() => {
  let pagesPool: any[] = [];

  pagesData.totalPages = Math.ceil(props.totalItems / props.elementsPerPage);

  if (
    pagesData.currentPage > pagesData.totalPages &&
    pagesData.totalPages != 0
  ) {
    pagesData.currentPage = pagesData.totalPages;
    setCurrentPage(pagesData.currentPage);
  } else if (pagesData.currentPage <= 1) {
    pagesData.currentPage = 1;
    setCurrentPage(pagesData.currentPage);
  }

  if (pagesData.totalPages <= 7) {
    for (let i = 1; i <= pagesData.totalPages; i++) {
      pagesPool.push(i);
    }
  } else {
    if (pagesData.currentPage < 5) {
      pagesPool = [1, 2, 3, 4, 5, "...", pagesData.totalPages];
    } else if (pagesData.currentPage >= pagesData.totalPages - 3) {
      pagesPool = [
        1,
        "...",
        pagesData.totalPages - 4,
        pagesData.totalPages - 3,
        pagesData.totalPages - 2,
        pagesData.totalPages - 1,
        pagesData.totalPages
      ];
    } else {
      pagesPool = [
        "1",
        "...",
        pagesData.currentPage - 1,
        pagesData.currentPage,
        pagesData.currentPage + 1,
        "...",
        pagesData.totalPages
      ];
    }
  }
  return pagesPool;
});

const changePage = (page: number) => {
  if (page >= 1 && page <= pagesData.totalPages) {
    pagesData.currentPage = page;
    window.scroll({ top: 0, left: 0, behavior: "smooth" });
    setCurrentPage(pagesData.currentPage);
  }
};
</script>

<template>
  <div class="flex items-center justify-between">
    <div class="flex flex-1 justify-between sm:hidden">
      <a
        href="#"
        class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50"
        @click="changePage(pagesData.currentPage - 1)"
        >Previous</a
      >
      <a
        href="#"
        class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50"
        @click="changePage(pagesData.currentPage + 1)"
        >Next</a
      >
    </div>
    <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
      <div
        class="flex items-center gap-2 cursor-pointer"
        @click="changePage(pagesData.currentPage - 1)"
      >
        <img class="" src="/arrow-left.svg" alt="arrow-left-icon" />
        <span class="text-gray-500 text-sm font-medium">Previous</span>
      </div>
      <div>
        <nav
          class="isolate inline-flex -space-x-px rounded-md"
          aria-label="Pagination"
        >
          <div class="flex items-center gap-2">
            <button
              v-for="(page, index) in visiblePages"
              :key="index"
              href="#"
              class="pagination-button"
              :class="{ active: page === pagesData.currentPage }"
              :disabled="page === '...' || page === pagesData.currentPage"
              @click="changePage(page)"
            >
              {{ page }}
            </button>
          </div>
        </nav>
      </div>
      <div
        class="flex items-center gap-2 cursor-pointer"
        @click="changePage(pagesData.currentPage + 1)"
      >
        <span class="text-gray-500 text-sm font-medium">Next</span>
        <img class="" src="/arrow-right.svg" alt="arrow-right-icon" />
      </div>
    </div>
  </div>
</template>
