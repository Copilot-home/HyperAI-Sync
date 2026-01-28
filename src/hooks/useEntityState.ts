import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { EntityState } from "@/types/ecvm";

// GET /v1/entity/state - Real Edge Function call
async function fetchEntityState(): Promise<EntityState> {
  const { data, error } = await supabase.functions.invoke("entity-state", {
    method: "GET",
  });

  if (error) {
    console.error("[useEntityState] Edge function error:", error);
    throw new Error(error.message || "Failed to fetch entity state");
  }

  // Handle NO_IDENTITY case
  if (data.entity_id === null) {
    return {
      entity_id: "",
      status: "pending",
      coverage_percent: 0,
      variance: 1.0,
      reference_uploaded: false,
      last_sync: "",
      metadata: data.metadata ?? {},
    };
  }

  return {
    entity_id: data.entity_id,
    status: data.status as EntityState["status"],
    coverage_percent: data.coverage_percent,
    variance: data.variance,
    reference_uploaded: data.reference_uploaded,
    last_sync: data.last_sync,
    metadata: data.metadata ?? {},
  };
}

export function useEntityState() {
  return useQuery({
    queryKey: ["entity-state"],
    queryFn: fetchEntityState,
    staleTime: 30000,
    refetchOnWindowFocus: false,
    retry: false, // ECVM: fail-closed, no retry
  });
}
