// ECVM API: GET /v1/entity/state
// Returns identity state for authenticated user's entity
// Spec: ECVM-CS-1.0 (User Node READ only)

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
};

Deno.serve(async (req) => {
  // Handle CORS preflight
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
      console.error("[entity-state] Auth error:", authError?.message);
      return new Response(
        JSON.stringify({ error: "UNAUTHORIZED", message: "Authentication required" }),
        { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    console.log("[entity-state] User authenticated:", user.id);

    // Get entity identity for this user
    const { data: identity, error: identityError } = await supabase
      .from("entity_identity")
      .select("entity_id, identity_hash, geometry_hash, created_at, locked")
      .eq("owner_user_id", user.id)
      .maybeSingle();

    if (identityError) {
      console.error("[entity-state] Identity fetch error:", identityError.message);
      return new Response(
        JSON.stringify({ error: "DB_ERROR", message: identityError.message }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // No identity exists yet
    if (!identity) {
      console.log("[entity-state] No identity found for user");
      return new Response(
        JSON.stringify({
          entity_id: null,
          status: "NO_IDENTITY",
          coverage_percent: 0,
          variance: 1.0,
          reference_uploaded: false,
          last_sync: null,
          metadata: {},
        }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Get identity state
    const { data: state, error: stateError } = await supabase
      .from("identity_state")
      .select("state, variance_score, coverage_percent, updated_at")
      .eq("entity_id", identity.entity_id)
      .maybeSingle();

    if (stateError) {
      console.error("[entity-state] State fetch error:", stateError.message);
      return new Response(
        JSON.stringify({ error: "DB_ERROR", message: stateError.message }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Map state enum to API response
    const statusMap: Record<string, string> = {
      NO_IDENTITY: "pending",
      INSUFFICIENT: "pending",
      ESTABLISHED: "active",
      DRIFT: "suspended",
    };

    const response = {
      entity_id: identity.entity_id,
      status: statusMap[state?.state ?? "NO_IDENTITY"] ?? "unknown",
      coverage_percent: state?.coverage_percent ?? 0,
      variance: state?.variance_score ?? 1.0,
      reference_uploaded: true,
      last_sync: state?.updated_at ?? identity.created_at,
      metadata: {
        identity_state: state?.state ?? "NO_IDENTITY",
        locked: identity.locked,
      },
    };

    console.log("[entity-state] Response:", response.entity_id, response.status);
    return new Response(JSON.stringify(response), {
      status: 200,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error("[entity-state] Unexpected error:", error);
    return new Response(
      JSON.stringify({ error: "INTERNAL_ERROR", message: String(error) }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
