import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import type { Tables } from "@/integrations/supabase/types";

export type EntityState = Tables<"entity_state">;

export function useEntityState() {
  return useQuery({
    queryKey: ["entity_state"],
    queryFn: async () => {
      const { data, error } = await supabase
        .from("entity_state")
        .select("*")
        .order("updated_at", { ascending: false });

      if (error) throw error;
      return data as EntityState[];
    },
  });
}
