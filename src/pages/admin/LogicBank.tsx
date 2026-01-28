import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { useLogicBank } from "@/hooks/useAdminData";
import { Database, RefreshCw } from "lucide-react";
import { format } from "date-fns";
import { cn } from "@/lib/utils";

const statusStyles = {
  active: "bg-status-pass-bg text-status-pass-foreground",
  deprecated: "bg-status-reject-bg text-status-reject-foreground",
  draft: "bg-status-pending-bg text-status-pending-foreground",
};

export default function LogicBank() {
  const { data: logicBank, isLoading } = useLogicBank();

  return (
    <AppLayout>
      <PageHeader
        title="Logic Bank"
        subtitle="service_role context (read-only)"
        icon={<Database className="h-5 w-5 text-muted-foreground" />}
      />

      <div className="p-6">
        <div className="ecvm-panel overflow-hidden">
          {isLoading ? (
            <div className="flex items-center gap-2 text-muted-foreground p-4">
              <RefreshCw className="h-4 w-4 animate-spin" />
              <span className="font-mono text-sm">Loading logic bank...</span>
            </div>
          ) : logicBank && logicBank.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="ecvm-table">
                <thead>
                  <tr>
                    <th>Logic ID</th>
                    <th>Name</th>
                    <th>Version</th>
                    <th>Status</th>
                    <th>Updated</th>
                  </tr>
                </thead>
                <tbody>
                  {logicBank.map((entry) => (
                    <tr key={entry.logic_id}>
                      <td className="font-mono">{entry.logic_id}</td>
                      <td>
                        <div>
                          <div className="font-medium">{entry.name}</div>
                          <div className="text-xs text-muted-foreground">
                            {entry.description}
                          </div>
                        </div>
                      </td>
                      <td className="font-mono text-muted-foreground">
                        v{entry.version}
                      </td>
                      <td>
                        <span className={cn(
                          "inline-block px-2 py-0.5 rounded text-xs font-mono uppercase",
                          statusStyles[entry.status]
                        )}>
                          {entry.status}
                        </span>
                      </td>
                      <td className="text-muted-foreground">
                        {format(new Date(entry.updated_at), "yyyy-MM-dd")}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-8 text-center text-muted-foreground">
              <Database className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p className="font-mono text-sm">No logic entries</p>
            </div>
          )}
        </div>
      </div>
    </AppLayout>
  );
}
