export interface Article {
  id: string;
  title: string;
  publishedDate: string;
  imageLink: string;
  category: string;
  tags: string[];
  content: any;
}

function mapToArticle(data: any): Article {
  return {
    id: data[0] || '',
    title: data[1] || '',
    publishedDate: data[2] || '',
    imageLink: data[3] || '',
    category: data[4] || '',
    tags: data.tags[5] || [],
    content: data.content[6] || ''
  };
}

