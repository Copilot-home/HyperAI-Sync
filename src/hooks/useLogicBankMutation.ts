import { useMutation, useQueryClient } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";

interface ToggleLogicParams {
  logic_id: string;
  enabled: boolean;
}

interface UpdateLogicParams {
  logic_id: string;
  enabled?: boolean;
  name?: string;
  description?: string;
}

// Toggle logic module enabled state
async function toggleLogicModule(params: ToggleLogicParams): Promise<void> {
  const { data, error } = await supabase.functions.invoke("admin-logic-bank", {
    method: "PUT",
    body: params,
  });

  if (error) {
    console.error("[useLogicBankMutation] Toggle error:", error);
    throw new Error(error.message || "Failed to toggle logic module");
  }

  return data;
}

// Update logic module
async function updateLogicModule(params: UpdateLogicParams): Promise<void> {
  const { data, error } = await supabase.functions.invoke("admin-logic-bank", {
    method: "PUT",
    body: params,
  });

  if (error) {
    console.error("[useLogicBankMutation] Update error:", error);
    throw new Error(error.message || "Failed to update logic module");
  }

  return data;
}

export function useToggleLogic() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: toggleLogicModule,
    onSuccess: () => {
      // Invalidate logic bank query to refetch updated data
      queryClient.invalidateQueries({ queryKey: ["logic-bank"] });
    },
  });
}

export function useUpdateLogic() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateLogicModule,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["logic-bank"] });
    },
  });
}
