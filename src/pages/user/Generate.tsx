import { useState, useMemo, useCallback } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { DataPanel } from "@/components/ecvm/DataPanel";
import { ReasonPanel } from "@/components/ecvm/ReasonPanel";
import { IdentityGate } from "@/components/ecvm/IdentityGate";
import { HaltTerminalScreen } from "@/components/ecvm/HaltTerminalScreen";
import { useEntityState } from "@/hooks/useEntityState";
import { useAvailableLogic } from "@/hooks/useAvailableLogic";
import { useTaskExecute } from "@/hooks/useTaskExecute";
import { useUnmetLogicSignal } from "@/hooks/useUnmetLogicSignal";
import { TaskType, DisableReason } from "@/types/ecvm";
import { Sparkles, Image, Video, CheckCircle, XCircle, Loader2, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useNavigate } from "react-router-dom";

const taskTypes: { type: TaskType; label: string; icon: typeof Image }[] = [
  { type: "image_static", label: "Image Static", icon: Image },
  { type: "image", label: "Image", icon: Image },
  { type: "video", label: "Video", icon: Video },
];

// ECVM: Identity state hierarchy for comparison
const IDENTITY_STATE_ORDER: Record<string, number> = {
  "NO_IDENTITY": 0,
  "INSUFFICIENT": 1,
  "ESTABLISHED": 2,
  "DRIFT": -1, // DRIFT blocks all
};

