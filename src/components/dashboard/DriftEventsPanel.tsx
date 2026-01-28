import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertTriangle, Waves, CheckCircle2, Globe, User } from "lucide-react";
import { useDriftEvents } from "@/hooks/useDriftEvents";
import { Skeleton } from "@/components/ui/skeleton";
import { formatDistanceToNow } from "date-fns";

export function DriftEventsPanel() {
  const { data: events, isLoading, error } = useDriftEvents();

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Waves className="h-5 w-5" />
            Drift Events
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-16 w-full" />
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
            <Waves className="h-5 w-5" />
            Drift Events
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-destructive text-sm">Failed to load drift events</p>
        </CardContent>
      </Card>
    );
  }

  const getSeverityColor = (severity: number | null) => {
    if (!severity) return "secondary";
    if (severity >= 8) return "destructive";
    if (severity >= 5) return "default";
    return "secondary";
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Waves className="h-5 w-5" />
          Drift Events
        </CardTitle>
        <CardDescription>Identity drift signals and anomalies (read-only)</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {events && events.length > 0 ? (
          events.map((event) => (
            <div 
              key={event.id} 
              className={`rounded-lg border p-3 space-y-2 ${
                event.resolved ? "opacity-60" : ""
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  {event.scope === "systemic" ? (
                    <Globe className="h-4 w-4 text-destructive" />
                  ) : (
                    <User className="h-4 w-4" />
                  )}
                  <span className="font-medium text-sm">{event.event_type}</span>
                </div>
                <div className="flex items-center gap-2">
                  {event.resolved && (
                    <CheckCircle2 className="h-4 w-4 text-primary" />
                  )}
                  <Badge variant={event.scope === "systemic" ? "destructive" : "outline"}>
                    {event.scope}
                  </Badge>
                  <Badge variant={getSeverityColor(event.severity) as "default" | "secondary" | "destructive" | "outline"}>
                    Sev: {event.severity ?? 1}
                  </Badge>
                </div>
              </div>
              
              {event.description && (
                <p className="text-sm text-muted-foreground">{event.description}</p>
              )}
              
              <div className="flex items-center gap-4 text-xs text-muted-foreground">
                {event.node_id && (
                  <code className="bg-muted px-1.5 py-0.5 rounded">{event.node_id}</code>
                )}
                <span className="ml-auto">
                  {formatDistanceToNow(new Date(event.created_at), { addSuffix: true })}
                </span>
              </div>
            </div>
          ))
        ) : (
          <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
            <AlertTriangle className="h-8 w-8 mb-2" />
            <p className="text-sm">No drift events detected</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
