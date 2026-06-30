import { Box } from "@mui/material";
import { useChat } from "../../hooks/useChat";
import { MessageList } from "./MessageList";
import { PromptInput } from "./PromptInput";

export function ChatWindow() {
  const { messages, isLoading, sendMessage } = useChat();

  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <MessageList messages={messages} isLoading={isLoading} onSuggestedPrompt={sendMessage} />
      <PromptInput onSend={sendMessage} disabled={isLoading} />
    </Box>
  );
}
