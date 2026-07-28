import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import Auth from "./pages/Auth";
import { ProtectedRoute } from "./components/auth/ProtectedRoute";

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
          <Route path="/auth" element={<Auth />} />
          
          {/* User Routes (Protected) */}
          <Route path="/app/user/identity" element={
            <ProtectedRoute><Identity /></ProtectedRoute>
          } />
          <Route path="/app/user/generate" element={
            <ProtectedRoute><Generate /></ProtectedRoute>
          } />
          <Route path="/app/user/history" element={
            <ProtectedRoute><HistoryPage /></ProtectedRoute>
          } />
          <Route path="/app/user/settings" element={
            <ProtectedRoute><SettingsPage /></ProtectedRoute>
          } />
          
          {/* Admin Routes (Protected + Admin Required) */}
          <Route path="/app/admin/overview" element={
            <ProtectedRoute requireAdmin><AdminOverview /></ProtectedRoute>
          } />
          <Route path="/app/admin/logic-bank" element={
            <ProtectedRoute requireAdmin><LogicBank /></ProtectedRoute>
          } />
          <Route path="/app/admin/unmet-logic" element={
            <ProtectedRoute requireAdmin><UnmetLogic /></ProtectedRoute>
          } />
          <Route path="/app/admin/drift" element={
            <ProtectedRoute requireAdmin><Drift /></ProtectedRoute>
          } />
          <Route path="/app/admin/audit" element={
            <ProtectedRoute requireAdmin><Audit /></ProtectedRoute>
          } />
          
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
