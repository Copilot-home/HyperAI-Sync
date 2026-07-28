// ECVM API: POST /v1/task/execute
// Execute a task through Kernel (FAIL-CLOSED)
// Spec: ECVM-CS-1.0 · Kernel v0.1.3

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import {
  validateTask,
  isVerdictExecutable,
  isVerdictTerminal,
  TaskValidationInput,
  IdentityStateEnum,
  TaskTypeEnum,
} from "../_shared/kernel.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
};

interface TaskRequest {
  task_type: TaskTypeEnum;
  logic_ids: string[];
  entity_id: string;
}

interface LogicModule {
  logic_id: string;
  task_type: TaskTypeEnum;
  enabled: boolean;
  required_identity_state: IdentityStateEnum;
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

    // KERNEL GATE 0: Verify authenticated user
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

    // KERNEL GATE 3: Fetch and validate logic modules
    const { data: modules, error: modulesError } = await userClient
      .from("logic_module")
      .select("logic_id, task_type, enabled, required_identity_state")
      .in("logic_id", logic_ids ?? []);

    if (modulesError) {
      console.error("[task-execute] Logic fetch error:", modulesError.message);
      return new Response(
        JSON.stringify({ error: "LOGIC_FETCH_ERROR", message: modulesError.message }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const logicModules: LogicModule[] = modules ?? [];
    const requestedLogicIds = logic_ids ?? [];

    // Check for missing logic modules
    const foundLogicIds = logicModules.map((m) => m.logic_id);
    const missingLogic = requestedLogicIds.filter((id) => !foundLogicIds.includes(id));

    if (missingLogic.length > 0) {
      console.log("[task-execute] REJECT: Missing logic:", missingLogic);
      
      await kernelClient.from("task_execution_log").insert({
        entity_id,
        task_type,
        verdict: "REJECT",
        logic_applied: [],
        execution_time_ms: 0,
        metadata: { reason: "Requested logic not found", missing: missingLogic },
      });

      return new Response(
        JSON.stringify({
          task_id: null,
          status: "rejected",
          verdict: "REJECT",
          reason: {
            code: "LOGIC_NOT_FOUND",
            message: "Requested logic modules not found",
            technical_detail: `Missing: ${missingLogic.join(", ")}`,
          },
        }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // KERNEL GATE 4: Validate each logic module through Kernel
    const executionStart = Date.now();
    const validationResults: { logic_id: string; verdict: string; reasons: string[]; terminal: boolean }[] = [];

    for (const logic of logicModules) {
      const validationInput: TaskValidationInput = {
        task_id: `temp-${Date.now()}`,
        entity_id,
        logic_id: logic.logic_id,
        task_type: logic.task_type,
        identity_state: state.state as IdentityStateEnum,
        required_identity_state: logic.required_identity_state as IdentityStateEnum,
        logic_enabled: logic.enabled,
      };

      const result = validateTask(validationInput);
      validationResults.push({
        logic_id: logic.logic_id,
        verdict: result.verdict,
        reasons: result.reasons,
        terminal: result.terminal,
      });

      // FAIL-CLOSED: Stop on first non-PASS verdict
      if (!isVerdictExecutable(result.verdict)) {
        console.log(`[task-execute] ${result.verdict}: ${result.reasons.join(", ")}`);

        // Log the verdict
        await kernelClient.from("task_execution_log").insert({
          entity_id,
          task_type,
          verdict: result.verdict,
          logic_id: logic.logic_id,
          logic_applied: [],
          execution_time_ms: Date.now() - executionStart,
          metadata: { 
            reason: result.reasons.join("; "),
            identity_state: state.state,
            required_state: logic.required_identity_state,
          },
        });

        return new Response(
          JSON.stringify({
            task_id: null,
            status: isVerdictTerminal(result.verdict) ? "halted" : "rejected",
            verdict: result.verdict,
            reason: {
              code: result.reasons[0]?.split(":")[0] ?? result.verdict,
              message: `Task validation failed for logic ${logic.logic_id}`,
              technical_detail: result.reasons.join("; "),
            },
          }),
          { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }
    }

    // KERNEL EXECUTION: All gates passed
    const executionTime = Date.now() - executionStart;
    const approvedLogicIds = logicModules.map((m) => m.logic_id);

    // Log PASS verdict
    const { data: taskLog, error: logError } = await kernelClient
      .from("task_execution_log")
      .insert({
        entity_id,
        task_type,
        verdict: "PASS",
        logic_applied: approvedLogicIds,
        execution_time_ms: executionTime,
        metadata: { 
          coverage: state.coverage_percent, 
          variance: state.variance_score,
          validation_results: validationResults,
        },
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
