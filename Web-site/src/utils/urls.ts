export const urls = {
  getArticlesCount: () => `/api/v1/articles/count`,
  /**
   * Returns the API endpoint for fetching a specific page of articles.
   *
   * @param {number} page - the page number to fetch
   * @param {number} perPage - the number of articles per page
   * @return {string} the API endpoint for the specified page and perPage
   */
  getArticles: (page: number, perPage: number) =>
    `/api/v1/articles?page=${page}&per_page=${perPage}`,
  getArticle: (slug: string) => `/api/v1/articles/${slug}`,
};

export default urls;
