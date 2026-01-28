import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { StatusBadge } from "@/components/ecvm/StatusBadge";
import { useTaskHistory } from "@/hooks/useTaskHistory";
import { History, RefreshCw, AlertCircle, FileText } from "lucide-react";
import { format } from "date-fns";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export default function HistoryPage() {
  const { data: history, isLoading, error, refetch } = useTaskHistory();

  return (
    <AppLayout>
      <PageHeader
        title="Execution History"
        subtitle="task_execution_log (read-only)"
        icon={<History className="h-5 w-5 text-muted-foreground" />}
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

      <div className="p-6">
        <div className="ecvm-panel overflow-hidden">
          {/* Loading State */}
          {isLoading && (
            <div className="flex items-center gap-2 text-muted-foreground p-4">
              <RefreshCw className="h-4 w-4 animate-spin" />
              <span className="font-mono text-sm">Loading history...</span>
            </div>
          )}

          {/* Error State - ECVM: Fail-closed */}
          {error && (
            <div className="p-4 bg-status-reject-bg border-b border-status-reject/30">
              <div className="flex items-start gap-3">
                <AlertCircle className="h-5 w-5 text-status-reject mt-0.5" />
                <div>
                  <div className="text-sm font-medium text-status-reject-foreground">
                    Failed to fetch execution history
                  </div>
                  <div className="text-xs font-mono text-status-reject-foreground/80 mt-1">
                    {error.message || "Database query failed"}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Data Table */}
          {history && history.length > 0 && (
            <div className="overflow-x-auto">
              <table className="ecvm-table">
                <thead>
                  <tr>
                    <th>Task ID</th>
                    <th>Type</th>
                    <th>Verdict</th>
                    <th>Logic Applied</th>
                    <th>Duration</th>
                    <th>Executed At</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((log) => (
                    <tr key={log.id}>
                      <td className="font-mono text-xs">
                        {log.task_id.slice(0, 8)}...
                      </td>
                      <td>
                        <span className="inline-block px-2 py-0.5 bg-muted rounded text-xs uppercase font-mono">
                          {log.task_type}
                        </span>
                      </td>
                      <td>
                        <StatusBadge status={log.verdict} />
                      </td>
                      <td>
                        <div className="flex flex-wrap gap-1 max-w-xs">
                          {log.logic_applied.length === 0 ? (
                            <span className="text-xs text-muted-foreground">—</span>
                          ) : (
                            log.logic_applied.slice(0, 3).map((logicId, idx) => (
                              <span
                                key={idx}
                                className="text-[10px] font-mono bg-muted px-1.5 py-0.5 rounded truncate max-w-[80px]"
                                title={logicId}
                              >
                                {logicId.slice(0, 8)}...
                              </span>
                            ))
                          )}
                          {log.logic_applied.length > 3 && (
                            <span className="text-[10px] text-muted-foreground">
                              +{log.logic_applied.length - 3} more
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="text-muted-foreground font-mono">
                        {log.execution_time_ms}ms
                      </td>
                      <td className="text-muted-foreground whitespace-nowrap">
                        {format(new Date(log.executed_at), "yyyy-MM-dd HH:mm:ss")}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Empty State */}
          {history && history.length === 0 && !isLoading && (
            <div className="p-8 text-center text-muted-foreground">
              <FileText className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p className="font-mono text-sm">No execution history</p>
              <p className="text-xs mt-1">
                Task executions for your entity will appear here
              </p>
            </div>
          )}
        </div>

        {/* ECVM Notice */}
        <div className="mt-4 text-xs text-muted-foreground font-mono">
          <span className="text-foreground/60">Note:</span> Verdicts are immutable. 
          PASS = output generated. REJECT = validation failed. HALT = system stop.
        </div>
      </div>
    </AppLayout>
  );
}
