import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { HomePage } from "./pages/HomePage";
import { ChatPage } from "./pages/ChatPage";
import { ToastProvider } from "./components/common/ToastProvider";
import { ColorModeProvider } from "./theme/ColorModeProvider";

const queryClient = new QueryClient();

function App() {
  return (
    <ColorModeProvider>
      <QueryClientProvider client={queryClient}>
        <ToastProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<ChatPage />} />
              <Route path="/status" element={<HomePage />} />
            </Routes>
          </BrowserRouter>
        </ToastProvider>
      </QueryClientProvider>
    </ColorModeProvider>
  );
}

export default App;
