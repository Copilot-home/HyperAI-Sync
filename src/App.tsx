import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";

// User Pages
import Identity from "./pages/user/Identity";
import Generate from "./pages/user/Generate";
import HistoryPage from "./pages/user/History";
import SettingsPage from "./pages/user/Settings";

// Admin Pages
import AdminOverview from "./pages/admin/Overview";
import LogicBank from "./pages/admin/LogicBank";
import UnmetLogic from "./pages/admin/UnmetLogic";
import Drift from "./pages/admin/Drift";
import Audit from "./pages/admin/Audit";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false, // No retries per ECVM spec
      refetchOnWindowFocus: false,
    },
  },
});

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          
          {/* User Routes */}
          <Route path="/app/user/identity" element={<Identity />} />
          <Route path="/app/user/generate" element={<Generate />} />
          <Route path="/app/user/history" element={<HistoryPage />} />
          <Route path="/app/user/settings" element={<SettingsPage />} />
          
          {/* Admin Routes */}
          <Route path="/app/admin/overview" element={<AdminOverview />} />
          <Route path="/app/admin/logic-bank" element={<LogicBank />} />
          <Route path="/app/admin/unmet-logic" element={<UnmetLogic />} />
          <Route path="/app/admin/drift" element={<Drift />} />
          <Route path="/app/admin/audit" element={<Audit />} />
          
          {/* Redirects */}
          <Route path="/app" element={<Navigate to="/app/user/identity" replace />} />
          <Route path="/app/user" element={<Navigate to="/app/user/identity" replace />} />
          <Route path="/app/admin" element={<Navigate to="/app/admin/overview" replace />} />
          
          {/* Catch-all */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
