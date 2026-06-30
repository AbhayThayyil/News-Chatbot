import { apiClient } from "./client";

export interface Citation {
  title: string;
  url: string;
  source: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string | null;
}

export interface ChatResponse {
  reply: string;
  citations: Citation[];
  conversation_id: string;
}

export async function sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
  const { data } = await apiClient.post<ChatResponse>("/chat", request);
  return data;
}
