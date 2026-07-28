import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { useLogicBank } from "@/hooks/useAdminData";
import { useToggleLogic } from "@/hooks/useLogicBankMutation";
import { Database, RefreshCw, AlertCircle, Power, Loader2 } from "lucide-react";
import { format } from "date-fns";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { toast } from "sonner";
import { useState } from "react";

const statusStyles: Record<string, string> = {
  active: "bg-status-pass-bg text-status-pass-foreground",
  deprecated: "bg-status-reject-bg text-status-reject-foreground",
  draft: "bg-status-pending-bg text-status-pending-foreground",
};

export default function LogicBank() {
  const { data: logicBank, isLoading, error, refetch } = useLogicBank();
  const toggleMutation = useToggleLogic();
  const [togglingId, setTogglingId] = useState<string | null>(null);

  const activeCount = logicBank?.filter(l => l.status === "active").length ?? 0;
  const draftCount = logicBank?.filter(l => l.status === "draft").length ?? 0;

  // ECVM: Toggle uses 'enabled' field, not 'status'
  const handleToggle = async (logicId: string, currentlyEnabled: boolean) => {
    const newEnabled = !currentlyEnabled;
    setTogglingId(logicId);
    
    try {
      await toggleMutation.mutateAsync({ 
        logic_id: logicId, 
        enabled: newEnabled 
      });
      toast.success(`Logic module ${newEnabled ? "enabled" : "disabled"}`);
    } catch (error) {
      toast.error(`Failed to toggle: ${error instanceof Error ? error.message : "Unknown error"}`);
    } finally {
      setTogglingId(null);
    }
  };

  return (
    <AppLayout>
      <PageHeader
        title="Logic Bank"
        subtitle="Internal Logic Brain (service_role)"
        icon={<Database className="h-5 w-5 text-muted-foreground" />}
        actions={
          <div className="flex items-center gap-2">
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
          </div>
        }
      />

      <div className="p-6 space-y-6">
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="ecvm-panel">
            <div className="text-xs font-mono uppercase tracking-wider text-muted-foreground mb-1">
              Total Modules
            </div>
            <div className="text-2xl font-mono font-semibold">
              {logicBank?.length ?? 0}
            </div>
          </div>
          <div className="ecvm-panel border-status-pass/30">
            <div className="text-xs font-mono uppercase tracking-wider text-muted-foreground mb-1">
              Active
            </div>
            <div className="text-2xl font-mono font-semibold text-status-pass">
              {activeCount}
            </div>
          </div>
          <div className="ecvm-panel border-status-pending/30">
            <div className="text-xs font-mono uppercase tracking-wider text-muted-foreground mb-1">
              Draft
            </div>
            <div className="text-2xl font-mono font-semibold text-status-pending">
              {draftCount}
            </div>
          </div>
        </div>

        {/* Main Table */}
        <div className="ecvm-panel overflow-hidden">
          {isLoading ? (
            <div className="flex items-center gap-2 text-muted-foreground p-4">
              <RefreshCw className="h-4 w-4 animate-spin" />
              <span className="font-mono text-sm">Loading logic bank...</span>
            </div>
          ) : error ? (
            <div className="p-4 bg-status-reject-bg">
              <div className="flex items-start gap-3">
                <AlertCircle className="h-5 w-5 text-status-reject" />
                <div>
                  <div className="text-sm font-medium text-status-reject-foreground">
                    Failed to fetch logic bank
                  </div>
                  <div className="text-xs font-mono text-status-reject-foreground/80 mt-1">
                    {error.message}
                  </div>
                </div>
              </div>
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
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {logicBank.map((entry) => (
                    <tr key={entry.logic_id}>
                      <td className="font-mono text-xs">
                        {entry.logic_id.slice(0, 8)}...
                      </td>
                      <td>
                        <div>
                          <div className="font-medium">{entry.name}</div>
                          <div className="text-xs text-muted-foreground max-w-xs truncate">
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
                      <td className="text-muted-foreground whitespace-nowrap">
                        {format(new Date(entry.updated_at), "yyyy-MM-dd")}
                      </td>
                      <td>
                        <div className="flex items-center gap-1">
                          <Button
                            variant="ghost"
                            size="sm"
                            className={cn(
                              "h-7 px-2",
                              entry.status === "active" 
                                ? "text-status-pass hover:text-status-reject"
                                : "text-muted-foreground hover:text-status-pass"
                            )}
                            title={entry.status === "active" ? "Disable module" : "Enable module"}
                            onClick={() => handleToggle(entry.logic_id, entry.enabled)}
                            disabled={togglingId === entry.logic_id}
                          >
                            {togglingId === entry.logic_id ? (
                              <Loader2 className="h-3.5 w-3.5 animate-spin" />
                            ) : (
                              <Power className="h-3.5 w-3.5" />
                            )}
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-8 text-center text-muted-foreground">
              <Database className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p className="font-mono text-sm">No logic modules</p>
              <p className="text-xs mt-1">
                Logic Bank is empty. Synthesize modules from unmet signals.
              </p>
            </div>
          )}
        </div>

        {/* ECVM Logic Bank Reference */}
        <div className="ecvm-reason-panel">
          <div className="text-xs font-medium text-foreground/80 mb-2">
            Logic Bank (ECVM-CS-1.0)
          </div>
          <div className="text-xs text-disabled-foreground space-y-1">
            <div>• Logic Bank is the internal logic brain of the system</div>
            <div>• Each LogicModule defines: task_type, required_identity_state, drift_risk_profile</div>
            <div>• Logic is endogenously synthesized from operation</div>
            <div>• enabled = false by default (explicit enable required)</div>
            <div>• Version history tracked for audit (logic_version_history)</div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
