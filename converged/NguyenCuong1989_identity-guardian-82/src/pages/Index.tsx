import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";
import { useRealtimeSubscription } from "@/hooks/useRealtimeSubscription";
import { DashboardHeader } from "@/components/dashboard/DashboardHeader";
import { AxesPanel } from "@/components/dashboard/AxesPanel";
import { IdentityCoveragePanel } from "@/components/dashboard/IdentityCoveragePanel";
import { LogicBankPanel } from "@/components/dashboard/LogicBankPanel";
import { TaskMonitorPanel } from "@/components/dashboard/TaskMonitorPanel";
import { DriftEventsPanel } from "@/components/dashboard/DriftEventsPanel";
import { SlaMetricsPanel } from "@/components/dashboard/SlaMetricsPanel";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Loader2 } from "lucide-react";

const Index = () => {
  const { user, isLoading } = useAuth();
  const navigate = useNavigate();

  // Enable realtime subscriptions for all dashboard tables
  useRealtimeSubscription([
    "entity_state",
    "logic_modules",
    "tasks",
    "drift_events",
    "sla_metrics",
  ]);

  useEffect(() => {
    if (!isLoading && !user) {
      navigate("/auth");
    }
  }, [user, isLoading, navigate]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />
      
      <main className="container mx-auto px-4 py-6">
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 lg:w-auto lg:inline-flex">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="identity">Identity</TabsTrigger>
            <TabsTrigger value="execution">Execution</TabsTrigger>
            <TabsTrigger value="signals">Signals</TabsTrigger>
          </TabsList>
          
          <TabsContent value="overview" className="space-y-6">
            <div className="grid gap-6 md:grid-cols-2">
              <AxesPanel />
              <IdentityCoveragePanel />
            </div>
            <div className="grid gap-6 md:grid-cols-2">
              <TaskMonitorPanel />
              <DriftEventsPanel />
            </div>
          </TabsContent>
          
          <TabsContent value="identity" className="space-y-6">
            <div className="grid gap-6 md:grid-cols-2">
              <AxesPanel />
              <IdentityCoveragePanel />
            </div>
            <LogicBankPanel />
          </TabsContent>
          
          <TabsContent value="execution" className="space-y-6">
            <div className="grid gap-6 md:grid-cols-2">
              <TaskMonitorPanel />
              <SlaMetricsPanel />
            </div>
          </TabsContent>
          
          <TabsContent value="signals" className="space-y-6">
            <div className="grid gap-6 md:grid-cols-2">
              <DriftEventsPanel />
              <SlaMetricsPanel />
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
};

export default Index;
