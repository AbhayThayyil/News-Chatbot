import { Box, useMediaQuery, useTheme } from "@mui/material";
import { useState } from "react";
import type { Conversation } from "../../types/chat";
import { Header } from "./Header";
import { Sidebar } from "./Sidebar";

const MOCK_CONVERSATIONS: Conversation[] = [
  { id: "1", title: "Today's AI news" },
  { id: "2", title: "Formula 1 updates" },
  { id: "3", title: "India market summary" },
];

interface AppShellProps {
  children: React.ReactNode;
  onClearChat: () => void;
  canClearChat: boolean;
}

export function AppShell({ children, onClearChat, canClearChat }: AppShellProps) {
  const theme = useTheme();
  const isDesktop = useMediaQuery(theme.breakpoints.up("md"));
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <Box sx={{ display: "flex", height: "100vh" }}>
      <Sidebar
        open={isDesktop ? true : mobileOpen}
        variant={isDesktop ? "permanent" : "temporary"}
        conversations={MOCK_CONVERSATIONS}
        onClose={() => setMobileOpen(false)}
        onNewChat={() => setMobileOpen(false)}
      />
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          flex: 1,
          minWidth: 0,
        }}
      >
        <Header
          onMenuClick={() => setMobileOpen(true)}
          showMenuButton={!isDesktop}
          onClearChat={onClearChat}
          canClearChat={canClearChat}
        />
        <Box sx={{ flex: 1, minHeight: 0 }}>{children}</Box>
      </Box>
    </Box>
  );
}
