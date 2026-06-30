import type { Citation } from "../api/chat";

export type MessageRole = "user" | "assistant";

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  createdAt: number;
  citations?: Citation[];
}

export interface Conversation {
  id: string;
  title: string;
}
