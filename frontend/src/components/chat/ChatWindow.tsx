import { Box } from "@mui/material";
import { forwardRef } from "react";
import type { useChat } from "../../hooks/useChat";
import { MessageList } from "./MessageList";
import { PromptInput, type PromptInputHandle } from "./PromptInput";

interface ChatWindowProps {
  chat: ReturnType<typeof useChat>;
}

export const ChatWindow = forwardRef<PromptInputHandle, ChatWindowProps>(function ChatWindow(
  { chat },
  inputRef
) {
  const { messages, isLoading, sendMessage } = chat;

  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <MessageList messages={messages} isLoading={isLoading} onSuggestedPrompt={sendMessage} />
      <PromptInput ref={inputRef} onSend={sendMessage} disabled={isLoading} />
    </Box>
  );
});
