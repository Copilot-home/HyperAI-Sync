import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { useAuditLog } from "@/hooks/useAdminData";
import { FileText, RefreshCw, User, Bot, Shield } from "lucide-react";
import { format } from "date-fns";
import { cn } from "@/lib/utils";

const actorIcons = {
  user: User,
  system: Bot,
  service_role: Shield,
};

export default function Audit() {
  const { data: auditLog, isLoading } = useAuditLog();

  return (
    <AppLayout>
      <PageHeader
        title="Audit Log"
        subtitle="service_role context (read-only)"
        icon={<FileText className="h-5 w-5 text-muted-foreground" />}
      />

      <div className="p-6">
        <div className="ecvm-panel overflow-hidden">
          {isLoading ? (
            <div className="flex items-center gap-2 text-muted-foreground p-4">
              <RefreshCw className="h-4 w-4 animate-spin" />
              <span className="font-mono text-sm">Loading audit log...</span>
            </div>
          ) : auditLog && auditLog.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="ecvm-table">
                <thead>
                  <tr>
                    <th>Timestamp</th>
                    <th>Action</th>
                    <th>Actor</th>
                    <th>Resource</th>
                    <th>Details</th>
                  </tr>
                </thead>
                <tbody>
                  {auditLog.map((entry) => {
                    const ActorIcon = actorIcons[entry.actor_type];
                    return (
                      <tr key={entry.id}>
                        <td className="text-muted-foreground whitespace-nowrap">
                          {format(new Date(entry.timestamp), "yyyy-MM-dd HH:mm:ss")}
                        </td>
                        <td>
                          <span className="font-mono text-sm bg-muted px-2 py-0.5 rounded">
                            {entry.action}
                          </span>
                        </td>
                        <td>
                          <div className="flex items-center gap-2">
                            <ActorIcon className="h-4 w-4 text-muted-foreground" />
                            <div>
                              <div className="text-xs text-muted-foreground uppercase">
                                {entry.actor_type}
                              </div>
                              <div className="font-mono text-xs">
                                {entry.actor_id}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td>
                          <div className="font-mono text-xs">
                            <span className="text-muted-foreground">
                              {entry.resource_type}/
                            </span>
                            {entry.resource_id}
                          </div>
                        </td>
                        <td className="text-muted-foreground text-xs font-mono max-w-xs truncate">
                          {JSON.stringify(entry.details)}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-8 text-center text-muted-foreground">
              <FileText className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p className="font-mono text-sm">No audit entries</p>
            </div>
          )}
        </div>
      </div>
    </AppLayout>
  );
}
