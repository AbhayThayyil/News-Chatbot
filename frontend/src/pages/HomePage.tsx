import { useQuery } from "@tanstack/react-query";
import { Alert, Box, CircularProgress, Stack, Typography } from "@mui/material";
import { getHealth } from "../api/health";
import { sendChatMessage } from "../api/chat";
import { searchNews } from "../api/news";

export function HomePage() {
  const health = useQuery({
    queryKey: ["health"],
    queryFn: getHealth,
  });

  const chat = useQuery({
    queryKey: ["chat-test"],
    queryFn: () => sendChatMessage({ message: "Latest AI news" }),
  });

  const news = useQuery({
    queryKey: ["news-test"],
    queryFn: () => searchNews({ query: "formula 1", max_results: 3 }),
  });

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Backend Connectivity Check
      </Typography>
      <Stack spacing={2} sx={{ maxWidth: 600 }}>
        <Box>
          <Typography variant="subtitle2">GET /health</Typography>
          {health.isLoading && <CircularProgress size={20} />}
          {health.isError && <Alert severity="error">Could not reach backend</Alert>}
          {health.data && <Alert severity="success">status: {health.data.status}</Alert>}
        </Box>

        <Box>
          <Typography variant="subtitle2">POST /chat</Typography>
          {chat.isLoading && <CircularProgress size={20} />}
          {chat.isError && <Alert severity="error">Request failed</Alert>}
          {chat.data && <Alert severity="success">{chat.data.reply}</Alert>}
        </Box>

        <Box>
          <Typography variant="subtitle2">POST /news/search</Typography>
          {news.isLoading && <CircularProgress size={20} />}
          {news.isError && <Alert severity="error">Request failed</Alert>}
          {news.data && (
            <Alert severity="success">{news.data.articles.length} articles returned</Alert>
          )}
        </Box>
      </Stack>
    </Box>
  );
}
