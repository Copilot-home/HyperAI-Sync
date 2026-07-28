// ECVM API: GET/PUT /v1/admin/drift
// Manage Drift Events (Admin Node only)
// Spec: ECVM-CS-1.0 (Admin observes systemic drift, acknowledges)

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
      return new Response(
        JSON.stringify({ error: "UNAUTHORIZED" }),
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
      return new Response(
        JSON.stringify({ error: "FORBIDDEN" }),
        { status: 403, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    console.log("[admin-drift] Admin:", user.id, "Method:", req.method);

    if (req.method === "GET") {
      // List all drift events
      const { data: drifts, error } = await serviceClient
        .from("drift_event")
        .select("*")
        .order("detected_at", { ascending: false })
        .limit(100);

      if (error) {
        return new Response(
          JSON.stringify({ error: "DB_ERROR", message: error.message }),
          { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      // Map to API response
      const response = (drifts ?? []).map((d) => ({
        drift_id: d.drift_id,
        entity_id: d.entity_id,
        logic_id: d.logic_id,
        drift_type: d.drift_type, // Keep original uppercase (PER_NODE, SYSTEMIC)
        baseline: d.baseline,
        current_value: d.current_value,
        severity: d.severity,
        detected_at: d.detected_at,
        acknowledged: d.acknowledged,
      }));

      return new Response(JSON.stringify(response), {
        status: 200,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    if (req.method === "PUT") {
      // Acknowledge drift
      const body = await req.json();
      const { drift_id, acknowledged } = body;

      if (!drift_id) {
        return new Response(
          JSON.stringify({ error: "INVALID_REQUEST", message: "drift_id required" }),
          { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      const { data, error } = await serviceClient
        .from("drift_event")
        .update({ acknowledged: acknowledged ?? true })
        .eq("drift_id", drift_id)
        .select()
        .single();

      if (error) {
        return new Response(
          JSON.stringify({ error: "DB_ERROR", message: error.message }),
          { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      // Log to audit
      await serviceClient.from("audit_log").insert({
        action: "drift.acknowledge",
        actor_type: "user",
        actor_id: user.id,
        resource_type: "drift",
        resource_id: drift_id,
        details: { acknowledged },
      });

      console.log("[admin-drift] Acknowledged:", drift_id);
      return new Response(JSON.stringify(data), {
        status: 200,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    return new Response(
      JSON.stringify({ error: "METHOD_NOT_ALLOWED" }),
      { status: 405, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (error) {
    console.error("[admin-drift] Error:", error);
    return new Response(
      JSON.stringify({ error: "INTERNAL_ERROR", message: String(error) }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
