import { useMutation, useQueryClient } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { TaskExecutionRequest, TaskExecutionResponse, DisableReason } from "@/types/ecvm";

interface TaskExecuteResult {
  task_id: string | null;
  status: "completed" | "halted" | "rejected";
  verdict: "PASS" | "REJECT" | "HALT";
  reason?: DisableReason;
  created_at?: string;
}

// POST /v1/task/execute - Kernel Gate
async function executeTask(request: TaskExecutionRequest): Promise<TaskExecuteResult> {
  const { data, error } = await supabase.functions.invoke("task-execute", {
    method: "POST",
    body: request,
  });

  if (error) {
    console.error("[useTaskExecute] Edge function error:", error);
    throw new Error(error.message || "Task execution failed");
  }

  // API returns structured response with verdict
  return {
    task_id: data.task_id,
    status: data.status,
    verdict: data.verdict,
    reason: data.reason,
    created_at: data.created_at,
  };
}

export function useTaskExecute() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: executeTask,
    onSuccess: () => {
      // Invalidate task history to show new entry
      queryClient.invalidateQueries({ queryKey: ["task-history"] });
      // Invalidate entity state in case of state changes
      queryClient.invalidateQueries({ queryKey: ["entity-state"] });
    },
    // ECVM: No retry - fail-closed
    retry: false,
  });
}
