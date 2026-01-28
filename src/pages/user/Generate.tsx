import { useState, useMemo, useEffect, useCallback } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { DataPanel } from "@/components/ecvm/DataPanel";
import { ReasonPanel } from "@/components/ecvm/ReasonPanel";
import { StatusBadge } from "@/components/ecvm/StatusBadge";
import { HaltTerminalScreen } from "@/components/ecvm/HaltTerminalScreen";
import { useEntityState } from "@/hooks/useEntityState";
import { useAvailableLogic } from "@/hooks/useAvailableLogic";
import { useTaskExecute } from "@/hooks/useTaskExecute";
import { useUnmetLogicSignal } from "@/hooks/useUnmetLogicSignal";
import { TaskType, DisableReason } from "@/types/ecvm";
import { Sparkles, Image, Video, Shield, CheckCircle, XCircle, Loader2, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

const taskTypes: { type: TaskType; label: string; icon: typeof Image }[] = [
  { type: "image", label: "Image", icon: Image },
  { type: "image_static", label: "Image Static", icon: Image },
  { type: "video", label: "Video", icon: Video },
];

export default function Generate() {
  const { data: entityState, isLoading: entityLoading, error: entityError } = useEntityState();
  const { data: logicRules, isLoading: logicLoading, error: logicError } = useAvailableLogic();

  const [selectedTaskType, setSelectedTaskType] = useState<TaskType>("image");
  const [selectedLogic, setSelectedLogic] = useState<string[]>([]);

  const taskMutation = useTaskExecute();
  const unmetLogicMutation = useUnmetLogicSignal();

  // Auto-select required logic when available
  useEffect(() => {
    if (logicRules) {
      const requiredLogicIds = logicRules
        .filter(l => l.required && l.available)
        .map(l => l.logic_id);
      setSelectedLogic(prev => {
        const newSelection = [...new Set([...prev, ...requiredLogicIds])];
        return newSelection;
      });
    }
  }, [logicRules]);

  // ECVM: Compute disable reasons based on current state (NO INTERPRETATION)
  const disableReasons = useMemo<DisableReason[]>(() => {
    const reasons: DisableReason[] = [];

    // Gate 1: Entity state must be loaded
    if (entityError) {
      reasons.push({
        code: "API_ERROR",
        message: "Failed to fetch entity state",
        technical_detail: "GET /v1/entity/state returned error",
      });
      return reasons; // Terminal
    }

    if (!entityState && !entityLoading) {
      reasons.push({
        code: "NO_ENTITY",
        message: "Entity state not available",
        technical_detail: "GET /v1/entity/state returned null",
      });
      return reasons;
    }

    // Gate 2: Identity state must be ESTABLISHED (from metadata.identity_state)
    const identityState = entityState?.metadata?.identity_state as string | undefined;
    if (identityState && identityState !== "ESTABLISHED") {
      reasons.push({
        code: "IDENTITY_NOT_ESTABLISHED",
        message: `Identity state is "${identityState}"`,
        technical_detail: `Task execution requires identity_state === 'ESTABLISHED'. Current: ${identityState}`,
      });
    }

    // Gate 3: Entity status must be active
    if (entityState?.status !== "active") {
      reasons.push({
        code: "ENTITY_INACTIVE",
        message: `Entity status is "${entityState?.status}"`,
        technical_detail: "Task execution requires entity.status === 'active'",
      });
    }

    // Gate 4: Reference must be uploaded
    if (!entityState?.reference_uploaded) {
      reasons.push({
        code: "NO_REFERENCE",
        message: "No reference material uploaded",
        technical_detail: "entity.reference_uploaded === false",
      });
    }

    // Gate 5: Logic availability error
    if (logicError) {
      reasons.push({
        code: "LOGIC_API_ERROR",
        message: "Failed to fetch available logic",
        technical_detail: "GET /v1/logic/available returned error",
      });
    }

    // Gate 6: At least one logic must be selected
    if (selectedLogic.length === 0 && !logicLoading) {
      reasons.push({
        code: "NO_LOGIC_SELECTED",
        message: "No logic rules selected",
        technical_detail: "At least one available logic rule must be selected",
      });
    }

    // Gate 7: All required logic must be selected
    const requiredLogic = logicRules?.filter(l => l.required && l.available) ?? [];
    const missingRequired = requiredLogic.filter(l => !selectedLogic.includes(l.logic_id));
    if (missingRequired.length > 0) {
      reasons.push({
        code: "MISSING_REQUIRED_LOGIC",
        message: `${missingRequired.length} required logic rule(s) not selected`,
        technical_detail: `Missing: ${missingRequired.map(l => l.name || l.logic_id).join(", ")}`,
      });
    }

    // Gate 8: Selected logic must be available
    const unavailableSelected = selectedLogic.filter(id => {
      const rule = logicRules?.find(l => l.logic_id === id);
      return rule && !rule.available;
    });
    if (unavailableSelected.length > 0) {
      reasons.push({
        code: "UNAVAILABLE_LOGIC_SELECTED",
        message: `${unavailableSelected.length} selected logic rule(s) not available`,
        technical_detail: `Unavailable: ${unavailableSelected.join(", ")}`,
      });
    }

    return reasons;
  }, [entityState, entityError, entityLoading, logicRules, logicError, logicLoading, selectedLogic]);

  const isDisabled = disableReasons.length > 0 || taskMutation.isPending || entityLoading || logicLoading;

  // ECVM: Send unmet logic signal when user attempts with unavailable logic
  const sendUnmetSignal = useCallback(() => {
    if (!entityState?.entity_id) return;

    const identityState = entityState?.metadata?.identity_state as string || "NO_IDENTITY";
    const unavailableSelected = selectedLogic.filter(id => {
      const rule = logicRules?.find(l => l.logic_id === id);
      return rule && !rule.available;
    });

    // Only send if there are unavailable logic selected or identity not established
    if (unavailableSelected.length > 0 || identityState !== "ESTABLISHED") {
      unmetLogicMutation.mutate({
        entity_id: entityState.entity_id,
        requested_task: selectedTaskType,
        observed_state: identityState,
        unavailable_logic_ids: unavailableSelected,
      }, {
        onSuccess: (signal) => {
          console.log("[Generate] Unmet logic signal sent:", signal.signal_id);
        },
      });
    }
  }, [entityState, selectedLogic, logicRules, selectedTaskType, unmetLogicMutation]);

  // ECVM: Single action = Single API call (POST /v1/task/execute)
  const handleGenerate = () => {
    // If disabled due to unmet logic conditions, send signal before returning
    if (isDisabled) {
      sendUnmetSignal();
      return;
    }
    
    if (!entityState) return;
    
    taskMutation.mutate({
      task_type: selectedTaskType,
      logic_ids: selectedLogic,
      entity_id: entityState.entity_id,
    }, {
      onSuccess: (result) => {
        if (result.verdict === "PASS") {
          toast.success(`Task completed: ${result.task_id}`);
        } else if (result.verdict === "HALT") {
          toast.warning(`Task halted: ${result.reason?.message || "System halt"}`);
        } else {
          toast.error(`Task rejected: ${result.reason?.message || "Validation failed"}`);
        }
      },
      onError: (error) => {
        toast.error(`Task execution failed: ${error.message}`);
      },
    });
  };

  const toggleLogic = (logicId: string) => {
    const rule = logicRules?.find(l => l.logic_id === logicId);
    if (!rule?.available) return;
    
    setSelectedLogic(prev =>
      prev.includes(logicId)
        ? prev.filter(id => id !== logicId)
        : [...prev, logicId]
    );
  };

  // Filter logic by selected task type
  const filteredLogic = useMemo(() => {
    return logicRules?.filter(rule => rule.category === selectedTaskType) ?? [];
  }, [logicRules, selectedTaskType]);

  // ECVM: HALT = Terminal - show full-screen halt message, no retry
  if (taskMutation.data?.verdict === "HALT" && taskMutation.data.reason) {
    return (
      <AppLayout>
        <HaltTerminalScreen 
          reason={taskMutation.data.reason}
          taskId={taskMutation.data.task_id ?? undefined}
        />
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <PageHeader
        title="Generate Task"
        subtitle="POST /v1/task/execute"
        icon={<Sparkles className="h-5 w-5 text-muted-foreground" />}
      />

      <div className="p-6 space-y-6">
        {/* Identity Gate Panel - ECVM: Read-only state display */}
        <DataPanel title="Identity Gate" icon={<Shield className="h-3.5 w-3.5" />}>
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <div className="text-sm">
                Entity: <span className="font-mono">{entityState?.entity_id || "—"}</span>
              </div>
              <div className="text-xs text-muted-foreground">
                Status verification required before task execution
              </div>
              {entityState?.metadata?.identity_state && (
                <div className="text-xs font-mono text-muted-foreground">
                  identity_state: {entityState.metadata.identity_state as string}
                </div>
              )}
            </div>
            {entityLoading ? (
              <div className="flex items-center gap-2 text-muted-foreground">
                <Loader2 className="h-4 w-4 animate-spin" />
                <span className="text-sm font-mono">Loading...</span>
              </div>
            ) : entityError ? (
              <div className="flex items-center gap-2 text-status-reject">
                <AlertCircle className="h-4 w-4" />
                <span className="text-sm font-mono">Error</span>
              </div>
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

        {/* Logic Availability List - ECVM: Filtered by task_type */}
        <DataPanel title="Logic Availability" icon={<CheckCircle className="h-3.5 w-3.5" />}>
          {logicLoading ? (
            <div className="flex items-center gap-2 text-muted-foreground">
              <Loader2 className="h-4 w-4 animate-spin" />
              <span className="font-mono text-sm">Loading logic rules...</span>
            </div>
          ) : logicError ? (
            <div className="flex items-center gap-2 text-status-reject-foreground bg-status-reject-bg p-3 rounded">
              <AlertCircle className="h-4 w-4" />
              <span className="text-sm font-mono">Failed to load logic rules</span>
            </div>
          ) : filteredLogic.length === 0 ? (
            <div className="text-sm text-muted-foreground font-mono p-3 bg-muted rounded">
              No logic rules available for task type: {selectedTaskType}
            </div>
          ) : (
            <div className="space-y-2">
              {filteredLogic.map((rule) => (
                <div
                  key={rule.logic_id}
                  className={cn(
                    "flex items-center justify-between p-3 rounded-md border transition-colors",
                    !rule.available && "opacity-50 cursor-not-allowed bg-disabled-bg",
                    rule.available && selectedLogic.includes(rule.logic_id) && "border-primary bg-primary/5",
                    rule.available && !selectedLogic.includes(rule.logic_id) && "border-border hover:border-foreground/30 cursor-pointer"
                  )}
                  onClick={() => toggleLogic(rule.logic_id)}
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
                    <span className="text-[10px] font-mono text-muted-foreground truncate max-w-[100px]">
                      {rule.logic_id.slice(0, 8)}...
                    </span>
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

        {/* Disable Reasons - ECVM: Show technical details */}
        {disableReasons.length > 0 && (
          <ReasonPanel reasons={disableReasons} />
        )}

        {/* Task Execution Result */}
        {taskMutation.data && (
          <DataPanel title="Last Execution Result">
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <div className="text-sm font-mono">
                  task_id: {taskMutation.data.task_id || "—"}
                </div>
                <div className="text-xs text-muted-foreground">
                  status: {taskMutation.data.status}
                </div>
              </div>
              <StatusBadge status={taskMutation.data.verdict} />
            </div>
            {taskMutation.data.reason && (
              <div className="mt-3 p-2 bg-muted rounded text-xs font-mono">
                [{taskMutation.data.reason.code}] {taskMutation.data.reason.message}
              </div>
            )}
          </DataPanel>
        )}

        {/* Generate Button - ECVM: Single action, strict disable */}
        <div className="flex justify-end">
          <Button
            onClick={handleGenerate}
            disabled={isDisabled}
            className={cn(
              "font-mono text-sm px-6",
              isDisabled && "opacity-50 cursor-not-allowed"
            )}
          >
            {taskMutation.isPending ? (
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
