import HomeVue from "@/views/Home.vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeVue,
    },
    {
      path: "/search",
      name: "search",
      component: () => import("@/views/SearchView.vue"),
    },
    {
      path: "/security",
      name: "security",
      component: () => import("@/views/SecurityView.vue"),
    },
    {
      path: "/privacy",
      name: "privacy",
      component: () => import("@/views/PrivacyView.vue"),
    },
    {
      path: "/tech",
      name: "tech",
      component: () => import("@/views/TechView.vue"),
    },
    {
      path: "/crypto",
      name: "crypto",
      component: () => import("@/views/CryptoView.vue"),
    },


    {
      path: "/about",
      name: "about",
      component: () => import("@/views/AboutView.vue"),
    },
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // }
    {
      path: "/article/:id",
      name: "article",
      component: () => import("@/views/ArticlePage.vue"),
      props: route => {
        return { article: Array.isArray(route.params.id) ? route.params.id[0] : route.params.id || null };
      },
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: () => import("@/views/NotFound.vue"),
    },
  ],
  
});

export default router;
