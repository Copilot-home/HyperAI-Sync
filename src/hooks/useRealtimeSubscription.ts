import { useEffect } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import type { RealtimePostgresChangesPayload } from "@supabase/supabase-js";

type TableName = "entity_state" | "logic_modules" | "tasks" | "drift_events" | "sla_metrics";

export function useRealtimeSubscription(tables: TableName[]) {
  const queryClient = useQueryClient();

  useEffect(() => {
    const channel = supabase.channel("dashboard-realtime");

    tables.forEach((table) => {
      channel.on(
        "postgres_changes",
        {
          event: "*",
          schema: "public",
          table: table,
        },
        (payload: RealtimePostgresChangesPayload<Record<string, unknown>>) => {
          // Invalidate the query to refetch data
          queryClient.invalidateQueries({ queryKey: [table] });
        }
      );
    });

    channel.subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, [queryClient, tables]);
}
