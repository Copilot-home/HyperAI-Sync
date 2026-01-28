// ECVM API: POST /v1/logic/unmet
// Record unmet logic signals when user attempts task with unavailable logic
// Spec: ECVM-CS-1.0 (User Node - Unmet Logic Signal)

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
};

interface UnmetLogicRequest {
  entity_id: string;
  requested_task: string;
  observed_state: string;
  unavailable_logic_ids: string[];
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  if (req.method !== "POST") {
    return new Response(
      JSON.stringify({ error: "METHOD_NOT_ALLOWED" }),
      { status: 405, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }

  try {
    const supabaseClient = createClient(
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
    } = await supabaseClient.auth.getUser();

    if (authError || !user) {
      console.error("[logic-unmet] Auth error:", authError?.message);
      return new Response(
        JSON.stringify({ error: "UNAUTHORIZED", message: "Authentication required" }),
        { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Parse request body
    const body: UnmetLogicRequest = await req.json();
    
    // Validate required fields
    if (!body.entity_id || !body.requested_task || !body.observed_state) {
      return new Response(
        JSON.stringify({ error: "INVALID_REQUEST", message: "Missing required fields" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    console.log("[logic-unmet] Signal from user:", user.id, "Entity:", body.entity_id);

    // Verify entity belongs to user
    const { data: entity } = await serviceClient
      .from("entity_identity")
      .select("entity_id")
      .eq("entity_id", body.entity_id)
      .eq("owner_user_id", user.id)
      .maybeSingle();

    if (!entity) {
      return new Response(
        JSON.stringify({ error: "ENTITY_NOT_FOUND", message: "Entity not found or not owned by user" }),
        { status: 404, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Determine severity based on state and logic count
    let severity = "low";
    if (body.observed_state === "NO_IDENTITY") {
      severity = "critical";
    } else if (body.observed_state === "DRIFT") {
      severity = "high";
    } else if (body.observed_state === "INSUFFICIENT") {
      severity = "medium";
    } else if ((body.unavailable_logic_ids?.length ?? 0) > 2) {
      severity = "medium";
    }

    // Build reason string
    const reason = body.unavailable_logic_ids?.length > 0
      ? `Requested ${body.unavailable_logic_ids.length} unavailable logic module(s) for ${body.requested_task}`
      : `Attempted ${body.requested_task} task in ${body.observed_state} state`;

    // Insert unmet logic signal
    const { data: signal, error: insertError } = await serviceClient
      .from("unmet_logic_signal")
      .insert({
        entity_id: body.entity_id,
        requested_task: body.requested_task,
        observed_state: body.observed_state,
        severity,
        reason,
      })
      .select("signal_id, severity, created_at")
      .single();

    if (insertError) {
      console.error("[logic-unmet] Insert error:", insertError);
      return new Response(
        JSON.stringify({ error: "DB_ERROR", message: insertError.message }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Log to audit
    await serviceClient.from("audit_log").insert({
      action: "logic.unmet_signal",
      actor_type: "user",
      actor_id: user.id,
      resource_type: "unmet_logic_signal",
      resource_id: signal.signal_id,
      details: {
        entity_id: body.entity_id,
        requested_task: body.requested_task,
        observed_state: body.observed_state,
        unavailable_logic_ids: body.unavailable_logic_ids,
        severity,
      },
    });

    console.log("[logic-unmet] Signal created:", signal.signal_id, "Severity:", severity);

    return new Response(
      JSON.stringify(signal),
      { status: 201, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (error) {
    console.error("[logic-unmet] Error:", error);
    return new Response(
      JSON.stringify({ error: "INTERNAL_ERROR", message: String(error) }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
