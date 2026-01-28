import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { useDrift } from "@/hooks/useAdminData";
import { Activity, RefreshCw, CheckCircle, XCircle, AlertCircle, AlertTriangle } from "lucide-react";
import { format } from "date-fns";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

// ECVM: Drift taxonomy per spec
const driftTypeInfo: Record<string, { label: string; description: string; authority: string }> = {
  PER_NODE: {
    label: "Per-Node Drift",
    description: "Single user node - insufficient personal data",
    authority: "User Node",
  },
  SYSTEMIC: {
    label: "Systemic Drift",
    description: "Multiple nodes affected - LogicModule mismatch",
    authority: "Admin Node",
  },
};

export default function Drift() {
  const { data: drift, isLoading, error, refetch } = useDrift();

  const perNodeCount = drift?.filter(d => d.drift_type === "PER_NODE").length ?? 0;
  const systemicCount = drift?.filter(d => d.drift_type === "SYSTEMIC").length ?? 0;
  const unacknowledgedCount = drift?.filter(d => !d.acknowledged).length ?? 0;

  return (
    <AppLayout>
      <PageHeader
        title="Drift Monitoring"
        subtitle="GET /v1/admin/drift/events (service_role)"
        icon={<Activity className="h-5 w-5 text-muted-foreground" />}
        actions={
          <Button
            variant="outline"
            size="sm"
            onClick={() => refetch()}
            disabled={isLoading}
            className="font-mono text-xs"
          >
            <RefreshCw className={cn("h-3.5 w-3.5 mr-2", isLoading && "animate-spin")} />
            Refresh
          </Button>
        }
      />

      <div className="p-6 space-y-6">
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className={cn(
            "ecvm-panel",
            perNodeCount > 0 && "border-status-halt/50"
          )}>
            <div className="text-xs font-mono uppercase tracking-wider text-muted-foreground mb-1">
              Per-Node Drift
            </div>
            <div className="text-2xl font-mono font-semibold">{perNodeCount}</div>
            <div className="text-xs text-muted-foreground mt-1">
              Authority: User Node
            </div>
          </div>
          <div className={cn(
            "ecvm-panel",
            systemicCount > 0 && "border-status-reject/50"
          )}>
            <div className="text-xs font-mono uppercase tracking-wider text-muted-foreground mb-1">
              Systemic Drift
            </div>
            <div className="text-2xl font-mono font-semibold">{systemicCount}</div>
            <div className="text-xs text-muted-foreground mt-1">
              Authority: Admin Node
            </div>
          </div>
          <div className={cn(
            "ecvm-panel",
            unacknowledgedCount > 0 && "border-status-halt/50"
          )}>
            <div className="text-xs font-mono uppercase tracking-wider text-muted-foreground mb-1">
              Unacknowledged
            </div>
            <div className="text-2xl font-mono font-semibold">{unacknowledgedCount}</div>
            <div className="text-xs text-muted-foreground mt-1">
              Requires attention
            </div>
          </div>
        </div>

        {/* Main Table */}
        <div className="ecvm-panel overflow-hidden">
          {isLoading ? (
            <div className="flex items-center gap-2 text-muted-foreground p-4">
              <RefreshCw className="h-4 w-4 animate-spin" />
              <span className="font-mono text-sm">Loading drift data...</span>
            </div>
          ) : error ? (
            <div className="p-4 bg-status-reject-bg">
              <div className="flex items-start gap-3">
                <AlertCircle className="h-5 w-5 text-status-reject" />
                <div>
                  <div className="text-sm font-medium text-status-reject-foreground">
                    Failed to fetch drift events
                  </div>
                  <div className="text-xs font-mono text-status-reject-foreground/80 mt-1">
                    {error.message}
                  </div>
                </div>
              </div>
            </div>
          ) : drift && drift.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="ecvm-table">
                <thead>
                  <tr>
                    <th>Drift Type</th>
                    <th>Entity ID</th>
                    <th>Logic ID</th>
                    <th>Baseline</th>
                    <th>Current</th>
                    <th>Delta</th>
                    <th>Acknowledged</th>
                    <th>Detected</th>
                  </tr>
                </thead>
                <tbody>
                  {drift.map((entry) => {
                    const typeInfo = driftTypeInfo[entry.drift_type];
                    return (
                      <tr key={entry.id}>
                        <td>
                          <div className="flex items-center gap-2">
                            {entry.drift_type === "SYSTEMIC" ? (
                              <AlertTriangle className="h-4 w-4 text-status-reject" />
                            ) : (
                              <AlertCircle className="h-4 w-4 text-status-halt" />
                            )}
                            <div>
                              <div className={cn(
                                "text-xs font-mono uppercase px-1.5 py-0.5 rounded",
                                entry.drift_type === "SYSTEMIC" 
                                  ? "bg-status-reject-bg text-status-reject-foreground"
                                  : "bg-status-halt-bg text-status-halt-foreground"
                              )}>
                                {entry.drift_type}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="font-mono text-xs">
                          {entry.entity_id ? `${entry.entity_id.slice(0, 8)}...` : "—"}
                        </td>
                        <td className="font-mono text-xs">
                          {entry.drift_type === "SYSTEMIC" && entry.id 
                            ? `${entry.id.slice(0, 8)}...` 
                            : "—"}
                        </td>
                        <td className="text-muted-foreground font-mono">
                          {entry.baseline.toFixed(3)}
                        </td>
                        <td className="text-muted-foreground font-mono">
                          {entry.current.toFixed(3)}
                        </td>
                        <td className={cn(
                          "font-mono font-medium",
                          entry.delta > 0 ? "text-status-reject" : "text-status-pass"
                        )}>
                          {entry.delta > 0 ? "+" : ""}{entry.delta.toFixed(3)}
                        </td>
                        <td>
                          {entry.acknowledged ? (
                            <CheckCircle className="h-4 w-4 text-status-pass" />
                          ) : (
                            <XCircle className="h-4 w-4 text-status-reject" />
                          )}
                        </td>
                        <td className="text-muted-foreground whitespace-nowrap">
                          {format(new Date(entry.detected_at), "yyyy-MM-dd HH:mm")}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-8 text-center text-muted-foreground">
              <Activity className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p className="font-mono text-sm">No drift detected</p>
              <p className="text-xs mt-1">
                System is operating within normal variance bounds
              </p>
            </div>
          )}
        </div>

        {/* ECVM Drift Taxonomy Reference */}
        <div className="ecvm-reason-panel">
          <div className="text-xs font-medium text-foreground/80 mb-2">
            Drift Taxonomy (ECVM-CS-1.0)
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            {Object.entries(driftTypeInfo).map(([type, info]) => (
              <div key={type}>
                <div className="font-mono font-medium">{info.label}</div>
                <div className="text-disabled-foreground">{info.description}</div>
                <div className="text-disabled-foreground mt-1">
                  Resolution authority: <span className="text-foreground/70">{info.authority}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
