import { useQuery } from "@tanstack/react-query";
import { Alert, Box, CircularProgress, Typography } from "@mui/material";
import { getHealth } from "../api/health";

export function HomePage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["health"],
    queryFn: getHealth,
  });

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        AI News Chatbot
      </Typography>
      {isLoading && <CircularProgress size={24} />}
      {isError && <Alert severity="error">Could not reach backend</Alert>}
      {data && <Alert severity="success">Backend status: {data.status}</Alert>}
    </Box>
  );
}
