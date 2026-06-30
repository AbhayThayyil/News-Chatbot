import AddCommentOutlinedIcon from "@mui/icons-material/AddCommentOutlined";
import ChatBubbleOutlineIcon from "@mui/icons-material/ChatBubbleOutlined";
import {
  Box,
  Divider,
  Drawer,
  IconButton,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
} from "@mui/material";
import type { Conversation } from "../../types/chat";

export const SIDEBAR_WIDTH = 280;

interface SidebarProps {
  open: boolean;
  variant: "permanent" | "temporary";
  conversations: Conversation[];
  onClose: () => void;
  onNewChat: () => void;
}

export function Sidebar({ open, variant, conversations, onClose, onNewChat }: SidebarProps) {
  return (
    <Drawer
      variant={variant}
      open={open}
      onClose={onClose}
      ModalProps={{ keepMounted: true }}
      sx={{
        width: SIDEBAR_WIDTH,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: SIDEBAR_WIDTH,
          boxSizing: "border-box",
          bgcolor: "grey.900",
          color: "grey.100",
        },
      }}
    >
      <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", p: 1.5 }}>
        <Typography variant="subtitle1" fontWeight={600}>
          News Chatbot
        </Typography>
        <IconButton size="small" onClick={onNewChat} sx={{ color: "grey.100" }} aria-label="New chat">
          <AddCommentOutlinedIcon fontSize="small" />
        </IconButton>
      </Box>
      <Divider sx={{ borderColor: "grey.800" }} />
      <List sx={{ overflowY: "auto" }}>
        {conversations.map((conversation) => (
          <ListItemButton key={conversation.id} sx={{ py: 1 }}>
            <ListItemIcon sx={{ minWidth: 36, color: "grey.400" }}>
              <ChatBubbleOutlineIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText
              primary={conversation.title}
              slotProps={{ primary: { noWrap: true, sx: { fontSize: 14 } } }}
            />
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  );
}
