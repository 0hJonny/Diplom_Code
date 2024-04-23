<script setup lang="ts">
import { RouterLink } from "vue-router";
import ThemeSwitcher from "./ThemeSwitcher.vue";
import SideBar from "./SideBar.vue";
</script>

<template>
  <header>
    <div class="header-container border-b-2 border-slate-300">
      <nav class="header-container-nav header-text">
        <div class="header-left-side">
          <SideBar />

          <!-- <RouterLink to="profiles" class="flex gap-1">
            <img
              class="header-icon invert dark:invert-0"
              src="/profile-circle.svg"
              alt="profile-icon"
            />
            <h2 class="profile-text">Profile</h2>
          </RouterLink> -->
        </div>
        <div class="header-right-side flex gap-4 items-center">
          <div>
            <RouterLink to="/">
              <h2>Home</h2>
            </RouterLink>
          </div>
          <div>
            <RouterLink to="/about">
              <h2>About</h2>
            </RouterLink>
          </div>
          <div>
            <ThemeSwitcher />
            <!-- <div class="theme-switcher relative">
              <div
                class="theme-switcher-icon absolute bg-white rounded-full z-10"
              />
              <img
                class="theme-switcher-icon"
                src="/moon.svg"
                alt="moon-theme-icon"
              />
              <img
                class="theme-switcher-icon"
                src="/sun.svg"
                alt="sun-theme-icon"
              />
            </div> -->
          </div>
        </div>
      </nav>
    </div>
  </header>
</template>
