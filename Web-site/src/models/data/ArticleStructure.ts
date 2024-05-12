import { formatDate } from "@/utils/formatDate";
export interface Article {
  id: string;
  title: string;
  publishedDate: string;
  category: string;
  tags: string[];
  content: string;
  languageCode: string;
  neuralNetworks: {
    annotator: string;
    translator: string;
  };
  imageSource?: string;

}

/**
 * Map a JSON object to an Article
 * @param {Object} data The JSON object to map
 * @returns {Article} The mapped Article
 */
export function mapToArticle(data: any): Article {
  return {
    id: data.id || "",
    title: data.title.replace(/^"|"(?=\s|$)/g, "") || "",
    publishedDate: formatDate(data.publishedDate).toUpperCase() || "",
    category: (data.category || "").toUpperCase() || "", // Add a fallback value in case data.category is null or undefined
    tags: (data.tags || "[]") // Parse the string to an array
          .replace(/^\[|\]$/g, "") // Remove the surrounding square brackets
          .split(", ") // Split the string by comma and space
          .map((tag: string) =>
            tag.replace(/^"|"$/g, "").trim().replace(/\\|"/g, "")
          ), // Parse each tag and remove the surrounding quotes, and remove backslashes and quotes from the tag value
    content: data.content || "",
    languageCode: data.language_code || "",
    neuralNetworks: data.neural_networks || {
      annotator: "",
      translator: "",
    },
    imageSource: data.image_source
      ? `http://${import.meta.env.VITE_MINIO_URL || "localhost:9000"}${
          data.image_source
        }`
      : "",
  };
}


