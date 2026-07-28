// ECVM API: GET /v1/logic/available
// Returns available logic modules for authenticated user based on identity state
// Spec: ECVM-CS-1.0 (User Node READ, filtered by required_identity_state)

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_ANON_KEY") ?? "",
      {
        global: {
          headers: { Authorization: req.headers.get("Authorization") ?? "" },
        },
      }
    );

    // Verify authenticated user
    const {
      data: { user },
      error: authError,
    } = await supabase.auth.getUser();

    if (authError || !user) {
      console.error("[logic-available] Auth error:", authError?.message);
      return new Response(
        JSON.stringify({ error: "UNAUTHORIZED", message: "Authentication required" }),
        { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    console.log("[logic-available] User authenticated:", user.id);

    // Get user's current identity state
    const { data: identity } = await supabase
      .from("entity_identity")
      .select("entity_id")
      .eq("owner_user_id", user.id)
      .maybeSingle();

    let currentState = "NO_IDENTITY";
    if (identity) {
      const { data: state } = await supabase
        .from("identity_state")
        .select("state")
        .eq("entity_id", identity.entity_id)
        .maybeSingle();
      currentState = state?.state ?? "NO_IDENTITY";
    }

    console.log("[logic-available] Current identity state:", currentState);

    // Get all enabled logic modules
    const { data: modules, error: modulesError } = await supabase
      .from("logic_module")
      .select("logic_id, name, description, task_type, required_identity_state, drift_risk_score, enabled")
      .eq("enabled", true);

    if (modulesError) {
      console.error("[logic-available] Modules fetch error:", modulesError.message);
      return new Response(
        JSON.stringify({ error: "DB_ERROR", message: modulesError.message }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // State hierarchy for availability check
    const stateHierarchy: Record<string, number> = {
      NO_IDENTITY: 0,
      INSUFFICIENT: 1,
      ESTABLISHED: 2,
      DRIFT: 1, // DRIFT = degraded to INSUFFICIENT level
    };

    const currentLevel = stateHierarchy[currentState] ?? 0;

    // Map modules to API response with availability
    const logicRules = (modules ?? []).map((mod) => {
      const requiredLevel = stateHierarchy[mod.required_identity_state] ?? 2;
      const available = currentLevel >= requiredLevel;

      return {
        logic_id: mod.logic_id,
        name: mod.name,
        description: mod.description,
        available,
        required: mod.required_identity_state === "ESTABLISHED",
        category: mod.task_type,
      };
    });

    console.log("[logic-available] Returning", logicRules.length, "modules");
    return new Response(JSON.stringify(logicRules), {
      status: 200,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error("[logic-available] Unexpected error:", error);
    return new Response(
      JSON.stringify({ error: "INTERNAL_ERROR", message: String(error) }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
