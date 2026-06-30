import { useMutation } from "@tanstack/react-query";
import { isAxiosError } from "axios";
import { useRef, useState } from "react";
import { sendChatMessage, type Citation } from "../api/chat";
import { useToast } from "../components/common/ToastProvider";
import type { ChatMessage } from "../types/chat";

function createMessage(
  role: ChatMessage["role"],
  content: string,
  citations?: Citation[]
): ChatMessage {
  return {
    id: crypto.randomUUID(),
    role,
    content,
    createdAt: Date.now(),
    citations,
  };
}

function getErrorMessage(error: unknown): string {
  if (isAxiosError(error)) {
    if (!error.response) return "Could not reach the server. Check your connection.";
    if (error.response.status === 422) return "That message couldn't be processed.";
    return "Something went wrong on our end.";
  }
  return "Unexpected error. Please try again.";
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const conversationIdRef = useRef<string | null>(null);
  const { showToast } = useToast();

  const mutation = useMutation({
    mutationFn: (text: string) =>
      sendChatMessage({ message: text, conversation_id: conversationIdRef.current }),
    retry: 1,
    onSuccess: (data) => {
      conversationIdRef.current = data.conversation_id;
      setMessages((prev) => [...prev, createMessage("assistant", data.reply, data.citations)]);
    },
    onError: (error, text) => {
      showToast({
        message: getErrorMessage(error),
        severity: "error",
        actionLabel: "Retry",
        onAction: () => mutation.mutate(text),
      });
    },
  });

  function sendMessage(text: string) {
    const trimmed = text.trim();
    if (!trimmed || mutation.isPending) return;

    setMessages((prev) => [...prev, createMessage("user", trimmed)]);
    mutation.mutate(trimmed);
  }

  function clearConversation() {
    setMessages([]);
    conversationIdRef.current = null;
  }

  return { messages, isLoading: mutation.isPending, sendMessage, clearConversation };
}