export default function Generate() {
  const navigate = useNavigate();
  const { data: entityState, isLoading: entityLoading, error: entityError } = useEntityState();
  const { data: logicRules, isLoading: logicLoading, error: logicError } = useAvailableLogic();

  const [selectedTaskType, setSelectedTaskType] = useState<TaskType>("image");
  const [selectedLogic, setSelectedLogic] = useState<string[]>([]);

  const taskMutation = useTaskExecute();
  const unmetLogicMutation = useUnmetLogicSignal();

  // Extract identity_state from metadata
  const identityState = (entityState?.metadata?.identity_state as string) || "NO_IDENTITY";
  const isLocked = entityState?.metadata?.locked as boolean | undefined;

  // Filter logic by selected task type
  const filteredLogic = useMemo(() => {
    return logicRules?.filter(rule => rule.category === selectedTaskType) ?? [];
  }, [logicRules, selectedTaskType]);

  // Auto-select available logic for current task type
  useMemo(() => {
    if (filteredLogic.length > 0) {
      const availableLogicIds = filteredLogic
        .filter(l => l.available)
        .map(l => l.logic_id);
      if (availableLogicIds.length > 0 && selectedLogic.length === 0) {
        setSelectedLogic(availableLogicIds);
      }
    }
  }, [filteredLogic]);

  // ECVM: Compute SINGLE disable reason based on STRICT priority order (NO MULTIPLE REASONS)
  // Priority: 1. API_ERROR → 2. INSUFFICIENT_IDENTITY → 3. DRIFT_DETECTED → 4. LOGIC_DISABLED → 5. NO_LOGIC_SELECTED
  const disableReason = useMemo<DisableReason | null>(() => {
    // Priority 1: API Errors
    if (entityError) {
      return {
        code: "API_ERROR",
        message: "Failed to fetch entity state",
        technical_detail: "GET /v1/entity/state returned error",
      };
    }

    if (logicError) {
      return {
        code: "LOGIC_API_ERROR",
        message: "Failed to fetch available logic",
        technical_detail: "GET /v1/logic/available returned error",
      };
    }

    // Priority 2: INSUFFICIENT_IDENTITY (NO_IDENTITY or INSUFFICIENT - NOT ESTABLISHED and NOT DRIFT)
    if (identityState === "NO_IDENTITY" || identityState === "INSUFFICIENT") {
      return {
        code: "INSUFFICIENT_IDENTITY",
        message: "Identity state is not sufficient to guarantee stability.",
        technical_detail: `identity_state === '${identityState}'. Required: 'ESTABLISHED'`,
      };
    }

    // Priority 3: DRIFT_DETECTED (explicit DRIFT state)
    if (identityState === "DRIFT") {
      return {
        code: "DRIFT_DETECTED",
        message: "Identity drift detected. Additional reference data required.",
        technical_detail: `identity_state === 'DRIFT'. Task execution blocked.`,
      };
    }

    // Priority 4: LOGIC_DISABLED (no enabled logic for selected task type)
    const enabledLogicForTask = filteredLogic.filter(l => l.available);
    if (enabledLogicForTask.length === 0 && !logicLoading) {
      return {
        code: "LOGIC_DISABLED",
        message: "Requested capability is not available under current system logic.",
        technical_detail: `No enabled logic modules for task_type '${selectedTaskType}'`,
      };
    }

    // Priority 5: Check if selected logic meets requirements
    const selectedLogicRules = filteredLogic.filter(l => selectedLogic.includes(l.logic_id));
    for (const rule of selectedLogicRules) {
      if (!rule.available) {
        return {
          code: "LOGIC_DISABLED",
          message: "Requested capability is not available under current system logic.",
          technical_detail: `Logic '${rule.name}' is not enabled`,
        };
      }
    }

    // Priority 6: No logic selected
    if (selectedLogic.length === 0 && !logicLoading) {
      return {
        code: "NO_LOGIC_SELECTED",
        message: "No logic rules selected for task execution.",
        technical_detail: "At least one available logic rule must be selected",
      };
    }

    return null;
  }, [entityError, logicError, identityState, filteredLogic, logicLoading, selectedLogic, selectedTaskType]);

  const isDisabled = disableReason !== null || taskMutation.isPending || entityLoading || logicLoading;

  // ECVM: Send unmet logic signal when user attempts with unavailable logic
  const sendUnmetSignal = useCallback(() => {
    if (!entityState?.entity_id) return;

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
      });
    }
  }, [entityState, selectedLogic, logicRules, selectedTaskType, identityState, unmetLogicMutation]);

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
        // ECVM: Navigate to history unconditionally (except HALT which is handled by terminal screen)
        // SPEC E2: Do not assume PASS, do not poll verdict
        // SPEC E3: Redirect to history, no retry
        if (result.verdict !== "HALT") {
          navigate("/app/user/history");
        }
        // HALT → terminal screen rendered at component level (line 192-200)
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
        {/* Identity Gate Panel - ECVM: Read-only state display with coverage */}
        <IdentityGate 
          identityState={identityState}
          entityId={entityState?.entity_id}
          isLocked={isLocked}
        />

        {/* Coverage Display */}
        {entityState && (
          <DataPanel title="Coverage Metrics">
            <div className="flex items-center justify-between">
              <div className="text-sm font-mono">
                coverage_percent: <span className="text-foreground">{entityState.coverage_percent.toFixed(1)}%</span>
              </div>
              <div className="text-sm font-mono">
                variance: <span className="text-foreground">{(entityState.variance * 100).toFixed(2)}%</span>
              </div>
            </div>
          </DataPanel>
        )}

        {/* Task Type Selector */}
        <DataPanel title="Task Type">
          <div className="flex gap-2">
            {taskTypes.map(({ type, label, icon: Icon }) => (
              <button
                key={type}
                onClick={() => {
                  setSelectedTaskType(type);
                  setSelectedLogic([]); // Reset selection on type change
                }}
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
              <span className="font-mono text-sm">Loading...</span>
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
                      <div className="text-[10px] font-mono text-muted-foreground mt-0.5">
                        required_state: {rule.required ? "ESTABLISHED" : "INSUFFICIENT"} · category: {rule.category}
                      </div>
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

        {/* ECVM: Single Reason Panel - Always mounted, shows only when disabled */}
        {disableReason && (
          <ReasonPanel reasons={[disableReason]} />
        )}

        {/* Generate Button - ECVM: Single action, no spinner text, strict disable */}
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
              <Loader2 className="h-4 w-4 animate-spin" />
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
