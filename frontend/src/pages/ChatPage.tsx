import { useEffect, useRef } from "react";
import { AppShell } from "../components/layout/AppShell";
import { ChatWindow } from "../components/chat/ChatWindow";
import { useChat } from "../hooks/useChat";
import type { PromptInputHandle } from "../components/chat/PromptInput";

export function ChatPage() {
  const chat = useChat();
  const inputRef = useRef<PromptInputHandle>(null);

  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      const isModifierPressed = event.metaKey || event.ctrlKey;
      if (!isModifierPressed) return;

      if (event.key === "k") {
        event.preventDefault();
        chat.clearConversation();
        inputRef.current?.focus();
      } else if (event.key === "/") {
        event.preventDefault();
        inputRef.current?.focus();
      }
    }

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [chat]);

  return (
    <AppShell onClearChat={chat.clearConversation} canClearChat={chat.messages.length > 0}>
      <ChatWindow chat={chat} ref={inputRef} />
    </AppShell>
  );
}
