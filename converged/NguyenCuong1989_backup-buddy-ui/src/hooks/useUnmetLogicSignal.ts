import { useMutation } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { TaskType } from "@/types/ecvm";

interface UnmetLogicRequest {
  entity_id: string;
  requested_task: TaskType;
  observed_state: string;
  unavailable_logic_ids: string[];
}

interface UnmetLogicResponse {
  signal_id: string;
  severity: string;
  created_at: string;
}

/**
 * ECVM API: POST /v1/logic/unmet
 * Signal when user attempts task execution with unavailable logic
 * Spec: ECVM-CS-1.0 (User Node - Unmet Logic Signal)
 */
async function sendUnmetLogicSignal(request: UnmetLogicRequest): Promise<UnmetLogicResponse> {
  const { data, error } = await supabase.functions.invoke("logic-unmet", {
    method: "POST",
    body: request,
  });

  if (error) {
    console.error("[useUnmetLogicSignal] Error:", error);
    throw new Error(error.message || "Failed to send unmet logic signal");
  }

  return data as UnmetLogicResponse;
}

export function useUnmetLogicSignal() {
  return useMutation({
    mutationFn: sendUnmetLogicSignal,
    // ECVM: No retry - signal is informational, fail-silent
    retry: false,
  });
}
