// ECVM Type Definitions - Strict contract types

export type TaskType = 'image' | 'image_static' | 'video';
export type VerdictStatus = 'PASS' | 'REJECT' | 'HALT';
export type EntityStatus = 'active' | 'pending' | 'suspended' | 'unknown';

export interface EntityState {
  entity_id: string;
  status: EntityStatus;
  coverage_percent: number;
  variance: number;
  reference_uploaded: boolean;
  last_sync: string;
  metadata: Record<string, unknown>;
}

export interface LogicRule {
  logic_id: string;
  name: string;
  description: string;
  available: boolean;
  required: boolean;
  category: string;
}

export interface TaskExecutionRequest {
  task_type: TaskType;
  logic_ids: string[];
  entity_id: string;
}

export interface TaskExecutionResponse {
  task_id: string;
  status: 'queued' | 'processing' | 'completed' | 'failed';
  created_at: string;
}

export interface TaskExecutionLog {
  id: string;
  task_id: string;
  entity_id: string;
  task_type: TaskType;
  verdict: VerdictStatus;
  logic_applied: string[];
  executed_at: string;
  execution_time_ms: number;
  metadata: Record<string, unknown>;
}

export interface DisableReason {
  code: string;
  message: string;
  technical_detail: string;
}

export interface WorkflowSettings {
  default_task_type: TaskType;
  auto_select_required_logic: boolean;
  max_concurrent_tasks: number;
}

// Admin Types
export interface LogicBankEntry {
  logic_id: string;
  name: string;
  description: string;
  version: string;
  status: 'active' | 'deprecated' | 'draft';
  created_at: string;
  updated_at: string;
}

export interface UnmetLogicEntry {
  id: string;
  entity_id: string;
  logic_id: string;
  reason: string;
  detected_at: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
}

export interface DriftEntry {
  id: string;
  entity_id: string;
  drift_type: string;
  delta: number;
  baseline: number;
  current: number;
  detected_at: string;
  acknowledged: boolean;
}

export interface AuditLogEntry {
  id: string;
  action: string;
  actor_type: 'user' | 'system' | 'service_role';
  actor_id: string;
  resource_type: string;
  resource_id: string;
  timestamp: string;
  details: Record<string, unknown>;
}

export interface AdminOverview {
  total_entities: number;
  active_entities: number;
  total_tasks_today: number;
  pass_rate: number;
  unmet_logic_count: number;
  active_drift_count: number;
}
