import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { DataPanel, DataRow } from "@/components/ecvm/DataPanel";
import { StatusBadge } from "@/components/ecvm/StatusBadge";
import { CoverageIndicator } from "@/components/ecvm/CoverageIndicator";
import { ReferenceUploader } from "@/components/identity/ReferenceUploader";
import { useEntityState } from "@/hooks/useEntityState";
import { useRealtimeIdentityState } from "@/hooks/useRealtimeIdentityState";
import { User, RefreshCw, AlertCircle, Shield, Upload, Radio } from "lucide-react";
import { Button } from "@/components/ui/button";
import { format } from "date-fns";
import { cn } from "@/lib/utils";

// Identity state display names per ECVM spec
const identityStateLabels: Record<string, { label: string; description: string }> = {
  NO_IDENTITY: {
    label: "No Identity",
    description: "No stable embedding established. Upload reference materials to begin.",
  },
  INSUFFICIENT: {
    label: "Insufficient",
    description: "High variance detected. Additional reference materials required.",
  },
  ESTABLISHED: {
    label: "Established",
    description: "Identity stable within bounds. Task execution enabled.",
  },
  DRIFT: {
    label: "Drift Detected",
    description: "Progressive deviation detected. Identity re-verification required.",
  },
};

export default function Identity() {
  const { data: entityState, isLoading, error, refetch } = useEntityState();

  // ECVM: Subscribe to realtime identity_state updates for live coverage % changes
  useRealtimeIdentityState(entityState?.entity_id);

  // Extract identity_state from metadata (per API response structure)
  const identityState = (entityState?.metadata?.identity_state as string) || "NO_IDENTITY";
  const isLocked = entityState?.metadata?.locked as boolean | undefined;
  const stateInfo = identityStateLabels[identityState] || identityStateLabels.NO_IDENTITY;

  return (
    <AppLayout>
      <PageHeader
        title="Identity State"
        subtitle="GET /v1/entity/state (read-only)"
        icon={<User className="h-5 w-5 text-muted-foreground" />}
        actions={
          <div className="flex items-center gap-3">
            {/* Realtime indicator */}
            {entityState?.entity_id && (
              <div className="flex items-center gap-1.5 text-xs font-mono text-muted-foreground">
                <Radio className="h-3 w-3 text-status-pass animate-pulse" />
                <span>Live</span>
              </div>
            )}
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
        {/* Loading State */}
        {isLoading && (
          <div className="ecvm-panel">
            <div className="flex items-center gap-2 text-muted-foreground">
              <RefreshCw className="h-4 w-4 animate-spin" />
              <span className="font-mono text-sm">Fetching entity state...</span>
            </div>
          </div>
        )}

        {/* Error State - ECVM: Fail-closed, show technical error */}
        {error && (
          <div className="ecvm-panel border-status-reject/30 bg-status-reject-bg">
            <div className="flex items-start gap-3">
              <AlertCircle className="h-5 w-5 text-status-reject mt-0.5" />
              <div>
                <div className="text-sm font-medium text-status-reject-foreground">
                  Failed to fetch entity state
                </div>
                <div className="text-xs font-mono text-status-reject-foreground/80 mt-1">
                  GET /v1/entity/state returned error
                </div>
              </div>
            </div>
          </div>
        )}

        {/* No Identity State - Special handling for NO_IDENTITY */}
        {entityState && !entityState.entity_id && (
          <div className="ecvm-panel border-status-halt/30">
            <div className="flex items-start gap-3">
              <Shield className="h-5 w-5 text-status-halt mt-0.5" />
              <div className="flex-1">
                <div className="text-sm font-medium">{stateInfo.label}</div>
                <div className="text-xs text-muted-foreground mt-1">
                  {stateInfo.description}
                </div>
                <div className="mt-4">
                  <Button className="font-mono text-sm">
                    <Upload className="h-4 w-4 mr-2" />
                    Upload Reference Materials
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Entity Data Display */}
        {entityState && entityState.entity_id && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Entity Info Panel */}
            <DataPanel title="Entity Information" icon={<User className="h-3.5 w-3.5" />}>
              <div className="space-y-1">
                <DataRow label="Entity ID" value={entityState.entity_id} />
                <DataRow 
                  label="Status" 
                  value={<StatusBadge status={entityState.status} />} 
                />
                <DataRow 
                  label="Identity State" 
                  value={
                    <span className={cn(
                      "font-mono text-xs px-2 py-0.5 rounded",
                      identityState === "ESTABLISHED" && "bg-status-pass-bg text-status-pass-foreground",
                      identityState === "DRIFT" && "bg-status-reject-bg text-status-reject-foreground",
                      identityState === "INSUFFICIENT" && "bg-status-halt-bg text-status-halt-foreground",
                      identityState === "NO_IDENTITY" && "bg-status-pending-bg text-status-pending-foreground"
                    )}>
                      {identityState}
                    </span>
                  } 
                />
                <DataRow 
                  label="Locked" 
                  value={isLocked ? "YES" : "NO"} 
                />
                <DataRow 
                  label="Reference Uploaded" 
                  value={entityState.reference_uploaded ? "YES" : "NO"} 
                />
                {entityState.last_sync && (
                  <DataRow 
                    label="Last Sync" 
                    value={format(new Date(entityState.last_sync), "yyyy-MM-dd HH:mm:ss")} 
                  />
                )}
              </div>
            </DataPanel>

            {/* Coverage Panel */}
            <DataPanel title="Coverage Metrics" icon={<RefreshCw className="h-3.5 w-3.5" />}>
              <div className="space-y-4">
                <CoverageIndicator percent={entityState.coverage_percent} />
                <DataRow 
                  label="Variance Score" 
                  value={`${(entityState.variance * 100).toFixed(2)}%`} 
                />
                <div className="pt-2 border-t border-border">
                  <div className="text-xs font-mono text-muted-foreground mb-2">
                    State Info
                  </div>
                  <div className="text-sm">{stateInfo.label}</div>
                  <div className="text-xs text-muted-foreground mt-1">
                    {stateInfo.description}
                  </div>
                </div>
              </div>
            </DataPanel>

            {/* Reference Upload - ECVM: Guide upload, don't force */}
            <div className="lg:col-span-2">
              <DataPanel 
                title="Reference Management" 
                icon={<Upload className="h-3.5 w-3.5" />}
              >
                <div className="space-y-4">
                  <div>
                    <p className="text-sm text-muted-foreground">
                      {identityState === "ESTABLISHED" 
                        ? "Identity is established. You can update reference materials if needed."
                        : identityState === "DRIFT"
                        ? "Drift detected. Re-upload reference materials to restore identity stability."
                        : "Upload reference materials to establish identity."
                      }
                    </p>
                    <p className="text-xs font-mono text-muted-foreground mt-1">
                      POST /v1/entity/reference
                    </p>
                  </div>
                  <ReferenceUploader />
                </div>
              </DataPanel>
            </div>

            {/* ECVM Compliance Notice */}
            <div className="lg:col-span-2">
              <div className="ecvm-reason-panel flex items-start gap-3">
                <Shield className="h-4 w-4 mt-0.5 flex-shrink-0" />
                <div>
                  <div className="text-sm font-medium text-foreground/80 mb-1">
                    Identity Immutability Notice
                  </div>
                  <div className="text-xs text-disabled-foreground">
                    Once established, identity records are immutable per ECVM-CS-1.0 specification. 
                    Entity ID and identity hashes cannot be modified. Only variance score and 
                    coverage metrics are updated by system processes.
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
