// ECVM API: POST /v1/entity/reference
// Handle reference image upload and trigger identity processing
// Spec: ECVM-CS-1.0 (User Node - Reference Upload)

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
      return new Response(
        JSON.stringify({ error: "UNAUTHORIZED" }),
        { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    console.log("[entity-reference] User:", user.id, "Method:", req.method);

    if (req.method === "GET") {
      // List user's reference images
      const { data: files, error: listError } = await supabaseClient.storage
        .from("entity-references")
        .list(user.id, { limit: 100, sortBy: { column: "created_at", order: "desc" } });

      if (listError) {
        console.error("[entity-reference] List error:", listError);
        return new Response(
          JSON.stringify({ error: "STORAGE_ERROR", message: listError.message }),
          { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      // Get entity_id for this user
      const { data: entityData } = await serviceClient
        .from("entity_identity")
        .select("entity_id")
        .eq("owner_user_id", user.id)
        .maybeSingle();

      // Get identity state
      let identityState = null;
      if (entityData?.entity_id) {
        const { data: stateData } = await serviceClient
          .from("identity_state")
          .select("*")
          .eq("entity_id", entityData.entity_id)
          .maybeSingle();
        identityState = stateData;
      }

      const imageFiles = (files ?? []).filter(f => 
        f.name.match(/\.(jpg|jpeg|png|webp)$/i)
      );

      return new Response(
        JSON.stringify({
          entity_id: entityData?.entity_id ?? null,
          reference_count: imageFiles.length,
          files: imageFiles.map(f => ({
            name: f.name,
            size: f.metadata?.size ?? 0,
            created_at: f.created_at,
          })),
          identity_state: identityState,
        }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    if (req.method === "POST") {
      // Process uploaded references and update identity state
      // This is called after files are uploaded via storage API

      // Count reference images
      const { data: files, error: listError } = await supabaseClient.storage
        .from("entity-references")
        .list(user.id, { limit: 100 });

      if (listError) {
        return new Response(
          JSON.stringify({ error: "STORAGE_ERROR", message: listError.message }),
          { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      const imageFiles = (files ?? []).filter(f => 
        f.name.match(/\.(jpg|jpeg|png|webp)$/i)
      );
      const refCount = imageFiles.length;

      // Get entity_id
      const { data: entityData, error: entityError } = await serviceClient
        .from("entity_identity")
        .select("entity_id")
        .eq("owner_user_id", user.id)
        .maybeSingle();

      if (entityError || !entityData) {
        return new Response(
          JSON.stringify({ error: "NO_ENTITY", message: "Entity not initialized" }),
          { status: 404, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      // ECVM Logic: Calculate coverage and state based on reference count
      // This is a simplified model - real implementation would use ML embeddings
      let newState: "NO_IDENTITY" | "INSUFFICIENT" | "ESTABLISHED" = "NO_IDENTITY";
      let coveragePercent = 0;
      let varianceScore = 1.0;

      if (refCount === 0) {
        newState = "NO_IDENTITY";
        coveragePercent = 0;
        varianceScore = 1.0;
      } else if (refCount < 5) {
        newState = "INSUFFICIENT";
        coveragePercent = Math.min(refCount * 15, 60);
        varianceScore = 1.0 - (refCount * 0.1);
      } else if (refCount < 10) {
        newState = "INSUFFICIENT";
        coveragePercent = 60 + (refCount - 5) * 6;
        varianceScore = 0.5 - ((refCount - 5) * 0.05);
      } else {
        newState = "ESTABLISHED";
        coveragePercent = Math.min(90 + (refCount - 10) * 2, 100);
        varianceScore = Math.max(0.1, 0.25 - ((refCount - 10) * 0.01));
      }

      // Update identity_state (service_role only per ECVM spec)
      const { error: updateError } = await serviceClient
        .from("identity_state")
        .update({
          state: newState,
          coverage_percent: coveragePercent,
          variance_score: varianceScore,
          updated_at: new Date().toISOString(),
        })
        .eq("entity_id", entityData.entity_id);

      if (updateError) {
        console.error("[entity-reference] Update error:", updateError);
        return new Response(
          JSON.stringify({ error: "DB_ERROR", message: updateError.message }),
          { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      // Log to audit
      await serviceClient.from("audit_log").insert({
        action: "identity.reference_processed",
        actor_type: "system",
        actor_id: user.id,
        resource_type: "entity",
        resource_id: entityData.entity_id,
        details: {
          reference_count: refCount,
          new_state: newState,
          coverage_percent: coveragePercent,
        },
      });

      console.log("[entity-reference] Updated state:", newState, "Coverage:", coveragePercent);

      return new Response(
        JSON.stringify({
          entity_id: entityData.entity_id,
          reference_count: refCount,
          state: newState,
          coverage_percent: coveragePercent,
          variance_score: varianceScore,
        }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    return new Response(
      JSON.stringify({ error: "METHOD_NOT_ALLOWED" }),
      { status: 405, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (error) {
    console.error("[entity-reference] Error:", error);
    return new Response(
      JSON.stringify({ error: "INTERNAL_ERROR", message: String(error) }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
