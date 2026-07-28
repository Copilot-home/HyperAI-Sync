// ECVM API: GET/PUT /v1/admin/logic-bank
// Manage Logic Bank (Admin Node only)
// Spec: ECVM-CS-1.0 (Admin OWNS Internal Logic Bank)

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
        JSON.stringify({ error: "FORBIDDEN", message: "Admin access required" }),
        { status: 403, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    console.log("[admin-logic-bank] Admin:", user.id, "Method:", req.method);

    if (req.method === "GET") {
      // List all logic modules
      const { data: modules, error } = await serviceClient
        .from("logic_module")
        .select("*")
        .order("created_at", { ascending: false });

      if (error) {
        return new Response(
          JSON.stringify({ error: "DB_ERROR", message: error.message }),
          { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      // Map to API response format
      const response = (modules ?? []).map((m) => ({
        logic_id: m.logic_id,
        name: m.name,
        description: m.description,
        version: `${m.version}.0.0`,
        status: m.enabled ? "active" : "draft",
        task_type: m.task_type,
        required_identity_state: m.required_identity_state,
        drift_risk_score: m.drift_risk_score,
        created_at: m.created_at,
        updated_at: m.updated_at,
      }));

      return new Response(JSON.stringify(response), {
        status: 200,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    if (req.method === "PUT") {
      // Update a logic module
      const body = await req.json();
      const { logic_id, enabled, name, description } = body;

      if (!logic_id) {
        return new Response(
          JSON.stringify({ error: "INVALID_REQUEST", message: "logic_id required" }),
          { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      const updates: Record<string, unknown> = {};
      if (typeof enabled === "boolean") updates.enabled = enabled;
      if (name) updates.name = name;
      if (description) updates.description = description;

      const { data, error } = await serviceClient
        .from("logic_module")
        .update(updates)
        .eq("logic_id", logic_id)
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
        action: "logic.update",
        actor_type: "user",
        actor_id: user.id,
        resource_type: "logic",
        resource_id: logic_id,
        details: updates,
      });

      console.log("[admin-logic-bank] Updated:", logic_id);
      return new Response(JSON.stringify(data), {
        status: 200,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    if (req.method === "POST") {
      // Create new logic module
      const body = await req.json();
      const { name, description, task_type, required_identity_state, drift_risk_score } = body;

      if (!name || !task_type) {
        return new Response(
          JSON.stringify({ error: "INVALID_REQUEST", message: "name and task_type required" }),
          { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      const { data, error } = await serviceClient
        .from("logic_module")
        .insert({
          name,
          description: description ?? "",
          task_type,
          required_identity_state: required_identity_state ?? "ESTABLISHED",
          drift_risk_score: drift_risk_score ?? 0.5,
          enabled: false, // Always start disabled
        })
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
        action: "logic.create",
        actor_type: "user",
        actor_id: user.id,
        resource_type: "logic",
        resource_id: data.logic_id,
        details: { name, task_type },
      });

      console.log("[admin-logic-bank] Created:", data.logic_id);
      return new Response(JSON.stringify(data), {
        status: 201,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    return new Response(
      JSON.stringify({ error: "METHOD_NOT_ALLOWED" }),
      { status: 405, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (error) {
    console.error("[admin-logic-bank] Error:", error);
    return new Response(
      JSON.stringify({ error: "INTERNAL_ERROR", message: String(error) }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
