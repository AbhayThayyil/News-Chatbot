import SendRoundedIcon from "@mui/icons-material/SendRounded";
import { Box, IconButton, TextField } from "@mui/material";
import { useState, type KeyboardEvent } from "react";

interface PromptInputProps {
  onSend: (text: string) => void;
  disabled: boolean;
}

export function PromptInput({ onSend, disabled }: PromptInputProps) {
  const [value, setValue] = useState("");

  function handleSend() {
    if (!value.trim() || disabled) return;
    onSend(value);
    setValue("");
  }

  function handleKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  }

  return (
    <Box
      sx={{
        borderTop: "1px solid",
        borderColor: "divider",
        bgcolor: "background.paper",
        px: { xs: 2, sm: 4 },
        py: 2,
      }}
    >
      <Box
        sx={{
          maxWidth: 760,
          mx: "auto",
          display: "flex",
          alignItems: "flex-end",
          gap: 1,
          border: "1px solid",
          borderColor: "divider",
          borderRadius: 3,
          px: 1.5,
          py: 0.5,
        }}
      >
        <TextField
          value={value}
          onChange={(event) => setValue(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about today's news..."
          multiline
          maxRows={6}
          fullWidth
          variant="standard"
          slotProps={{ input: { disableUnderline: true } }}
          disabled={disabled}
        />
        <IconButton
          color="primary"
          onClick={handleSend}
          disabled={disabled || !value.trim()}
          aria-label="Send message"
          sx={{ mb: 0.5 }}
        >
          <SendRoundedIcon />
        </IconButton>
      </Box>
    </Box>
  );
}
