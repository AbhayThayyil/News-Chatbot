import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";
import DeleteOutlineOutlinedIcon from "@mui/icons-material/DeleteOutlineOutlined";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import MenuIcon from "@mui/icons-material/Menu";
import { AppBar, IconButton, Toolbar, Tooltip, Typography } from "@mui/material";
import { useColorMode } from "../../theme/ColorModeProvider";

interface HeaderProps {
  onMenuClick: () => void;
  showMenuButton: boolean;
  onClearChat: () => void;
  canClearChat: boolean;
}

export function Header({ onMenuClick, showMenuButton, onClearChat, canClearChat }: HeaderProps) {
  const { mode, toggleColorMode } = useColorMode();

  return (
    <AppBar
      position="sticky"
      elevation={0}
      sx={{
        bgcolor: "background.paper",
        color: "text.primary",
        borderBottom: "1px solid",
        borderColor: "divider",
      }}
    >
      <Toolbar variant="dense">
        {showMenuButton && (
          <IconButton edge="start" onClick={onMenuClick} sx={{ mr: 1 }} aria-label="Open sidebar">
            <MenuIcon />
          </IconButton>
        )}
        <Typography variant="subtitle1" fontWeight={600} sx={{ flex: 1 }}>
          AI News Chatbot
        </Typography>
        <Tooltip title="Clear chat">
          <span>
            <IconButton onClick={onClearChat} disabled={!canClearChat} aria-label="Clear chat">
              <DeleteOutlineOutlinedIcon fontSize="small" />
            </IconButton>
          </span>
        </Tooltip>
        <Tooltip title={mode === "dark" ? "Switch to light mode" : "Switch to dark mode"}>
          <IconButton onClick={toggleColorMode} aria-label="Toggle color mode">
            {mode === "dark" ? (
              <LightModeOutlinedIcon fontSize="small" />
            ) : (
              <DarkModeOutlinedIcon fontSize="small" />
            )}
          </IconButton>
        </Tooltip>
      </Toolbar>
    </AppBar>
  );
}
