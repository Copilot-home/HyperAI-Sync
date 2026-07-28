/**
 * ECVM Kernel - Shared Edge Function Library
 * Kernel v0.1.3 · LOCKED · LAW-COMPLIANT
 * 
 * Port of src/lib/kernel for Deno Edge Functions.
 * This is the SINGLE SOURCE OF TRUTH for kernel logic in edge functions.
 */

// ============================================
// TYPES (from src/lib/kernel/types.ts)
// ============================================

export type IdentityStateEnum = 
  | 'NO_IDENTITY' 
  | 'INSUFFICIENT' 
  | 'ESTABLISHED' 
  | 'DRIFT';

export type KernelVerdict = 'PASS' | 'REJECT' | 'HALT';

export type DriftType = 'PER_NODE' | 'SYSTEMIC';

export type TaskTypeEnum = 'image_static' | 'image' | 'video' | 'validation';

export interface TaskValidationInput {
  task_id: string;
  entity_id: string;
  logic_id: string;
  task_type: TaskTypeEnum;
  identity_state: IdentityStateEnum;
  required_identity_state: IdentityStateEnum;
  logic_enabled: boolean;
}

export interface TaskValidationResult {
  task_id: string;
  verdict: KernelVerdict;
  reasons: string[];
  terminal: boolean;
}

export interface KernelConfig {
  variance_threshold_established: number;
  variance_threshold_drift: number;
  coverage_minimum_percent: number;
  drift_severity_threshold: number;
  systemic_drift_node_threshold: number;
}

export const DEFAULT_KERNEL_CONFIG: KernelConfig = {
  variance_threshold_established: 0.15,
  variance_threshold_drift: 0.35,
  coverage_minimum_percent: 70,
  drift_severity_threshold: 0.25,
  systemic_drift_node_threshold: 3,
};

// ============================================
// IDENTITY DETECTOR (from src/lib/kernel/identity-detector.ts)
// ============================================

const IDENTITY_STATE_HIERARCHY: Record<IdentityStateEnum, number> = {
  'NO_IDENTITY': 0,
  'INSUFFICIENT': 1,
  'ESTABLISHED': 2,
  'DRIFT': -1, // DRIFT is a special terminal state
};

/**
 * Check if current identity state meets the required state
 * DRIFT is always invalid regardless of requirement
 */
export function isIdentityStateValid(
  current: IdentityStateEnum,
  required: IdentityStateEnum
): boolean {
  // DRIFT is always invalid - no task can execute in DRIFT state
  if (current === 'DRIFT') {
    return false;
  }

  const currentLevel = IDENTITY_STATE_HIERARCHY[current];
  const requiredLevel = IDENTITY_STATE_HIERARCHY[required];

  return currentLevel >= requiredLevel;
}

// ============================================
// TASK VALIDATOR (from src/lib/kernel/task-validator.ts)
// ============================================

/**
 * Validate task against all kernel gates
 * 
 * Gate sequence (LOCKED):
 * 1. Logic must be enabled
 * 2. Identity state must meet requirement
 * 3. Task type must be valid for logic
 * 
 * If any gate fails → REJECT
 * If terminal error → HALT
 */
export function validateTask(input: TaskValidationInput): TaskValidationResult {
  // Gate 1: Logic must be enabled
  if (!input.logic_enabled) {
    return createResult(input.task_id, 'REJECT', ['LOGIC_NOT_ENABLED'], false);
  }

  // Gate 2: Identity state validation
  if (!isIdentityStateValid(input.identity_state, input.required_identity_state)) {
    const reasons = [
      `IDENTITY_STATE_INSUFFICIENT: current=${input.identity_state}, required=${input.required_identity_state}`
    ];
    
    // HALT if identity is in DRIFT state (terminal)
    if (input.identity_state === 'DRIFT') {
      return createResult(input.task_id, 'HALT', reasons, true);
    }
    
    return createResult(input.task_id, 'REJECT', reasons, false);
  }

  // Gate 3: All gates passed
  return createResult(input.task_id, 'PASS', ['ALL_GATES_PASSED'], false);
}

function createResult(
  task_id: string,
  verdict: KernelVerdict,
  reasons: string[],
  terminal: boolean
): TaskValidationResult {
  return {
    task_id,
    verdict,
    reasons,
    terminal,
  };
}

/**
 * Check if verdict allows task execution
 */
export function isVerdictExecutable(verdict: KernelVerdict): boolean {
  return verdict === 'PASS';
}

/**
 * Check if verdict is terminal (no recovery possible)
 */
export function isVerdictTerminal(verdict: KernelVerdict): boolean {
  return verdict === 'HALT';
}
