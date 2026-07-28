import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { DataPanel } from "@/components/ecvm/DataPanel";
import { useAdminOverview } from "@/hooks/useAdminData";
import { LayoutDashboard, Users, CheckCircle, AlertTriangle, Activity, RefreshCw } from "lucide-react";
import { cn } from "@/lib/utils";

interface MetricCardProps {
  label: string;
  value: string | number;
  icon: React.ReactNode;
  trend?: "up" | "down" | "neutral";
  alert?: boolean;
}

function MetricCard({ label, value, icon, alert }: MetricCardProps) {
  return (
    <div className={cn(
      "ecvm-panel",
      alert && "border-status-halt/50"
    )}>
      <div className="flex items-start justify-between">
        <div>
          <div className="text-xs font-mono uppercase tracking-wider text-muted-foreground mb-1">
            {label}
          </div>
          <div className="text-2xl font-mono font-semibold">
            {value}
          </div>
        </div>
        <div className={cn(
          "p-2 rounded-md",
          alert ? "bg-status-halt-bg" : "bg-muted"
        )}>
          {icon}
        </div>
      </div>
    </div>
  );
}

export default function AdminOverview() {
  const { data: overview, isLoading } = useAdminOverview();

  return (
    <AppLayout>
      <PageHeader
        title="Admin Overview"
        subtitle="service_role context (read-only)"
        icon={<LayoutDashboard className="h-5 w-5 text-muted-foreground" />}
      />

      <div className="p-6 space-y-6">
        {isLoading ? (
          <div className="ecvm-panel">
            <div className="flex items-center gap-2 text-muted-foreground">
              <RefreshCw className="h-4 w-4 animate-spin" />
              <span className="font-mono text-sm">Loading overview...</span>
            </div>
          </div>
        ) : overview ? (
          <>
            {/* Primary Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <MetricCard
                label="Total Entities"
                value={overview.total_entities.toLocaleString()}
                icon={<Users className="h-5 w-5 text-muted-foreground" />}
              />
              <MetricCard
                label="Active Entities"
                value={overview.active_entities.toLocaleString()}
                icon={<CheckCircle className="h-5 w-5 text-status-pass" />}
              />
              <MetricCard
                label="Tasks Today"
                value={overview.total_tasks_today.toLocaleString()}
                icon={<Activity className="h-5 w-5 text-muted-foreground" />}
              />
              <MetricCard
                label="Pass Rate"
                value={`${overview.pass_rate}%`}
                icon={<CheckCircle className="h-5 w-5 text-status-pass" />}
              />
            </div>

            {/* Alert Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <MetricCard
                label="Unmet Logic"
                value={overview.unmet_logic_count}
                icon={<AlertTriangle className="h-5 w-5 text-status-halt" />}
                alert={overview.unmet_logic_count > 0}
              />
              <MetricCard
                label="Active Drift"
                value={overview.active_drift_count}
                icon={<Activity className="h-5 w-5 text-status-halt" />}
                alert={overview.active_drift_count > 0}
              />
            </div>

            {/* System Status */}
            <DataPanel title="System Status">
              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <div className="text-xs font-mono text-muted-foreground mb-1">API</div>
                  <div className="flex items-center justify-center gap-1.5">
                    <span className="h-2 w-2 rounded-full bg-status-pass animate-pulse-subtle" />
                    <span className="text-sm font-mono">Operational</span>
                  </div>
                </div>
                <div>
                  <div className="text-xs font-mono text-muted-foreground mb-1">Database</div>
                  <div className="flex items-center justify-center gap-1.5">
                    <span className="h-2 w-2 rounded-full bg-status-pass animate-pulse-subtle" />
                    <span className="text-sm font-mono">Operational</span>
                  </div>
                </div>
                <div>
                  <div className="text-xs font-mono text-muted-foreground mb-1">Logic Engine</div>
                  <div className="flex items-center justify-center gap-1.5">
                    <span className="h-2 w-2 rounded-full bg-status-pass animate-pulse-subtle" />
                    <span className="text-sm font-mono">Operational</span>
                  </div>
                </div>
              </div>
            </DataPanel>
          </>
        ) : null}
      </div>
    </AppLayout>
  );
}
