export interface Article {
  id: string;
  title: string;
  publishedDate: string;
  category: string;
  tags: string[];
  content: string;
  languageCode: string;
  imageSource?: string;
}
