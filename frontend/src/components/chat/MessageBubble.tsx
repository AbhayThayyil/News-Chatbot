import { Avatar, Box, Paper, Typography } from "@mui/material";
import SmartToyOutlinedIcon from "@mui/icons-material/SmartToyOutlined";
import PersonOutlineIcon from "@mui/icons-material/PersonOutlined";
import ReactMarkdown from "react-markdown";
import type { ChatMessage } from "../../types/chat";
import { SourceList } from "./SourceList";

interface MessageBubbleProps {
  message: ChatMessage;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: isUser ? "row-reverse" : "row",
        gap: 1.5,
        alignItems: "flex-start",
      }}
    >
      <Avatar
        sx={{
          width: 32,
          height: 32,
          bgcolor: isUser ? "primary.main" : "grey.700",
        }}
      >
        {isUser ? <PersonOutlineIcon fontSize="small" /> : <SmartToyOutlinedIcon fontSize="small" />}
      </Avatar>
      <Paper
        elevation={0}
        sx={{
          maxWidth: { xs: "90%", sm: "78%" },
          px: 2,
          py: 1.25,
          bgcolor: isUser ? "primary.main" : "grey.100",
          color: isUser ? "primary.contrastText" : "text.primary",
          borderRadius: 2,
          ...(isUser ? { borderTopRightRadius: 4 } : { borderTopLeftRadius: 4 }),
        }}
      >
        {isUser ? (
          <Typography variant="body2" sx={{ whiteSpace: "pre-wrap" }}>
            {message.content}
          </Typography>
        ) : (
          <Box
            sx={{
              fontSize: 14,
              "& p": { m: 0, mb: 1 },
              "& p:last-child": { mb: 0 },
              "& ul, & ol": { m: 0, mb: 1, pl: 2.5 },
              "& code": {
                bgcolor: "grey.200",
                px: 0.5,
                borderRadius: 0.5,
                fontSize: 13,
              },
            }}
          >
            <ReactMarkdown>{message.content}</ReactMarkdown>
            {message.citations && <SourceList citations={message.citations} />}
          </Box>
        )}
      </Paper>
    </Box>
  );
}
