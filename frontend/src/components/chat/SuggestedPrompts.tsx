import { Box, Chip, Stack, Typography } from "@mui/material";

const PROMPTS = [
  "What is today's sports news?",
  "Latest AI news.",
  "Summarize today's India news.",
  "Tell me the latest Formula 1 updates.",
];

interface SuggestedPromptsProps {
  onSelect: (prompt: string) => void;
}

export function SuggestedPrompts({ onSelect }: SuggestedPromptsProps) {
  return (
    <Box sx={{ textAlign: "center", maxWidth: 480, mx: "auto" }}>
      <Typography variant="h6" gutterBottom>
        Ask about today's news
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Try one of these, or ask your own question.
      </Typography>
      <Stack direction="row" flexWrap="wrap" gap={1} justifyContent="center">
        {PROMPTS.map((prompt) => (
          <Chip key={prompt} label={prompt} onClick={() => onSelect(prompt)} variant="outlined" />
        ))}
      </Stack>
    </Box>
  );
}
