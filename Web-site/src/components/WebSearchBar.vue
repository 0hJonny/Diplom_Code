<template>
  <section class="section section_spacing_n">
    <div class="section__body">
      <div
        class="cells cells_space_xl cells_responsive"
        style="--cells-v-spacing: var(--space-n)"
      >
        <div
          class="cells__item cells__item_width"
          style="--cells-item-width: 66.6%"
        >
          <div class="space space_direction_vertical space_size_l">
            <form
              class="text text_size_small align_center search__form"
              action="/search/"
              method="get"
              data-js-search-mobile=""
            >
              <input
                class="form-input form-input_light-border search__input"
                placeholder="Search..."
                type="search"
                data-js-search-input-mobile=""
              />
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
    </div>
  </section>
</template>

<style scoped>
.search__form {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 50vh;
  background-color: var(--color-bkg);
  box-shadow: var(--shadow-3);
  transition: var(--transition);
}

.search__input {
  width: 60%;
  padding: var(--space-m);
  font-size: var(--text-size-regular);
  border-radius: 25px;
  border: none;
  color: var(--color-text-primary);
  border: 1px solid var(--color-palette-silver);
  transition:
    box-shadow 0.3s,
    background-color 0.3s;
}

.search__input:focus {
  background-color: var(--color-bkg);
  color: var(--color-text-primary);
  box-shadow: 0px 0px 0px 2px var(--color-palette-silver);
  border: 1px solid var(--color-palette-silver);
}

.search__input:not(:placeholder-shown) {
  background-color: var(--color-bkg);
}

.search__button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  color: var(--color-text-primary);
  background-color: var(--color-text-primary);
  border: none;
  border-radius: 25px;
  transition:
    box-shadow 0.3s,
    var(--transition);
}

.search__button:hover {
  background-color: var(--color-text-title);
  transition: background-color 0.3s;
}

.search__button:focus {
  box-shadow: 0px 0px 0px 2px var(--color-palette-silver);
}

@media (hover: hover) {
  .search__input:hover:not(:placeholder-shown) {
    background-color: rgba(var(--color-text-primary), 0.1);
    color: var(--color-text-primary);
  }

  .search__input:focus:not(:placeholder-shown) {
    border: 1px solid var(--color-palette-silver);
  }
}
</style>
