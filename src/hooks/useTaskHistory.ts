import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { TaskExecutionLog } from "@/types/ecvm";

// Query task_execution_log table directly via Supabase client
// RLS ensures user only sees their own entity's logs
async function fetchTaskHistory(): Promise<TaskExecutionLog[]> {
  // First get user's entity_id
  const { data: identity, error: identityError } = await supabase
    .from("entity_identity")
    .select("entity_id")
    .maybeSingle();

  if (identityError) {
    console.error("[useTaskHistory] Identity fetch error:", identityError);
    throw new Error(identityError.message);
  }

  // No identity = no history
  if (!identity) {
    return [];
  }

  // Fetch execution logs for this entity
  const { data: logs, error: logsError } = await supabase
    .from("task_execution_log")
    .select("*")
    .eq("entity_id", identity.entity_id)
    .order("executed_at", { ascending: false })
    .limit(50);

  if (logsError) {
    console.error("[useTaskHistory] Logs fetch error:", logsError);
    throw new Error(logsError.message);
  }

  // Map to TaskExecutionLog type
  return (logs ?? []).map((log) => ({
    id: log.task_id,
    task_id: log.task_id,
    entity_id: log.entity_id,
    task_type: log.task_type as TaskExecutionLog["task_type"],
    verdict: log.verdict as TaskExecutionLog["verdict"],
    logic_applied: log.logic_applied ?? [],
    executed_at: log.executed_at,
    execution_time_ms: log.execution_time_ms,
    metadata: (log.metadata as Record<string, unknown>) ?? {},
  }));
}

export function useTaskHistory() {
  return useQuery({
    queryKey: ["task-history"],
    queryFn: fetchTaskHistory,
    staleTime: 30000,
    refetchOnWindowFocus: false,
    retry: false, // ECVM: fail-closed, no retry
  });
}
