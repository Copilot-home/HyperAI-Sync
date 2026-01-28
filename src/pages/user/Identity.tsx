import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { DataPanel, DataRow } from "@/components/ecvm/DataPanel";
import { StatusBadge } from "@/components/ecvm/StatusBadge";
import { CoverageIndicator } from "@/components/ecvm/CoverageIndicator";
import { useEntityState } from "@/hooks/useEntityState";
import { User, Upload, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { format } from "date-fns";

export default function Identity() {
  const { data: entityState, isLoading, error } = useEntityState();

  return (
    <AppLayout>
      <PageHeader
        title="Identity State"
        subtitle="GET /v1/entity/state"
        icon={<User className="h-5 w-5 text-muted-foreground" />}
      />

      <div className="p-6 space-y-6">
        {isLoading && (
          <div className="ecvm-panel">
            <div className="flex items-center gap-2 text-muted-foreground">
              <RefreshCw className="h-4 w-4 animate-spin" />
              <span className="font-mono text-sm">Fetching entity state...</span>
            </div>
          </div>
        )}

        {error && (
          <div className="ecvm-panel border-status-reject/30 bg-status-reject-bg">
            <div className="text-sm font-mono text-status-reject-foreground">
              Error: Failed to fetch entity state
            </div>
          </div>
        )}

        {entityState && (
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
                  label="Reference Uploaded" 
                  value={entityState.reference_uploaded ? "YES" : "NO"} 
                />
                <DataRow 
                  label="Last Sync" 
                  value={format(new Date(entityState.last_sync), "yyyy-MM-dd HH:mm:ss")} 
                />
              </div>
            </DataPanel>

            {/* Coverage Panel */}
            <DataPanel title="Coverage Metrics" icon={<RefreshCw className="h-3.5 w-3.5" />}>
              <div className="space-y-4">
                <CoverageIndicator percent={entityState.coverage_percent} />
                <DataRow label="Variance" value={`${(entityState.variance * 100).toFixed(2)}%`} />
                <DataRow label="Version" value={entityState.metadata.version as string} />
                <DataRow label="Region" value={entityState.metadata.region as string} />
              </div>
            </DataPanel>

            {/* Reference Upload CTA */}
            <div className="lg:col-span-2">
              <DataPanel title="Reference Management">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">
                      Upload or update reference materials for identity verification.
                    </p>
                    <p className="text-xs font-mono text-muted-foreground mt-1">
                      POST /v1/entity/reference
                    </p>
                  </div>
                  <Button variant="outline" className="font-mono text-sm">
                    <Upload className="h-4 w-4 mr-2" />
                    Upload Reference
                  </Button>
                </div>
              </DataPanel>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
