import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { useUnmetLogic } from "@/hooks/useAdminData";
import { AlertTriangle, RefreshCw, AlertCircle, Trash2 } from "lucide-react";
import { format } from "date-fns";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const severityStyles: Record<string, string> = {
  low: "bg-status-pending-bg text-status-pending-foreground",
  medium: "bg-status-halt-bg text-status-halt-foreground",
  high: "bg-status-reject-bg text-status-reject-foreground",
  critical: "bg-status-reject text-white",
};

const severityOrder: Record<string, number> = {
  critical: 0,
  high: 1,
  medium: 2,
  low: 3,
};

export default function UnmetLogic() {
  const { data: unmetLogic, isLoading, error, refetch } = useUnmetLogic();

  // Sort by severity
  const sortedUnmetLogic = [...(unmetLogic ?? [])].sort(
    (a, b) => (severityOrder[a.severity] ?? 4) - (severityOrder[b.severity] ?? 4)
  );

  const criticalCount = unmetLogic?.filter(s => s.severity === "critical").length ?? 0;
  const highCount = unmetLogic?.filter(s => s.severity === "high").length ?? 0;

  return (
    <AppLayout>
      <PageHeader
        title="Unmet Logic Signals"
        subtitle="GET /v1/admin/logic/unmet (service_role)"
        icon={<AlertTriangle className="h-5 w-5 text-muted-foreground" />}
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
        {/* Alert Banner */}
        {(criticalCount > 0 || highCount > 0) && (
          <div className={cn(
            "ecvm-panel flex items-start gap-3",
            criticalCount > 0 ? "border-status-reject/50 bg-status-reject-bg" : "border-status-halt/50 bg-status-halt-bg"
          )}>
            <AlertTriangle className={cn(
              "h-5 w-5 mt-0.5",
              criticalCount > 0 ? "text-status-reject" : "text-status-halt"
            )} />
            <div>
              <div className={cn(
                "text-sm font-medium",
                criticalCount > 0 ? "text-status-reject-foreground" : "text-status-halt-foreground"
              )}>
                {criticalCount > 0 
                  ? `${criticalCount} critical signal(s) require immediate attention`
                  : `${highCount} high-severity signal(s) pending review`
                }
              </div>
              <div className="text-xs text-muted-foreground mt-1">
                Admin action required: Review signals and synthesize logic or dismiss
              </div>
            </div>
          </div>
        )}

        {/* Main Table */}
        <div className="ecvm-panel overflow-hidden">
          {isLoading ? (
            <div className="flex items-center gap-2 text-muted-foreground p-4">
              <RefreshCw className="h-4 w-4 animate-spin" />
              <span className="font-mono text-sm">Loading unmet logic signals...</span>
            </div>
          ) : error ? (
            <div className="p-4 bg-status-reject-bg">
              <div className="flex items-start gap-3">
                <AlertCircle className="h-5 w-5 text-status-reject" />
                <div>
                  <div className="text-sm font-medium text-status-reject-foreground">
                    Failed to fetch unmet logic signals
                  </div>
                  <div className="text-xs font-mono text-status-reject-foreground/80 mt-1">
                    {error.message}
                  </div>
                </div>
              </div>
            </div>
          ) : sortedUnmetLogic && sortedUnmetLogic.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="ecvm-table">
                <thead>
                  <tr>
                    <th>Severity</th>
                    <th>Requested Task</th>
                    <th>Observed State</th>
                    <th>Reason</th>
                    <th>Detected</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {sortedUnmetLogic.map((entry) => (
                    <tr key={entry.id}>
                      <td>
                        <span className={cn(
                          "inline-block px-2 py-0.5 rounded text-xs font-mono uppercase",
                          severityStyles[entry.severity] ?? severityStyles.medium
                        )}>
                          {entry.severity}
                        </span>
                      </td>
                      <td className="font-mono text-xs">
                        {entry.entity_id.slice(0, 8)}...
                      </td>
                      <td>
                        <span className="inline-block px-2 py-0.5 bg-muted rounded text-xs uppercase font-mono">
                          {entry.requested_task}
                        </span>
                      </td>
                      <td>
                        <span className="inline-block px-2 py-0.5 bg-status-pending-bg text-status-pending-foreground rounded text-xs font-mono">
                          {entry.observed_state}
                        </span>
                      </td>
                      <td className="text-muted-foreground max-w-xs">
                        <div className="truncate" title={entry.reason}>
                          {entry.reason || "—"}
                        </div>
                      </td>
                      <td className="text-muted-foreground whitespace-nowrap">
                        {format(new Date(entry.detected_at), "yyyy-MM-dd HH:mm")}
                      </td>
                      <td>
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-7 px-2 text-muted-foreground hover:text-status-reject"
                          title="Dismiss signal (after logic synthesis)"
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-8 text-center text-muted-foreground">
              <AlertTriangle className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p className="font-mono text-sm">No unmet logic signals</p>
              <p className="text-xs mt-1">
                All user capability requests are satisfied
              </p>
            </div>
          )}
        </div>

        {/* ECVM Flow Reference */}
        <div className="ecvm-reason-panel">
          <div className="text-xs font-medium text-foreground/80 mb-2">
            Unmet Logic Flow (ECVM-CS-1.0)
          </div>
          <div className="text-xs text-disabled-foreground space-y-1">
            <div>1. User Node attempts task with unavailable logic</div>
            <div>2. POST /v1/logic/unmet creates signal</div>
            <div>3. Admin reviews and synthesizes new logic module</div>
            <div>4. POST /v1/admin/logic/module creates module</div>
            <div>5. POST /v1/admin/logic/enable activates module</div>
            <div>6. Signal deleted after resolution</div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
