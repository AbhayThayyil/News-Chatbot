import { Box } from "@mui/material";
import type { ChatMessage } from "../../types/chat";
import { useAutoScroll } from "../../hooks/useAutoScroll";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import { SuggestedPrompts } from "./SuggestedPrompts";

interface MessageListProps {
  messages: ChatMessage[];
  isLoading: boolean;
  onSuggestedPrompt: (prompt: string) => void;
}

export function MessageList({ messages, isLoading, onSuggestedPrompt }: MessageListProps) {
  const bottomRef = useAutoScroll(messages.length + (isLoading ? 1 : 0));

  if (messages.length === 0 && !isLoading) {
    return (
      <Box
        sx={{
          flex: 1,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          px: 2,
        }}
      >
        <SuggestedPrompts onSelect={onSuggestedPrompt} />
      </Box>
    );
  }

  return (
    <Box
      sx={{
        flex: 1,
        overflowY: "auto",
        px: { xs: 2, sm: 4 },
        py: 3,
      }}
    >
      <Box sx={{ display: "flex", flexDirection: "column", gap: 2.5, maxWidth: 760, mx: "auto" }}>
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        {isLoading && <TypingIndicator />}
        <div ref={bottomRef} />
      </Box>
    </Box>
  );
}
