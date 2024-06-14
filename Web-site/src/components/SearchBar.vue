<template>
  <div
    class="cells cells_space_xl cells_responsive"
    style="--cells-v-spacing: var(--space-n)"
  >
    <div
      class="cells__item cells__item_width"
      style="--cells-item-width: 66.6%"
    >
      <!-- The search view heading -->
      <h1 class="heading heading_size_1 newsletter__title">Search</h1>
      <div class="space space_direction_vertical space_size_l">
        <!-- The search form -->
        <form
          class="text text_size_small align_center search__form"
          action="/search/"
          method="get"
          data-js-search-mobile=""
        >
          <!-- The search input -->
          <input
            class="form-input form-input_light-border search__input"
            placeholder="Search..."
            type="search"
            data-js-search-input-mobile=""
            autofocus=""
          />
          <!-- The search button -->
          <button
            type="submit"
            class="button search__button button_height_as-input-field"
            title="Search"
          >
            <svg class="svg-icon" width="22" height="22">
              <use xlink:href="#mdi-magnify"></use>
            </svg>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
