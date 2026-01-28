/**
 * ECVM Kernel Types - v0.1.3
 * LOCKED · LAW-COMPLIANT
 * 
 * These types define the kernel's internal contracts.
 * No interpretation. No approximation.
 */

// Identity State Enum (matches DB)
export type IdentityStateEnum = 
  | 'NO_IDENTITY' 
  | 'INSUFFICIENT' 
  | 'ESTABLISHED' 
  | 'DRIFT';

// Kernel Verdict (immutable once issued)
export type KernelVerdict = 'PASS' | 'REJECT' | 'HALT';

// Drift Type Classification
export type DriftType = 'PER_NODE' | 'SYSTEMIC';

// Task Type Enum
export type TaskTypeEnum = 'image_static' | 'image' | 'video' | 'validation';

/**
 * Identity Embedding - geometric representation
 * NOT affective state. Pure geometric data.
 */
export interface IdentityEmbedding {
  entity_id: string;
  identity_hash: string;
  geometry_hash: string;
  variance_score: number;
  coverage_percent: number;
}

/**
 * Identity Validation Input
 */
export interface IdentityValidationInput {
  entity_id: string;
  current_embedding: IdentityEmbedding;
  reference_embeddings: IdentityEmbedding[];
}

/**
 * Identity State Result
 * System-computed, not user-editable
 */
export interface IdentityStateResult {
  entity_id: string;
  state: IdentityStateEnum;
  variance_score: number;
  coverage_percent: number;
  reasons: string[];
}

/**
 * Drift Detection Input
 */
export interface DriftDetectionInput {
  entity_id?: string;
  logic_id?: string;
  baseline_variance: number;
  current_variance: number;
  threshold: number;
}

/**
 * Drift Detection Result
 */
export interface DriftDetectionResult {
  detected: boolean;
  drift_type: DriftType | null;
  severity: number;
  delta: number;
  requires_action: boolean;
  action_authority: 'USER' | 'ADMIN' | null;
}

/**
 * Task Validation Input
 */
export interface TaskValidationInput {
  task_id: string;
  entity_id: string;
  logic_id: string;
  task_type: TaskTypeEnum;
  identity_state: IdentityStateEnum;
  required_identity_state: IdentityStateEnum;
  logic_enabled: boolean;
}

/**
 * Task Validation Result
 */
export interface TaskValidationResult {
  task_id: string;
  verdict: KernelVerdict;
  reasons: string[];
  terminal: boolean;
}

/**
 * Kernel Configuration (thresholds)
 * Admin-owned, not user-mutable
 */
export interface KernelConfig {
  variance_threshold_established: number;
  variance_threshold_drift: number;
  coverage_minimum_percent: number;
  drift_severity_threshold: number;
  systemic_drift_node_threshold: number;
}

/**
 * Default Kernel Configuration
 */
export const DEFAULT_KERNEL_CONFIG: KernelConfig = {
  variance_threshold_established: 0.15,
  variance_threshold_drift: 0.35,
  coverage_minimum_percent: 70,
  drift_severity_threshold: 0.25,
  systemic_drift_node_threshold: 3,
};
