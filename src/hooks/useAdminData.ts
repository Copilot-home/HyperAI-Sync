import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { 
  AdminOverview, 
  LogicBankEntry, 
  UnmetLogicEntry, 
  DriftEntry, 
  AuditLogEntry 
} from "@/types/ecvm";

// Admin endpoints - service_role authenticated via Edge Functions

async function fetchAdminOverview(): Promise<AdminOverview> {
  const { data, error } = await supabase.functions.invoke("admin-overview", {
    method: "GET",
  });

  if (error) {
    console.error("[useAdminOverview] Edge function error:", error);
    throw new Error(error.message || "Failed to fetch admin overview");
  }

  return {
    total_entities: data.total_entities ?? 0,
    active_entities: data.active_entities ?? 0,
    total_tasks_today: data.total_tasks_today ?? 0,
    pass_rate: data.pass_rate ?? 0,
    unmet_logic_count: data.unmet_logic_count ?? 0,
    active_drift_count: data.active_drift_count ?? 0,
  };
}

async function fetchLogicBank(): Promise<LogicBankEntry[]> {
  const { data, error } = await supabase.functions.invoke("admin-logic-bank", {
    method: "GET",
  });

  if (error) {
    console.error("[useLogicBank] Edge function error:", error);
    throw new Error(error.message || "Failed to fetch logic bank");
  }

  return (data ?? []).map((m: Record<string, unknown>) => ({
    logic_id: m.logic_id as string,
    name: m.name as string,
    description: m.description as string,
    version: String(m.version ?? "1"),
    status: (m.enabled ? "active" : "draft") as LogicBankEntry["status"],
    enabled: m.enabled as boolean,
    created_at: m.created_at as string,
    updated_at: m.updated_at as string,
  }));
}

async function fetchUnmetLogic(): Promise<UnmetLogicEntry[]> {
  const { data, error } = await supabase.functions.invoke("admin-unmet-logic", {
    method: "GET",
  });

  if (error) {
    console.error("[useUnmetLogic] Edge function error:", error);
    throw new Error(error.message || "Failed to fetch unmet logic");
  }

  return (data ?? []).map((s: Record<string, unknown>) => ({
    id: s.signal_id as string,
    entity_id: s.entity_id as string,
    requested_task: s.requested_task as string,
    observed_state: s.observed_state as string,
    reason: s.reason as string,
    detected_at: s.created_at as string,
    severity: s.severity as UnmetLogicEntry["severity"],
  }));
}

async function fetchDrift(): Promise<DriftEntry[]> {
  const { data, error } = await supabase.functions.invoke("admin-drift", {
    method: "GET",
  });

  if (error) {
    console.error("[useDrift] Edge function error:", error);
    throw new Error(error.message || "Failed to fetch drift data");
  }

  return (data ?? []).map((d: Record<string, unknown>) => {
    const baseline = (d.baseline as number) ?? 0;
    const current = (d.current_value as number) ?? (d.current as number) ?? 0;
    return {
      id: d.drift_id as string,
      entity_id: d.entity_id as string,
      drift_type: d.drift_type as string,
      delta: current - baseline,
      baseline,
      current,
      detected_at: d.detected_at as string,
      acknowledged: d.acknowledged as boolean,
    };
  });
}

async function fetchAuditLog(): Promise<AuditLogEntry[]> {
  const { data, error } = await supabase.functions.invoke("admin-audit", {
    method: "GET",
  });

  if (error) {
    console.error("[useAuditLog] Edge function error:", error);
    throw new Error(error.message || "Failed to fetch audit log");
  }

  return (data ?? []).map((a: Record<string, unknown>) => ({
    id: a.id as string,
    action: a.action as string,
    actor_type: a.actor_type as AuditLogEntry["actor_type"],
    actor_id: a.actor_id as string,
    resource_type: a.resource_type as string,
    resource_id: a.resource_id as string,
    timestamp: a.timestamp as string,
    details: (a.details as Record<string, unknown>) ?? {},
  }));
}

export function useAdminOverview() {
  return useQuery({
    queryKey: ["admin-overview"],
    queryFn: fetchAdminOverview,
    staleTime: 30000,
    retry: false, // ECVM: fail-closed
  });
}

export function useLogicBank() {
  return useQuery({
    queryKey: ["logic-bank"],
    queryFn: fetchLogicBank,
    staleTime: 60000,
    retry: false,
  });
}

export function useUnmetLogic() {
  return useQuery({
    queryKey: ["unmet-logic"],
    queryFn: fetchUnmetLogic,
    staleTime: 30000,
    retry: false,
  });
}

export function useDrift() {
  return useQuery({
    queryKey: ["drift"],
    queryFn: fetchDrift,
    staleTime: 30000,
    retry: false,
  });
}

export function useAuditLog() {
  return useQuery({
    queryKey: ["audit-log"],
    queryFn: fetchAuditLog,
    staleTime: 30000,
    retry: false,
  });
}
