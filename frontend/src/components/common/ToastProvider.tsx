import { Alert, Button, Snackbar } from "@mui/material";
import { createContext, useCallback, useContext, useState, type ReactNode } from "react";

type ToastSeverity = "success" | "error" | "info";

interface ToastOptions {
  message: string;
  severity?: ToastSeverity;
  actionLabel?: string;
  onAction?: () => void;
}

interface ToastContextValue {
  showToast: (options: ToastOptions) => void;
}

const ToastContext = createContext<ToastContextValue | null>(null);

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toast, setToast] = useState<ToastOptions | null>(null);
  const [open, setOpen] = useState(false);

  const showToast = useCallback((options: ToastOptions) => {
    setToast(options);
    setOpen(true);
  }, []);

  function handleClose() {
    setOpen(false);
  }

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      <Snackbar
        open={open}
        autoHideDuration={6000}
        onClose={handleClose}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert
          severity={toast?.severity ?? "info"}
          onClose={handleClose}
          action={
            toast?.actionLabel && toast?.onAction ? (
              <Button
                color="inherit"
                size="small"
                onClick={() => {
                  toast.onAction?.();
                  handleClose();
                }}
              >
                {toast.actionLabel}
              </Button>
            ) : undefined
          }
        >
          {toast?.message}
        </Alert>
      </Snackbar>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used within a ToastProvider");
  }
  return context;
}
