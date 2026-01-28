/**
 * ECVM Entity Initialization Hook
 * Calls initialize_entity RPC to create entity_identity + identity_state
 * on first login if not exists
 */

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";

interface InitEntityResult {
  entity_id: string | null;
  already_existed: boolean;
}

async function initializeEntity(): Promise<InitEntityResult> {
  // First check if entity already exists
  const { data: existingEntity } = await supabase
    .from("entity_identity")
    .select("entity_id")
    .maybeSingle();

  if (existingEntity?.entity_id) {
    return {
      entity_id: existingEntity.entity_id,
      already_existed: true,
    };
  }

  // Call RPC to initialize entity
  const { data, error } = await supabase.rpc("initialize_entity");

  if (error) {
    console.error("[useEntityInit] RPC error:", error);
    throw new Error(error.message || "Failed to initialize entity");
  }

  return {
    entity_id: data as string,
    already_existed: false,
  };
}

export function useEntityInit() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: initializeEntity,
    onSuccess: () => {
      // Invalidate entity-state query to fetch fresh data
      queryClient.invalidateQueries({ queryKey: ["entity-state"] });
    },
    retry: false, // ECVM: fail-closed
  });
}
