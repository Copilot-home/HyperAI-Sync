// ECVM API: POST /v1/task/execute
// Execute a task through Kernel (FAIL-CLOSED)
// Spec: ECVM-CS-1.0 (One action = One API call, no retries, no preview)

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
};

interface TaskRequest {
  task_type: "image" | "image_static" | "video";
  logic_ids: string[];
  entity_id: string;
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
    // Create client with user auth
    const userClient = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_ANON_KEY") ?? "",
      {
        global: {
          headers: { Authorization: req.headers.get("Authorization") ?? "" },
        },
      }
    );

    // Service role client for Kernel operations
    const kernelClient = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? ""
    );

    // Verify authenticated user
    const {
      data: { user },
      error: authError,
    } = await userClient.auth.getUser();

    if (authError || !user) {
      console.error("[task-execute] Auth error:", authError?.message);
      return new Response(
        JSON.stringify({ error: "UNAUTHORIZED", message: "Authentication required" }),
        { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    console.log("[task-execute] User authenticated:", user.id);

    // Parse request body
    const body: TaskRequest = await req.json();
    const { task_type, logic_ids, entity_id } = body;

    // Validate required fields
    if (!task_type || !entity_id) {
      return new Response(
        JSON.stringify({ error: "INVALID_REQUEST", message: "task_type and entity_id required" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    console.log("[task-execute] Request:", { task_type, logic_ids, entity_id });

    // KERNEL GATE 1: Verify entity ownership
    const { data: identity, error: identityError } = await userClient
      .from("entity_identity")
      .select("entity_id, owner_user_id")
      .eq("entity_id", entity_id)
      .eq("owner_user_id", user.id)
      .maybeSingle();

    if (identityError || !identity) {
      console.error("[task-execute] Entity not found or not owned");
      return new Response(
        JSON.stringify({ 
          error: "ENTITY_NOT_FOUND", 
          message: "Entity does not exist or is not owned by user" 
        }),
        { status: 403, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // KERNEL GATE 2: Check identity state
    const { data: state, error: stateError } = await userClient
      .from("identity_state")
      .select("state, variance_score, coverage_percent")
      .eq("entity_id", entity_id)
      .maybeSingle();

    if (stateError || !state) {
      console.error("[task-execute] State not found");
      return new Response(
        JSON.stringify({ error: "STATE_NOT_FOUND", message: "Identity state not found" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // KERNEL GATE 3: Fail-closed check
    const allowedStates = ["ESTABLISHED"];
    if (!allowedStates.includes(state.state)) {
      console.log("[task-execute] HALT: Identity state not ESTABLISHED:", state.state);
      
      // Log HALT verdict
      await kernelClient.from("task_execution_log").insert({
        entity_id,
        task_type,
        verdict: "HALT",
        logic_applied: logic_ids ?? [],
        execution_time_ms: 0,
        metadata: { reason: `Identity state is ${state.state}, required ESTABLISHED` },
      });

      return new Response(
        JSON.stringify({
          task_id: null,
          status: "halted",
          verdict: "HALT",
          reason: {
            code: "IDENTITY_NOT_ESTABLISHED",
            message: `Cannot execute: identity state is ${state.state}`,
            technical_detail: "Kernel requires ESTABLISHED state for task execution",
          },
        }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // KERNEL GATE 4: Verify logic availability
    const { data: modules } = await userClient
      .from("logic_module")
      .select("logic_id, task_type, enabled")
      .in("logic_id", logic_ids ?? [])
      .eq("enabled", true);

    const availableLogicIds = (modules ?? []).map((m) => m.logic_id);
    const unavailableLogic = (logic_ids ?? []).filter((id) => !availableLogicIds.includes(id));

    if (unavailableLogic.length > 0) {
      console.log("[task-execute] REJECT: Unavailable logic:", unavailableLogic);
      
      // Log REJECT verdict
      await kernelClient.from("task_execution_log").insert({
        entity_id,
        task_type,
        verdict: "REJECT",
        logic_applied: [],
        execution_time_ms: 0,
        metadata: { reason: "Requested logic not available", unavailable: unavailableLogic },
      });

      return new Response(
        JSON.stringify({
          task_id: null,
          status: "rejected",
          verdict: "REJECT",
          reason: {
            code: "LOGIC_UNAVAILABLE",
            message: "Requested logic modules are not available",
            technical_detail: `Unavailable: ${unavailableLogic.join(", ")}`,
          },
        }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // KERNEL EXECUTION: Task passes all gates
    const executionStart = Date.now();
    
    // TODO: Actual ML rendering pipeline would go here
    // For now, simulate successful execution
    
    const executionTime = Date.now() - executionStart;

    // Log PASS verdict
    const { data: taskLog, error: logError } = await kernelClient
      .from("task_execution_log")
      .insert({
        entity_id,
        task_type,
        verdict: "PASS",
        logic_applied: availableLogicIds,
        execution_time_ms: executionTime,
        metadata: { coverage: state.coverage_percent, variance: state.variance_score },
      })
      .select("task_id, executed_at")
      .single();

    if (logError) {
      console.error("[task-execute] Failed to log task:", logError.message);
      return new Response(
        JSON.stringify({ error: "LOG_ERROR", message: logError.message }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    console.log("[task-execute] PASS:", taskLog.task_id);

    return new Response(
      JSON.stringify({
        task_id: taskLog.task_id,
        status: "completed",
        verdict: "PASS",
        created_at: taskLog.executed_at,
      }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (error) {
    console.error("[task-execute] Unexpected error:", error);
    return new Response(
      JSON.stringify({ error: "INTERNAL_ERROR", message: String(error) }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
