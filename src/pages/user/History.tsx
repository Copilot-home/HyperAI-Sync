import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { StatusBadge } from "@/components/ecvm/StatusBadge";
import { useTaskHistory } from "@/hooks/useTaskHistory";
import { History, RefreshCw } from "lucide-react";
import { format } from "date-fns";

export default function HistoryPage() {
  const { data: history, isLoading, error } = useTaskHistory();

  return (
    <AppLayout>
      <PageHeader
        title="Execution History"
        subtitle="task_execution_log (read-only)"
        icon={<History className="h-5 w-5 text-muted-foreground" />}
      />

      <div className="p-6">
        <div className="ecvm-panel overflow-hidden">
          {isLoading && (
            <div className="flex items-center gap-2 text-muted-foreground p-4">
              <RefreshCw className="h-4 w-4 animate-spin" />
              <span className="font-mono text-sm">Loading history...</span>
            </div>
          )}

          {error && (
            <div className="p-4 text-sm font-mono text-status-reject-foreground bg-status-reject-bg">
              Error: Failed to fetch execution history
            </div>
          )}

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
                      <td className="font-mono">{log.task_id}</td>
                      <td>
                        <span className="inline-block px-2 py-0.5 bg-muted rounded text-xs uppercase">
                          {log.task_type}
                        </span>
                      </td>
                      <td>
                        <StatusBadge status={log.verdict} />
                      </td>
                      <td>
                        <div className="flex flex-wrap gap-1">
                          {log.logic_applied.map((logicId) => (
                            <span
                              key={logicId}
                              className="text-[10px] font-mono bg-muted px-1.5 py-0.5 rounded"
                            >
                              {logicId}
                            </span>
                          ))}
                        </div>
                      </td>
                      <td className="text-muted-foreground">
                        {log.execution_time_ms}ms
                      </td>
                      <td className="text-muted-foreground">
                        {format(new Date(log.executed_at), "yyyy-MM-dd HH:mm:ss")}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {history && history.length === 0 && (
            <div className="p-8 text-center text-muted-foreground">
              <History className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p className="font-mono text-sm">No execution history</p>
            </div>
          )}
        </div>
      </div>
    </AppLayout>
  );
}
