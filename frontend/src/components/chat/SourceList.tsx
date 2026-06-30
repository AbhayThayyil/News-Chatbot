import { Box, Link, Tooltip, Typography } from "@mui/material";
import type { Citation } from "../../api/chat";
import { formatRelativeTime } from "../../utils/time";

interface SourceListProps {
  citations: Citation[];
}

function confidenceColor(confidence: number): string {
  if (confidence >= 0.85) return "success.main";
  if (confidence >= 0.65) return "warning.main";
  return "grey.500";
}

export function SourceList({ citations }: SourceListProps) {
  if (citations.length === 0) return null;

  return (
    <Box sx={{ mt: 1.5, display: "flex", flexDirection: "column", gap: 0.75 }}>
      <Typography variant="caption" color="text.secondary" fontWeight={600}>
        Sources
      </Typography>
      <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
        {citations.map((citation, index) => (
          <Tooltip
            key={citation.url}
            title={`Confidence: ${Math.round(citation.confidence * 100)}%`}
            arrow
          >
            <Link
              href={citation.url}
              target="_blank"
              rel="noopener noreferrer"
              underline="none"
              sx={{
                display: "flex",
                alignItems: "center",
                gap: 0.75,
                maxWidth: 220,
                px: 1,
                py: 0.5,
                borderRadius: 1.5,
                border: "1px solid",
                borderColor: "divider",
                color: "text.primary",
                "&:hover": { borderColor: "primary.main", bgcolor: "action.hover" },
              }}
            >
              <Box
                sx={{
                  width: 7,
                  height: 7,
                  borderRadius: "50%",
                  bgcolor: confidenceColor(citation.confidence),
                  flexShrink: 0,
                }}
              />
              <Box sx={{ minWidth: 0 }}>
                <Typography variant="caption" fontWeight={600} noWrap component="div">
                  [{index + 1}] {citation.source}
                </Typography>
                <Typography variant="caption" color="text.secondary" noWrap component="div">
                  {formatRelativeTime(citation.published_at)}
                </Typography>
              </Box>
            </Link>
          </Tooltip>
        ))}
      </Box>
    </Box>
  );
}
