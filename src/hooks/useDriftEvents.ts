import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import type { Tables } from "@/integrations/supabase/types";

export type DriftEvent = Tables<"drift_events">;

export function useDriftEvents() {
  return useQuery({
    queryKey: ["drift_events"],
    queryFn: async () => {
      const { data, error } = await supabase
        .from("drift_events")
        .select("*")
        .order("created_at", { ascending: false });

      if (error) throw error;
      return data as DriftEvent[];
    },
  });
}
