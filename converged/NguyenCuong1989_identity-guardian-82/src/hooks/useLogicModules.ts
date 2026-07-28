import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import type { Tables } from "@/integrations/supabase/types";

export type LogicModule = Tables<"logic_modules">;

export function useLogicModules() {
  return useQuery({
    queryKey: ["logic_modules"],
    queryFn: async () => {
      const { data, error } = await supabase
        .from("logic_modules")
        .select("*")
        .order("module_name", { ascending: true });

      if (error) throw error;
      return data as LogicModule[];
    },
  });
}
