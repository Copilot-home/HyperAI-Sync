import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { useUnmetLogic } from "@/hooks/useAdminData";
import { AlertTriangle, RefreshCw } from "lucide-react";
import { format } from "date-fns";
import { cn } from "@/lib/utils";

const severityStyles = {
  low: "bg-status-pending-bg text-status-pending-foreground",
  medium: "bg-status-halt-bg text-status-halt-foreground",
  high: "bg-status-reject-bg text-status-reject-foreground",
  critical: "bg-status-reject text-white",
};

export default function UnmetLogic() {
  const { data: unmetLogic, isLoading } = useUnmetLogic();

  return (
    <AppLayout>
      <PageHeader
        title="Unmet Logic"
        subtitle="service_role context (read-only)"
        icon={<AlertTriangle className="h-5 w-5 text-muted-foreground" />}
      />

      <div className="p-6">
        <div className="ecvm-panel overflow-hidden">
          {isLoading ? (
            <div className="flex items-center gap-2 text-muted-foreground p-4">
              <RefreshCw className="h-4 w-4 animate-spin" />
              <span className="font-mono text-sm">Loading unmet logic...</span>
            </div>
          ) : unmetLogic && unmetLogic.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="ecvm-table">
                <thead>
                  <tr>
                    <th>Entity ID</th>
                    <th>Logic ID</th>
                    <th>Reason</th>
                    <th>Severity</th>
                    <th>Detected</th>
                  </tr>
                </thead>
                <tbody>
                  {unmetLogic.map((entry) => (
                    <tr key={entry.id}>
                      <td className="font-mono">{entry.entity_id}</td>
                      <td className="font-mono">{entry.logic_id}</td>
                      <td className="text-muted-foreground max-w-xs truncate">
                        {entry.reason}
                      </td>
                      <td>
                        <span className={cn(
                          "inline-block px-2 py-0.5 rounded text-xs font-mono uppercase",
                          severityStyles[entry.severity]
                        )}>
                          {entry.severity}
                        </span>
                      </td>
                      <td className="text-muted-foreground">
                        {format(new Date(entry.detected_at), "yyyy-MM-dd HH:mm")}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-8 text-center text-muted-foreground">
              <AlertTriangle className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p className="font-mono text-sm">No unmet logic entries</p>
            </div>
          )}
        </div>
      </div>
    </AppLayout>
  );
}
