import SmartToyOutlinedIcon from "@mui/icons-material/SmartToyOutlined";
import { Avatar, Box, Paper } from "@mui/material";

const dotSx = {
  width: 6,
  height: 6,
  borderRadius: "50%",
  bgcolor: "grey.500",
  animation: "typing-bounce 1.2s infinite ease-in-out",
  "@keyframes typing-bounce": {
    "0%, 80%, 100%": { transform: "scale(0.6)", opacity: 0.4 },
    "40%": { transform: "scale(1)", opacity: 1 },
  },
};

export function TypingIndicator() {
  return (
    <Box sx={{ display: "flex", gap: 1.5, alignItems: "flex-start" }}>
      <Avatar sx={{ width: 32, height: 32, bgcolor: "grey.700" }}>
        <SmartToyOutlinedIcon fontSize="small" />
      </Avatar>
      <Paper
        elevation={0}
        sx={{
          px: 2,
          py: 1.5,
          bgcolor: "grey.100",
          borderRadius: 2,
          borderTopLeftRadius: 4,
          display: "flex",
          gap: 0.6,
        }}
      >
        <Box sx={{ ...dotSx, animationDelay: "0s" }} />
        <Box sx={{ ...dotSx, animationDelay: "0.15s" }} />
        <Box sx={{ ...dotSx, animationDelay: "0.3s" }} />
      </Paper>
    </Box>
  );
}
