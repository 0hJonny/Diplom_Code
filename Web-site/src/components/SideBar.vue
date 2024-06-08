<template>
  <div>
    <!-- Кнопка открытия/закрытия меню -->
    <div>
      <button
        class="header__head-mobile-action"
        @click="toggleMenu"
        aria-label="Toggle navigation"
      >
        <svg
          class="svg-icon color-dynamic-bkg"
          width="24"
          height="24"
          transform="scale(0.75)"
        >
          <use xlink:href="/menu-pack-black.svg#menu"></use>
        </svg>
        <div class="menu__blog_text">Menu</div>
      </button>
    </div>

    <!-- Меню -->
    <nav
      class="menu"
      :class="{ menu_opened: isMenuOpen, menu_closed: !isMenuOpen }"
      @keydown.esc="toggleMenu"
      @click="toggleMenu"
    >
      <div class="menu__bucket" @click.stop>
        <div class="menu__wrapper">
          <div class="menu__header">
            <button
              @click="toggleMenu"
              class="menu__header-button-close"
              aria-label="Close navigation"
              data-js-header-menu-close
              tabindex="0"
            >
              <svg
                class="svg-icon svg-icon-white"
                width="24"
                height="24"
                transform="scale(0.75)"
              >
                <use xlink:href="/menu-pack-black.svg#close"></use>
              </svg>
              <div class="menu__header-text">Menu</div>
            </button>
            <!-- <div class="menu__header-search">
              <form
                class="menu__header-search-form"
                action="/search/"
                method="get"
                data-js-search-mobile
              >
                <input
                  class="menu__header-search-form-input"
                  placeholder="Поиск..."
                  type="search"
                  data-js-search-input-mobile
                />
                <button
                  type="submit"
                  class="menu__header-search-form-button"
                  title="Поиск"
                >
                  <svg
                    class="svg-icon menu__header-search-form-button-icon"
                    width="24"
                    height="24"
                  >
                    <use xlink:href="#search"></use>
                  </svg>
                </button>
              </form>
            </div> -->
          </div>
          <ul>
            <li
              v-for="(menuItem, index) in menuItems"
              :key="index"
              :class="{
                menu__item: true,
                'menu__item-has-children': menuItem.children
              }"
            >
              <input
                v-if="menuItem.children"
                :id="'header-nav-' + (index + 1)"
                type="checkbox"
                class="menu__sub-items-toggle"
                aria-hidden="true"
                :data-js-header-toggle="'header-nav-' + (index + 1)"
              />
              <label
                class="menu__item-link"
                v-if="menuItem.children"
                :for="'header-nav-' + (index + 1)"
                tabindex="0"
              >
                <div class="menu__label">{{ menuItem.label }}</div>
                <svg class="svg-icon menu__icon" width="24" height="24">
                  <use xlink:href="#mdi-chevron-right"></use>
                </svg>
              </label>
              <a
                v-else
                :class="{ 'menu__item-link': true }"
                :href="menuItem.link"
                tabindex="0"
              >
                <div class="menu__label">{{ menuItem.label }}</div>
              </a>
              <ul v-if="menuItem.children" class="menu__submenu">
                <li
                  v-for="(subItem, subIndex) in menuItem.children"
                  :key="subIndex"
                >
                  <a
                    class="menu__submenu-link"
                    :href="subItem.link"
                    tabindex="0"
                    >{{ subItem.label }}</a
                  >
                </li>
              </ul>
            </li>
          </ul>
          <div class="menu__divider"></div>
          <div class="menu__footer">
            <div class="menu__footer-social">
              <div
                v-for="(socialItem, index) in socialItems"
                :key="index"
                class="menu__footer-social__item"
              >
                <a
                  class="menu__footer-social__icon-link"
                  :href="socialItem.link"
                  :title="socialItem.title"
                  target="_blank"
                  rel="noopener"
                >
                  <svg
                    class="svg-icon menu__footer-social__icon lazyloaded"
                    width="24"
                    height="24"
                  >
                    <use :xlink:href="socialItem.icon"></use>
                  </svg>
                </a>
              </div>
            </div>
            <p class="menu__footer-notes">
              Developed by
              <a
                href="https://github.com/0hJonny"
                target="_blank"
                rel="noopener"
                >0hJonny</a
              >
              on GitHub.
            </p>
          </div>
        </div>
        <div data-js-header-overlay class="menu__overlay"></div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isMenuOpen: false,
      menuItems: [
        // {
        //   label: "Новости",
        //   children: [
        //     {
        //       label: "Новости кибербезопасности",
        //       link: "https://localhost/news/"
        //     },
        //     {
        //       label: "Новости криптовалют",
        //       link: "https://localhost/crypto-coins/"
        //     }
        //   ]
        // },
        { label: "Home", link: "/" },
        { label: "Редакция", link: "/editorial" },
        { label: "Безопасность", link: "/security" },
        { label: "Конфиденциальность", link: "/privacy" },
        { label: "Криптовалюта", link: "/crypto" },
        { label: "Технологии", link: "/tech" },
        {
          label: "Ресурсы",
          children: [
            {
              label: "Что такое VPN?",
              link: "https://localhost/what-is-vpn/"
            },
            {
              label: "Как использовать VPN?",
              link: "https://localhost/how-to-use-vpn/"
            }
          ]
        },
        { label: "О нас", link: "/about" }
        // Добавьте остальные пункты меню по аналогии
      ],
      socialItems: [
        {
          title: "Twitter",
          link: "",
          icon: "#twitter-x"
        },
        {
          title: "Facebook",
          link: "",
          icon: "#facebook-h"
        },
        {
          title: "YouTube",
          link: "",
          icon: "#youtube-h"
        },
        {
          title: "LinkedIn",
          link: "",
          icon: "#linkedin-h"
        },
        {
          title: "TikTok",
          link: "",
          icon: "#tiktok-h"
        },
        {
          title: "Flipboard",
          link: "",
          icon: "#flipboard-h"
        },
        {
          title: "Newsletter",
          link: "",
          icon: "#subscribe-h"
        }
      ]
    };
  },

  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen; // Изменяем состояние меню при нажатии на кнопку
    }
  }
};
</script>

