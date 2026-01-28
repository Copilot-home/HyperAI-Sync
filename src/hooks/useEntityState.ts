import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { EntityState } from "@/types/ecvm";

// Mock endpoint - in production this would be GET /v1/entity/state
async function fetchEntityState(): Promise<EntityState> {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  // Mock data - replace with actual API call when backend is ready
  return {
    entity_id: "ent_7f3a9c2d",
    status: "active",
    coverage_percent: 87.5,
    variance: 0.023,
    reference_uploaded: true,
    last_sync: new Date().toISOString(),
    metadata: {
      version: "2.1.0",
      region: "us-east-1",
    },
  };
}

export function useEntityState() {
  return useQuery({
    queryKey: ["entity-state"],
    queryFn: fetchEntityState,
    staleTime: 30000, // 30 seconds
    refetchOnWindowFocus: false,
  });
}
