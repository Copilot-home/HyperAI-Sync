import { useEffect } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";

/**
 * ECVM Realtime Hook: Subscribe to identity_state changes
 * Enables live coverage % updates during reference upload
 * Spec: ECVM-CS-1.0 (Read-only state observation)
 */
export function useRealtimeIdentityState(entityId: string | undefined) {
  const queryClient = useQueryClient();

  useEffect(() => {
    if (!entityId) return;

    console.log("[Realtime] Subscribing to identity_state for:", entityId);

    const channel = supabase
      .channel(`identity_state:${entityId}`)
      .on(
        "postgres_changes",
        {
          event: "UPDATE",
          schema: "public",
          table: "identity_state",
          filter: `entity_id=eq.${entityId}`,
        },
        (payload) => {
          console.log("[Realtime] identity_state updated:", payload.new);
          
          // Invalidate entity-state query to refetch with new data
          queryClient.invalidateQueries({ queryKey: ["entity-state"] });
          
          // Also invalidate references query for consistency
          queryClient.invalidateQueries({ queryKey: ["entity-references"] });
        }
      )
      .subscribe((status) => {
        console.log("[Realtime] Subscription status:", status);
      });

    return () => {
      console.log("[Realtime] Unsubscribing from identity_state");
      supabase.removeChannel(channel);
    };
  }, [entityId, queryClient]);
}
