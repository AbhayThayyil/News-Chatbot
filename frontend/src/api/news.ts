import { apiClient } from "./client";

export interface NewsArticle {
  title: string;
  url: string;
  source: string;
  published_at: string;
}

export interface NewsSearchRequest {
  query: string;
  max_results?: number;
}

export interface NewsSearchResponse {
  query: string;
  articles: NewsArticle[];
}

export async function searchNews(request: NewsSearchRequest): Promise<NewsSearchResponse> {
  const { data } = await apiClient.post<NewsSearchResponse>("/news/search", request);
  return data;
}
