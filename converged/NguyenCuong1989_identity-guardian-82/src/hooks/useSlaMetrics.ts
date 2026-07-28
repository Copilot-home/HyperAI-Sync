import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import type { Tables } from "@/integrations/supabase/types";

export type SlaMetric = Tables<"sla_metrics">;

export function useSlaMetrics() {
  return useQuery({
    queryKey: ["sla_metrics"],
    queryFn: async () => {
      const { data, error } = await supabase
        .from("sla_metrics")
        .select("*")
        .order("metric_name", { ascending: true });

      if (error) throw error;
      return data as SlaMetric[];
    },
  });
}
