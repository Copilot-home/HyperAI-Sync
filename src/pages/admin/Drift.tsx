import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { useDrift } from "@/hooks/useAdminData";
import { Activity, RefreshCw, CheckCircle, XCircle } from "lucide-react";
import { format } from "date-fns";

export default function Drift() {
  const { data: drift, isLoading } = useDrift();

  return (
    <AppLayout>
      <PageHeader
        title="Drift Monitoring"
        subtitle="service_role context (read-only)"
        icon={<Activity className="h-5 w-5 text-muted-foreground" />}
      />

      <div className="p-6">
        <div className="ecvm-panel overflow-hidden">
          {isLoading ? (
            <div className="flex items-center gap-2 text-muted-foreground p-4">
              <RefreshCw className="h-4 w-4 animate-spin" />
              <span className="font-mono text-sm">Loading drift data...</span>
            </div>
          ) : drift && drift.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="ecvm-table">
                <thead>
                  <tr>
                    <th>Entity ID</th>
                    <th>Drift Type</th>
                    <th>Baseline</th>
                    <th>Current</th>
                    <th>Delta</th>
                    <th>Acknowledged</th>
                    <th>Detected</th>
                  </tr>
                </thead>
                <tbody>
                  {drift.map((entry) => (
                    <tr key={entry.id}>
                      <td className="font-mono">{entry.entity_id}</td>
                      <td className="font-mono">{entry.drift_type}</td>
                      <td className="text-muted-foreground">
                        {entry.baseline.toFixed(3)}
                      </td>
                      <td className="text-muted-foreground">
                        {entry.current.toFixed(3)}
                      </td>
                      <td className="text-status-halt font-medium">
                        -{entry.delta.toFixed(3)}
                      </td>
                      <td>
                        {entry.acknowledged ? (
                          <CheckCircle className="h-4 w-4 text-status-pass" />
                        ) : (
                          <XCircle className="h-4 w-4 text-status-reject" />
                        )}
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
              <Activity className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p className="font-mono text-sm">No drift detected</p>
            </div>
          )}
        </div>
      </div>
    </AppLayout>
  );
}