<style scoped>
.menu {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 100%;
  z-index: 10000;
  transition:
    transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1),
    background-color 0s ease,
    backdrop-filter 0s ease;
  background-color: rgba(var(--color-cover-bkg-rgb), 0);
  backdrop-filter: blur(0);
  cursor: pointer;
}

.menu.menu_opened {
  display: block;
  transform: translateX(0);
  background-color: rgba(var(--color-cover-bkg-rgb), 0.7);
  backdrop-filter: blur(5px);
  transition:
    transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1),
    background-color 0.3s ease,
    backdrop-filter 0.3s ease;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.menu.menu_closed {
  visibility: hidden;
  cursor: default;
  transition:
    visibility 0.3s ease,
    transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.menu_overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0);
  backdrop-filter: blur(0);
  z-index: 9999;
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
}

.menu.menu_opened + .menu_overlay {
  opacity: 1;
  transition: opacity 0.3s ease-in-out;
}

.menu__wrapper {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  margin: auto;
  max-width: min(30%, 100vw);
  background-color: var(--color-black); /* Белый фон меню */
  /* padding: var(--space-m); */
  color: var(--color-white); /* Белый текст */
  z-index: 10001; /* Помещаем меню над полупрозрачным фоном */
  transform: translateX(-100%);
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  overflow-y: scroll;
  -webkit-overflow-scrolling: touch;
  will-change: transform;
  cursor: default;
  scroll-behavior: smooth;
  scrollbar-width: none;
  padding-right: var(--space-m);
  padding-left: 112px;
}

.menu__wrapper::-webkit-scrollbar {
  display: none;
}

@media (max-width: 1079px) {
  .menu__wrapper {
    width: 100vw;
    max-width: 100vw;
    left: 0;
    transform: translateX(-100%);
  }
}

.menu.menu_opened .menu__wrapper {
  transform: translateX(0);
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.menu__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-m); /* Отступ снизу */
}

.menu_opened .menu__header-button-close {
  display: flex;
}

.menu__header-button-close {
  margin-top: 30px;
  display: flex;
  width: fit-content;
  cursor: pointer;
  align-items: center;
  padding: var(--space-s) var(--space-m) var(--space-s) var(--space-s);
  border-radius: 25px; /* добавление скругления углов */
}

@media (max-width: 1079px) {
  .menu__header-button-close {
    padding: var(--space-s);
  }
}

.menu__header-button-close:hover {
  background-color: var(--color-palette-dark);
}

.menu__header-text {
  font-size: var(--text-size-small); /* Размер текста заголовка */
  color: var(--color-white);
  margin-left: var(--space-xs);
  line-height: 160%;
}

@media (max-width: 1079px) {
  .menu__header-text {
    display: none;
  }
}

.menu__blog_text {
  font-size: var(--text-size-small); /* Размер текста заголовка */
  color: var(--color-text-primary);
  margin-left: var(--space-xs);
  line-height: 160%;
}

@media (max-width: 1079px) {
  .menu__blog_text {
    display: none;
  }
}

.menu__header-search {
  display: none;
}

@media (max-width: 1079px) {
  .menu__header-search {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 120px;
    padding-bottom: 10px;
  }
}

.menu__item-link {
  position: relative;
  display: flex;
  height: 48px;
  padding: 0 var(--space-m) 0 var(--space-n);
  align-items: center;
  gap: var(--space-s);
  align-self: stretch;
  font-size: var(--text-size-regular);
  font-weight: 400;
  line-height: 24px;
  color: inherit; /* Использовать цвет текста из родительского элемента */
  text-decoration: none; /* Убрать подчеркивание у ссылок */
}

.menu__item-link:hover {
  background-color: var(--color-palette-dark);
}

.menu__item-has-children .menu__item-link {
  justify-content: space-between;
  cursor: pointer;
}

.menu__submenu {
  display: none;
  padding-left: var(--space-m);
}

.menu__item-has-children input[type="checkbox"]:checked ~ .menu__submenu {
  display: block; /* Отображаем вложенное меню при выборе родительского пункта */
}

.menu__item-has-children input[type="checkbox"] {
  position: absolute;
  visibility: hidden; /* или opacity: 0; */
}

.menu__footer {
  display: flex;
  flex-direction: column;
  gap: var(--space-m);
  padding: var(--space-m) var(--space-n);
}

.menu__footer-social {
  display: flex;
  gap: var(--space-m);
}

.menu__footer-notes {
  color: var(--color-palette-silver);
  font-size: var(--text-size-tiny);
  font-weight: 400;
  line-height: 160%;
  padding: var(--header-padding);
}

.header__burger {
  display: flex;
  cursor: pointer;
}

.header__head-mobile-action {
  display: inline-flex;
  width: fit-content;
  cursor: pointer;
  align-items: center;
  padding: var(--space-s) var(--space-m) var(--space-s) var(--space-s);
  padding-right: 16px;
  border-radius: 25px;
}

@media (max-width: 1079px) {
  .header__head-mobile-action {
    padding: var(--space-s);
  }
}

.header__head-mobile-action:hover {
  background-color: var(--color-palette-dark-dynamic);
}

.svg-icon-black {
  fill: var(--color-black);
}

.svg-icon-white {
  fill: var(--color-white);
}

.color-dynamic-bkg {
  fill: var(--color-text-primary);
}
</style>
