import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Lock, Shield, AlertTriangle } from "lucide-react";
import { useEntityState } from "@/hooks/useEntityState";
import { Skeleton } from "@/components/ui/skeleton";

interface LandmarkCoverage {
  name: string;
  coverage: number;
}

export function IdentityCoveragePanel() {
  const { data: entities, isLoading, error } = useEntityState();

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            Identity Coverage
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-20 w-full" />
          ))}
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            Identity Coverage
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-destructive text-sm">Failed to load entity state</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Shield className="h-5 w-5" />
          Identity Coverage
        </CardTitle>
        <CardDescription>Per-node identity preservation state (read-only)</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {entities && entities.length > 0 ? (
          entities.map((entity) => {
            const coverage = Number(entity.identity_coverage);
            const landmarks = Array.isArray(entity.landmark_coverage) 
              ? (entity.landmark_coverage as unknown as LandmarkCoverage[]) 
              : [];
            
            return (
              <div key={entity.id} className="space-y-3 rounded-lg border p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <code className="text-sm font-mono bg-muted px-2 py-1 rounded">
                      {entity.node_id}
                    </code>
                    {entity.locked && (
                      <Lock className="h-4 w-4 text-muted-foreground" />
                    )}
                  </div>
                  <Badge 
                    variant={coverage >= 80 ? "default" : coverage >= 50 ? "secondary" : "destructive"}
                  >
                    {coverage.toFixed(1)}%
                  </Badge>
                </div>
                
                <Progress value={coverage} className="h-2" />
                
                {landmarks.length > 0 && (
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    {landmarks.map((lm, idx) => (
                      <div key={idx} className="flex items-center justify-between bg-muted/50 rounded px-2 py-1">
                        <span className="text-muted-foreground">{lm.name}</span>
                        <span className="font-mono">{lm.coverage}%</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })
        ) : (
          <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
            <AlertTriangle className="h-8 w-8 mb-2" />
            <p className="text-sm">No entity states available</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
