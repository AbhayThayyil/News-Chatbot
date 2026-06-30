import MenuIcon from "@mui/icons-material/Menu";
import { AppBar, IconButton, Toolbar, Typography } from "@mui/material";

interface HeaderProps {
  onMenuClick: () => void;
  showMenuButton: boolean;
}

export function Header({ onMenuClick, showMenuButton }: HeaderProps) {
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
        <Typography variant="subtitle1" fontWeight={600}>
          AI News Chatbot
        </Typography>
      </Toolbar>
    </AppBar>
  );
}
