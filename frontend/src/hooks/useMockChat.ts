import { useState } from "react";
import type { ChatMessage } from "../types/chat";

const MOCK_REPLY = `Here's a quick summary based on what you asked:

- **Story 1**: Placeholder headline about today's top story.
- **Story 2**: Placeholder headline about a developing situation.
- **Story 3**: Placeholder headline about a market update.

This is mock content — real retrieval and summarization will be wired up in the next module.`;

function createMessage(role: ChatMessage["role"], content: string): ChatMessage {
  return {
    id: crypto.randomUUID(),
    role,
    content,
    createdAt: Date.now(),
  };
}

export function useMockChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  function sendMessage(text: string) {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;

    setMessages((prev) => [...prev, createMessage("user", trimmed)]);
    setIsLoading(true);

    setTimeout(() => {
      setMessages((prev) => [...prev, createMessage("assistant", MOCK_REPLY)]);
      setIsLoading(false);
    }, 1200);
  }

  function clearConversation() {
    setMessages([]);
  }

  return { messages, isLoading, sendMessage, clearConversation };
}
