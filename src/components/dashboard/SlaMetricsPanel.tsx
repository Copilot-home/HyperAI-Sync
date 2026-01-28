import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Gauge, CheckCircle2, XCircle, AlertTriangle } from "lucide-react";
import { useSlaMetrics } from "@/hooks/useSlaMetrics";
import { Skeleton } from "@/components/ui/skeleton";
import { formatDistanceToNow } from "date-fns";

export function SlaMetricsPanel() {
  const { data: metrics, isLoading, error } = useSlaMetrics();

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Gauge className="h-5 w-5" />
            SLA/SLO Metrics
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {[1, 2].map((i) => (
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
            <Gauge className="h-5 w-5" />
            SLA/SLO Metrics
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-destructive text-sm">Failed to load SLA metrics</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Gauge className="h-5 w-5" />
          SLA/SLO Metrics
        </CardTitle>
        <CardDescription>Service level metrics for long-form video (read-only)</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {metrics && metrics.length > 0 ? (
          metrics.map((metric) => {
            const current = Number(metric.current_value);
            const target = Number(metric.target_value);
            const percentage = target > 0 ? Math.min((current / target) * 100, 100) : 0;
            const isCompliant = metric.is_compliant ?? (current >= target);
            
            return (
              <div key={metric.id} className="space-y-2 rounded-lg border p-3">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-sm">{metric.metric_name}</span>
                  <Badge variant={isCompliant ? "default" : "destructive"}>
                    {isCompliant ? (
                      <CheckCircle2 className="h-3 w-3 mr-1" />
                    ) : (
                      <XCircle className="h-3 w-3 mr-1" />
                    )}
                    {isCompliant ? "Compliant" : "Breach"}
                  </Badge>
                </div>
                
                <div className="space-y-1">
                  <div className="flex justify-between text-xs text-muted-foreground">
                    <span>Current: {current.toLocaleString()} {metric.unit}</span>
                    <span>Target: {target.toLocaleString()} {metric.unit}</span>
                  </div>
                  <Progress 
                    value={percentage} 
                    className={`h-2 ${!isCompliant ? "[&>div]:bg-destructive" : ""}`}
                  />
                </div>
                
                {metric.last_measured_at && (
                  <p className="text-xs text-muted-foreground">
                    Last measured {formatDistanceToNow(new Date(metric.last_measured_at), { addSuffix: true })}
                  </p>
                )}
              </div>
            );
          })
        ) : (
          <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
            <AlertTriangle className="h-8 w-8 mb-2" />
            <p className="text-sm">No SLA metrics configured</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
