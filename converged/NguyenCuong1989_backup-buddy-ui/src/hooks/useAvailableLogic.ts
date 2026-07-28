import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { LogicRule } from "@/types/ecvm";

// GET /v1/logic/available - Real Edge Function call
async function fetchAvailableLogic(): Promise<LogicRule[]> {
  const { data, error } = await supabase.functions.invoke("logic-available", {
    method: "GET",
  });

  if (error) {
    console.error("[useAvailableLogic] Edge function error:", error);
    throw new Error(error.message || "Failed to fetch available logic");
  }

  // Map API response to LogicRule type
  return (data ?? []).map((m: Record<string, unknown>) => ({
    logic_id: m.logic_id as string,
    name: m.name as string,
    description: m.description as string,
    available: m.available as boolean,
    required: m.required as boolean,
    category: m.category as string, // API already returns 'category', not 'task_type'
  }));
}

export function useAvailableLogic() {
  return useQuery({
    queryKey: ["available-logic"],
    queryFn: fetchAvailableLogic,
    staleTime: 60000,
    refetchOnWindowFocus: false,
    retry: false, // ECVM: fail-closed, no retry
  });
}
