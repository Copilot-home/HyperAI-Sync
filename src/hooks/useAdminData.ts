import { useQuery } from "@tanstack/react-query";
import { 
  AdminOverview, 
  LogicBankEntry, 
  UnmetLogicEntry, 
  DriftEntry, 
  AuditLogEntry 
} from "@/types/ecvm";

// Mock admin data endpoints - service_role authenticated

async function fetchAdminOverview(): Promise<AdminOverview> {
  await new Promise(resolve => setTimeout(resolve, 400));
  return {
    total_entities: 1247,
    active_entities: 1189,
    total_tasks_today: 3842,
    pass_rate: 94.2,
    unmet_logic_count: 23,
    active_drift_count: 7,
  };
}

async function fetchLogicBank(): Promise<LogicBankEntry[]> {
  await new Promise(resolve => setTimeout(resolve, 500));
  return [
    {
      logic_id: "lg_face_detect",
      name: "Face Detection",
      description: "Validates presence and quality of facial features",
      version: "2.1.0",
      status: "active",
      created_at: "2025-01-15T10:00:00Z",
      updated_at: "2025-01-25T14:30:00Z",
    },
    {
      logic_id: "lg_age_verify",
      name: "Age Verification",
      description: "Cross-references age markers with reference data",
      version: "1.8.2",
      status: "active",
      created_at: "2025-01-10T08:00:00Z",
      updated_at: "2025-01-20T11:15:00Z",
    },
    {
      logic_id: "lg_liveness",
      name: "Liveness Check",
      description: "Anti-spoofing verification for live capture",
      version: "3.0.1",
      status: "active",
      created_at: "2025-01-08T09:00:00Z",
      updated_at: "2025-01-27T16:45:00Z",
    },
    {
      logic_id: "lg_doc_match_v1",
      name: "Document Matching (Legacy)",
      description: "Legacy document verification system",
      version: "1.0.0",
      status: "deprecated",
      created_at: "2024-06-01T10:00:00Z",
      updated_at: "2025-01-01T00:00:00Z",
    },
    {
      logic_id: "lg_motion_track",
      name: "Motion Tracking",
      description: "Analyzes motion patterns in video content",
      version: "2.5.0",
      status: "active",
      created_at: "2025-01-12T13:00:00Z",
      updated_at: "2025-01-26T09:30:00Z",
    },
  ];
}

async function fetchUnmetLogic(): Promise<UnmetLogicEntry[]> {
  await new Promise(resolve => setTimeout(resolve, 450));
  return [
    {
      id: "unmet_001",
      entity_id: "ent_a1b2c3d4",
      logic_id: "lg_doc_match",
      reason: "Document upload pending verification",
      detected_at: "2025-01-28T10:15:00Z",
      severity: "high",
    },
    {
      id: "unmet_002",
      entity_id: "ent_e5f6g7h8",
      logic_id: "lg_liveness",
      reason: "Liveness check failed - retry required",
      detected_at: "2025-01-28T09:45:00Z",
      severity: "critical",
    },
    {
      id: "unmet_003",
      entity_id: "ent_i9j0k1l2",
      logic_id: "lg_age_verify",
      reason: "Age reference data expired",
      detected_at: "2025-01-27T14:30:00Z",
      severity: "medium",
    },
  ];
}

async function fetchDrift(): Promise<DriftEntry[]> {
  await new Promise(resolve => setTimeout(resolve, 400));
  return [
    {
      id: "drift_001",
      entity_id: "ent_m3n4o5p6",
      drift_type: "face_embedding",
      delta: 0.12,
      baseline: 0.95,
      current: 0.83,
      detected_at: "2025-01-28T11:00:00Z",
      acknowledged: false,
    },
    {
      id: "drift_002",
      entity_id: "ent_q7r8s9t0",
      drift_type: "age_marker",
      delta: 0.08,
      baseline: 0.92,
      current: 0.84,
      detected_at: "2025-01-28T08:30:00Z",
      acknowledged: true,
    },
  ];
}

async function fetchAuditLog(): Promise<AuditLogEntry[]> {
  await new Promise(resolve => setTimeout(resolve, 550));
  return [
    {
      id: "audit_001",
      action: "task.execute",
      actor_type: "user",
      actor_id: "usr_abc123",
      resource_type: "task",
      resource_id: "task_xyz789",
      timestamp: "2025-01-28T11:30:00Z",
      details: { task_type: "image", logic_count: 3 },
    },
    {
      id: "audit_002",
      action: "logic.update",
      actor_type: "service_role",
      actor_id: "svc_system",
      resource_type: "logic",
      resource_id: "lg_face_detect",
      timestamp: "2025-01-28T10:00:00Z",
      details: { version: "2.1.0", change_type: "patch" },
    },
    {
      id: "audit_003",
      action: "entity.reference_upload",
      actor_type: "user",
      actor_id: "usr_def456",
      resource_type: "entity",
      resource_id: "ent_7f3a9c2d",
      timestamp: "2025-01-28T09:15:00Z",
      details: { file_count: 2 },
    },
    {
      id: "audit_004",
      action: "drift.acknowledge",
      actor_type: "user",
      actor_id: "usr_ghi789",
      resource_type: "drift",
      resource_id: "drift_002",
      timestamp: "2025-01-28T08:45:00Z",
      details: {},
    },
  ];
}

export function useAdminOverview() {
  return useQuery({
    queryKey: ["admin-overview"],
    queryFn: fetchAdminOverview,
    staleTime: 30000,
  });
}

export function useLogicBank() {
  return useQuery({
    queryKey: ["logic-bank"],
    queryFn: fetchLogicBank,
    staleTime: 60000,
  });
}

export function useUnmetLogic() {
  return useQuery({
    queryKey: ["unmet-logic"],
    queryFn: fetchUnmetLogic,
    staleTime: 30000,
  });
}

export function useDrift() {
  return useQuery({
    queryKey: ["drift"],
    queryFn: fetchDrift,
    staleTime: 30000,
  });
}

export function useAuditLog() {
  return useQuery({
    queryKey: ["audit-log"],
    queryFn: fetchAuditLog,
    staleTime: 30000,
  });
}
