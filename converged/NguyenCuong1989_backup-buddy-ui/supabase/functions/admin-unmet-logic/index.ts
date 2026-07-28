// ECVM API: GET/DELETE /v1/admin/unmet-logic
// Manage Unmet Logic Signals (Admin Node only)
// Spec: ECVM-CS-1.0 (User → Admin signal, Admin deletes after synthesis)

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

    console.log("[admin-unmet-logic] Admin:", user.id, "Method:", req.method);

    if (req.method === "GET") {
      // List all unmet logic signals
      const { data: signals, error } = await serviceClient
        .from("unmet_logic_signal")
        .select("*")
        .order("created_at", { ascending: false })
        .limit(100);

      if (error) {
        return new Response(
          JSON.stringify({ error: "DB_ERROR", message: error.message }),
          { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      // Map to API response
      const response = (signals ?? []).map((s) => ({
        signal_id: s.signal_id,
        entity_id: s.entity_id,
        requested_task: s.requested_task,
        observed_state: s.observed_state,
        reason: s.reason ?? `Requested ${s.requested_task} but state is ${s.observed_state}`,
        created_at: s.created_at,
        severity: s.severity,
      }));

      return new Response(JSON.stringify(response), {
        status: 200,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    if (req.method === "DELETE") {
      // Delete after synthesis
      const body = await req.json();
      const { signal_id } = body;

      if (!signal_id) {
        return new Response(
          JSON.stringify({ error: "INVALID_REQUEST", message: "signal_id required" }),
          { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      const { error } = await serviceClient
        .from("unmet_logic_signal")
        .delete()
        .eq("signal_id", signal_id);

      if (error) {
        return new Response(
          JSON.stringify({ error: "DB_ERROR", message: error.message }),
          { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      // Log to audit
      await serviceClient.from("audit_log").insert({
        action: "unmet_logic.resolve",
        actor_type: "user",
        actor_id: user.id,
        resource_type: "unmet_logic",
        resource_id: signal_id,
        details: {},
      });

      console.log("[admin-unmet-logic] Resolved:", signal_id);
      return new Response(JSON.stringify({ success: true }), {
        status: 200,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    return new Response(
      JSON.stringify({ error: "METHOD_NOT_ALLOWED" }),
      { status: 405, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (error) {
    console.error("[admin-unmet-logic] Error:", error);
    return new Response(
      JSON.stringify({ error: "INTERNAL_ERROR", message: String(error) }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
