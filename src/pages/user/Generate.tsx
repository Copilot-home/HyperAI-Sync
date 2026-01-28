import { useState, useMemo } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { DataPanel } from "@/components/ecvm/DataPanel";
import { ReasonPanel } from "@/components/ecvm/ReasonPanel";
import { StatusBadge } from "@/components/ecvm/StatusBadge";
import { useEntityState } from "@/hooks/useEntityState";
import { useAvailableLogic } from "@/hooks/useAvailableLogic";
import { TaskType, DisableReason } from "@/types/ecvm";
import { Sparkles, Image, Video, Shield, CheckCircle, XCircle, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";

const taskTypes: { type: TaskType; label: string; icon: typeof Image }[] = [
  { type: "image", label: "Image", icon: Image },
  { type: "image_static", label: "Image Static", icon: Image },
  { type: "video", label: "Video", icon: Video },
];

// Mock task execution - one API call per action
async function executeTask(request: { task_type: TaskType; logic_ids: string[]; entity_id: string }) {
  await new Promise(resolve => setTimeout(resolve, 1500));
  return {
    task_id: `task_${Math.random().toString(36).substring(7)}`,
    status: "queued" as const,
    created_at: new Date().toISOString(),
  };
}

export default function Generate() {
  const { data: entityState, isLoading: entityLoading } = useEntityState();
  const { data: logicRules, isLoading: logicLoading } = useAvailableLogic();

  const [selectedTaskType, setSelectedTaskType] = useState<TaskType>("image");
  const [selectedLogic, setSelectedLogic] = useState<string[]>([]);

  const mutation = useMutation({
    mutationFn: executeTask,
    onSuccess: (data) => {
      toast.success(`Task queued: ${data.task_id}`);
      setSelectedLogic([]);
    },
    onError: () => {
      toast.error("Task execution failed");
    },
  });

  // Compute disable reasons based on current state
  const disableReasons = useMemo<DisableReason[]>(() => {
    const reasons: DisableReason[] = [];

    if (!entityState) {
      reasons.push({
        code: "NO_ENTITY",
        message: "Entity state not loaded",
        technical_detail: "GET /v1/entity/state returned null or error",
      });
    }

    if (entityState?.status !== "active") {
      reasons.push({
        code: "ENTITY_INACTIVE",
        message: `Entity status is "${entityState?.status}"`,
        technical_detail: "Task execution requires entity.status === 'active'",
      });
    }

    if (!entityState?.reference_uploaded) {
      reasons.push({
        code: "NO_REFERENCE",
        message: "No reference material uploaded",
        technical_detail: "entity.reference_uploaded === false",
      });
    }

    const requiredLogic = logicRules?.filter(l => l.required && l.available) ?? [];
    const missingRequired = requiredLogic.filter(l => !selectedLogic.includes(l.logic_id));
    if (missingRequired.length > 0) {
      reasons.push({
        code: "MISSING_REQUIRED_LOGIC",
        message: `${missingRequired.length} required logic rule(s) not selected`,
        technical_detail: `Missing: ${missingRequired.map(l => l.logic_id).join(", ")}`,
      });
    }

    if (selectedLogic.length === 0) {
      reasons.push({
        code: "NO_LOGIC_SELECTED",
        message: "No logic rules selected",
        technical_detail: "At least one available logic rule must be selected",
      });
    }

    return reasons;
  }, [entityState, logicRules, selectedLogic]);

  const isDisabled = disableReasons.length > 0 || mutation.isPending;

  const handleGenerate = () => {
    if (isDisabled || !entityState) return;
    
    mutation.mutate({
      task_type: selectedTaskType,
      logic_ids: selectedLogic,
      entity_id: entityState.entity_id,
    });
  };

  const toggleLogic = (logicId: string) => {
    setSelectedLogic(prev =>
      prev.includes(logicId)
        ? prev.filter(id => id !== logicId)
        : [...prev, logicId]
    );
  };

  return (
    <AppLayout>
      <PageHeader
        title="Generate Task"
        subtitle="POST /v1/task/execute"
        icon={<Sparkles className="h-5 w-5 text-muted-foreground" />}
      />

      <div className="p-6 space-y-6">
        {/* Identity Gate Panel */}
        <DataPanel title="Identity Gate" icon={<Shield className="h-3.5 w-3.5" />}>
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <div className="text-sm">
                Entity: <span className="font-mono">{entityState?.entity_id ?? "—"}</span>
              </div>
              <div className="text-xs text-muted-foreground">
                Status verification required before task execution
              </div>
            </div>
            {entityLoading ? (
              <div className="text-sm text-muted-foreground font-mono">Loading...</div>
            ) : entityState ? (
              <StatusBadge status={entityState.status} />
            ) : (
              <StatusBadge status="unknown" />
            )}
          </div>
        </DataPanel>

        {/* Task Type Selector */}
        <DataPanel title="Task Type">
          <div className="flex gap-2">
            {taskTypes.map(({ type, label, icon: Icon }) => (
              <button
                key={type}
                onClick={() => setSelectedTaskType(type)}
                className={cn(
                  "flex items-center gap-2 px-4 py-2 rounded-md border text-sm font-mono transition-colors",
                  selectedTaskType === type
                    ? "bg-primary text-primary-foreground border-primary"
                    : "bg-card border-border text-muted-foreground hover:text-foreground hover:border-foreground/30"
                )}
              >
                <Icon className="h-4 w-4" />
                {label}
              </button>
            ))}
          </div>
        </DataPanel>

        {/* Logic Availability List */}
        <DataPanel title="Logic Availability" icon={<CheckCircle className="h-3.5 w-3.5" />}>
          {logicLoading ? (
            <div className="text-sm text-muted-foreground font-mono">Loading logic rules...</div>
          ) : (
            <div className="space-y-2">
              {logicRules?.map((rule) => (
                <div
                  key={rule.logic_id}
                  className={cn(
                    "flex items-center justify-between p-3 rounded-md border transition-colors",
                    !rule.available && "opacity-50 cursor-not-allowed bg-disabled-bg",
                    rule.available && selectedLogic.includes(rule.logic_id) && "border-primary bg-primary/5",
                    rule.available && !selectedLogic.includes(rule.logic_id) && "border-border hover:border-foreground/30 cursor-pointer"
                  )}
                  onClick={() => rule.available && toggleLogic(rule.logic_id)}
                >
                  <div className="flex items-center gap-3">
                    <div className={cn(
                      "h-5 w-5 rounded border flex items-center justify-center",
                      selectedLogic.includes(rule.logic_id) 
                        ? "bg-primary border-primary" 
                        : "border-border"
                    )}>
                      {selectedLogic.includes(rule.logic_id) && (
                        <CheckCircle className="h-3 w-3 text-primary-foreground" />
                      )}
                    </div>
                    <div>
                      <div className="text-sm font-medium flex items-center gap-2">
                        {rule.name}
                        {rule.required && (
                          <span className="text-[10px] font-mono uppercase px-1.5 py-0.5 bg-status-halt-bg text-status-halt-foreground rounded">
                            Required
                          </span>
                        )}
                      </div>
                      <div className="text-xs text-muted-foreground">{rule.description}</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-muted-foreground">{rule.logic_id}</span>
                    {rule.available ? (
                      <CheckCircle className="h-4 w-4 text-status-pass" />
                    ) : (
                      <XCircle className="h-4 w-4 text-status-reject" />
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </DataPanel>

        {/* Disable Reasons */}
        {disableReasons.length > 0 && (
          <ReasonPanel reasons={disableReasons} />
        )}

        {/* Generate Button */}
        <div className="flex justify-end">
          <Button
            onClick={handleGenerate}
            disabled={isDisabled}
            className={cn(
              "font-mono text-sm px-6",
              isDisabled && "opacity-50 cursor-not-allowed"
            )}
          >
            {mutation.isPending ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Executing...
              </>
            ) : (
              <>
                <Sparkles className="h-4 w-4 mr-2" />
                Generate
              </>
            )}
          </Button>
        </div>
      </div>
    </AppLayout>
  );
}
