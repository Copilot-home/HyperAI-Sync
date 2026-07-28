import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Activity, Clock, CheckCircle2, XCircle, AlertOctagon, AlertTriangle } from "lucide-react";
import { useTasks } from "@/hooks/useTasks";
import { Skeleton } from "@/components/ui/skeleton";
import { formatDistanceToNow } from "date-fns";

const statusConfig = {
  queued: { icon: Clock, color: "secondary" as const, label: "Queued" },
  running: { icon: Activity, color: "default" as const, label: "Running" },
  halting: { icon: AlertOctagon, color: "destructive" as const, label: "Halting" },
  completed: { icon: CheckCircle2, color: "outline" as const, label: "Completed" },
};

const verdictConfig = {
  PASS: { icon: CheckCircle2, color: "default" as const },
  REJECT: { icon: XCircle, color: "destructive" as const },
  HALT: { icon: AlertOctagon, color: "secondary" as const },
};

export function TaskMonitorPanel() {
  const { data: tasks, isLoading, error } = useTasks();

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-5 w-5" />
            Task Execution
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-24 w-full" />
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
            <Activity className="h-5 w-5" />
            Task Execution
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-destructive text-sm">Failed to load tasks</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Activity className="h-5 w-5" />
          Task Execution
        </CardTitle>
        <CardDescription>Task queue and execution state (read-only)</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {tasks && tasks.length > 0 ? (
          tasks.map((task) => {
            const status = statusConfig[task.status];
            const StatusIcon = status.icon;
            const progress = Number(task.progress) || 0;
            const verdict = task.verdict ? verdictConfig[task.verdict] : null;
            const VerdictIcon = verdict?.icon;
            
            return (
              <div key={task.id} className="rounded-lg border p-3 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <StatusIcon className="h-4 w-4" />
                    <span className="font-medium text-sm">{task.task_name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {verdict && VerdictIcon && (
                      <Badge variant={verdict.color}>
                        <VerdictIcon className="h-3 w-3 mr-1" />
                        {task.verdict}
                      </Badge>
                    )}
                    <Badge variant={status.color}>{status.label}</Badge>
                  </div>
                </div>
                
                {task.status === "running" && (
                  <div className="space-y-1">
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>Progress</span>
                      <span>{progress.toFixed(1)}%</span>
                    </div>
                    <Progress value={progress} className="h-1.5" />
                  </div>
                )}
                
                <div className="flex items-center gap-4 text-xs text-muted-foreground">
                  {task.frame_count !== null && (
                    <span>Frames: {task.frame_count}</span>
                  )}
                  {task.halt_point !== null && (
                    <span className="text-destructive">Halt @ {task.halt_point}</span>
                  )}
                  {task.halt_reason && (
                    <span className="text-destructive truncate max-w-[200px]" title={task.halt_reason}>
                      {task.halt_reason}
                    </span>
                  )}
                  <span className="ml-auto">
                    {formatDistanceToNow(new Date(task.created_at), { addSuffix: true })}
                  </span>
                </div>
              </div>
            );
          })
        ) : (
          <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
            <AlertTriangle className="h-8 w-8 mb-2" />
            <p className="text-sm">No tasks in queue</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
