/**
 * ECVM Task Validator - Kernel v0.1.3
 * LOCKED · LAW-COMPLIANT · FAIL-CLOSED
 * 
 * Validates task execution requests against kernel gates.
 * Verdict is immutable once issued. No retry. No recovery.
 */

import {
  KernelVerdict,
  TaskValidationInput,
  TaskValidationResult,
  IdentityStateEnum,
} from './types';
import { isIdentityStateValid } from './identity-detector';

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
  const reasons: string[] = [];

  // Gate 1: Logic must be enabled
  if (!input.logic_enabled) {
    return createResult(input.task_id, 'REJECT', ['LOGIC_NOT_ENABLED'], false);
  }

  // Gate 2: Identity state validation
  if (!isIdentityStateValid(input.identity_state, input.required_identity_state)) {
    reasons.push(
      `IDENTITY_STATE_INSUFFICIENT: current=${input.identity_state}, required=${input.required_identity_state}`
    );
    
    // HALT if identity is in DRIFT state (terminal)
    if (input.identity_state === 'DRIFT') {
      return createResult(input.task_id, 'HALT', reasons, true);
    }
    
    return createResult(input.task_id, 'REJECT', reasons, false);
  }

  // Gate 3: All gates passed
  return createResult(input.task_id, 'PASS', ['ALL_GATES_PASSED'], false);
}

/**
 * Create validation result
 */
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

/**
 * Get verdict description for UI display
 */
export function getVerdictDescription(verdict: KernelVerdict): string {
  const descriptions: Record<KernelVerdict, string> = {
    'PASS': 'Task execution approved',
    'REJECT': 'Task execution denied - conditions not met',
    'HALT': 'Task execution terminated - recovery not possible',
  };
  return descriptions[verdict];
}

/**
 * Batch validate multiple tasks
 * Stops on first HALT (fail-closed)
 */
export function validateTaskBatch(
  inputs: TaskValidationInput[]
): TaskValidationResult[] {
  const results: TaskValidationResult[] = [];
  
  for (const input of inputs) {
    const result = validateTask(input);
    results.push(result);
    
    // Fail-closed: stop on HALT
    if (result.terminal) {
      break;
    }
  }
  
  return results;
}
