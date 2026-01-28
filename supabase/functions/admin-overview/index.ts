// ECVM API: GET /v1/admin/overview
// Returns admin dashboard metrics
// Spec: ECVM-CS-1.0 (Admin Node only, service_role or has_role('admin'))

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
    const userClient = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_ANON_KEY") ?? "",
      {
        global: {
          headers: { Authorization: req.headers.get("Authorization") ?? "" },
        },
      }
    );

    const serviceClient = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? ""
    );

    // Verify authenticated user
    const {
      data: { user },
      error: authError,
    } = await userClient.auth.getUser();

    if (authError || !user) {
      console.error("[admin-overview] Auth error:", authError?.message);
      return new Response(
        JSON.stringify({ error: "UNAUTHORIZED", message: "Authentication required" }),
        { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Check admin role
    const { data: roleData } = await serviceClient
      .from("user_roles")
      .select("role")
      .eq("user_id", user.id)
      .eq("role", "admin")
      .maybeSingle();

    if (!roleData) {
      console.error("[admin-overview] Access denied: not admin");
      return new Response(
        JSON.stringify({ error: "FORBIDDEN", message: "Admin access required" }),
        { status: 403, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    console.log("[admin-overview] Admin authenticated:", user.id);

    // Fetch metrics using service role
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // Total entities
    const { count: totalEntities } = await serviceClient
      .from("entity_identity")
      .select("*", { count: "exact", head: true });

    // Active entities (ESTABLISHED state)
    const { count: activeEntities } = await serviceClient
      .from("identity_state")
      .select("*", { count: "exact", head: true })
      .eq("state", "ESTABLISHED");

    // Tasks today
    const { count: tasksToday } = await serviceClient
      .from("task_execution_log")
      .select("*", { count: "exact", head: true })
      .gte("executed_at", today.toISOString());

    // Pass rate today
    const { data: verdicts } = await serviceClient
      .from("task_execution_log")
      .select("verdict")
      .gte("executed_at", today.toISOString());

    const passCount = (verdicts ?? []).filter((v) => v.verdict === "PASS").length;
    const passRate = verdicts && verdicts.length > 0 
      ? (passCount / verdicts.length) * 100 
      : 100;

    // Unmet logic count
    const { count: unmetLogicCount } = await serviceClient
      .from("unmet_logic_signal")
      .select("*", { count: "exact", head: true });

    // Active drift count (unacknowledged)
    const { count: activeDriftCount } = await serviceClient
      .from("drift_event")
      .select("*", { count: "exact", head: true })
      .eq("acknowledged", false);

    const response = {
      total_entities: totalEntities ?? 0,
      active_entities: activeEntities ?? 0,
      total_tasks_today: tasksToday ?? 0,
      pass_rate: Math.round(passRate * 10) / 10,
      unmet_logic_count: unmetLogicCount ?? 0,
      active_drift_count: activeDriftCount ?? 0,
    };

    console.log("[admin-overview] Response:", response);
    return new Response(JSON.stringify(response), {
      status: 200,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error("[admin-overview] Unexpected error:", error);
    return new Response(
      JSON.stringify({ error: "INTERNAL_ERROR", message: String(error) }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
