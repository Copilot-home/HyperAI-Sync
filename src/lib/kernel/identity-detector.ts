/**
 * ECVM Identity State Detector - Kernel v0.1.3
 * LOCKED · LAW-COMPLIANT · FAIL-CLOSED
 * 
 * Determines identity state based on geometric data.
 * No interpretation. No approximation. Existence-first.
 */

import {
  IdentityStateEnum,
  IdentityValidationInput,
  IdentityStateResult,
  KernelConfig,
  DEFAULT_KERNEL_CONFIG,
} from './types';

/**
 * Compute identity state from embeddings
 * 
 * State Machine:
 * - NO_IDENTITY: No stable embedding exists
 * - INSUFFICIENT: High variance detected
 * - ESTABLISHED: Stable within bounds
 * - DRIFT: Progressive deviation detected
 */
export function computeIdentityState(
  input: IdentityValidationInput,
  config: KernelConfig = DEFAULT_KERNEL_CONFIG
): IdentityStateResult {
  const reasons: string[] = [];
  
  // Gate 1: No reference data = NO_IDENTITY
  if (!input.reference_embeddings || input.reference_embeddings.length === 0) {
    return {
      entity_id: input.entity_id,
      state: 'NO_IDENTITY',
      variance_score: 1.0,
      coverage_percent: 0,
      reasons: ['NO_REFERENCE_DATA'],
    };
  }

  // Gate 2: Compute variance across reference embeddings
  const variance = computeVariance(input.reference_embeddings);
  const coverage = computeCoverage(input.reference_embeddings, input.current_embedding);

  // Gate 3: Coverage below minimum = INSUFFICIENT
  if (coverage < config.coverage_minimum_percent) {
    reasons.push(`COVERAGE_BELOW_MINIMUM: ${coverage}% < ${config.coverage_minimum_percent}%`);
    return {
      entity_id: input.entity_id,
      state: 'INSUFFICIENT',
      variance_score: variance,
      coverage_percent: coverage,
      reasons,
    };
  }

  // Gate 4: Variance above drift threshold = DRIFT
  if (variance > config.variance_threshold_drift) {
    reasons.push(`VARIANCE_EXCEEDS_DRIFT_THRESHOLD: ${variance} > ${config.variance_threshold_drift}`);
    return {
      entity_id: input.entity_id,
      state: 'DRIFT',
      variance_score: variance,
      coverage_percent: coverage,
      reasons,
    };
  }

  // Gate 5: Variance above established threshold = INSUFFICIENT
  if (variance > config.variance_threshold_established) {
    reasons.push(`VARIANCE_EXCEEDS_ESTABLISHED_THRESHOLD: ${variance} > ${config.variance_threshold_established}`);
    return {
      entity_id: input.entity_id,
      state: 'INSUFFICIENT',
      variance_score: variance,
      coverage_percent: coverage,
      reasons,
    };
  }

  // Gate 6: All conditions met = ESTABLISHED
  return {
    entity_id: input.entity_id,
    state: 'ESTABLISHED',
    variance_score: variance,
    coverage_percent: coverage,
    reasons: ['ALL_GATES_PASSED'],
  };
}

/**
 * Compute variance score across embeddings
 * Lower is better (more stable identity)
 */
function computeVariance(embeddings: { variance_score: number }[]): number {
  if (embeddings.length === 0) return 1.0;
  if (embeddings.length === 1) return embeddings[0].variance_score;

  // Mean variance across all embeddings
  const sum = embeddings.reduce((acc, e) => acc + e.variance_score, 0);
  const mean = sum / embeddings.length;

  // Compute standard deviation as additional variance factor
  const squaredDiffs = embeddings.map(e => Math.pow(e.variance_score - mean, 2));
  const avgSquaredDiff = squaredDiffs.reduce((a, b) => a + b, 0) / embeddings.length;
  const stdDev = Math.sqrt(avgSquaredDiff);

  // Combined variance: mean + std deviation contribution
  return Math.min(1.0, mean + stdDev * 0.5);
}

/**
 * Compute coverage percentage
 * Measures how well reference data covers identity space
 */
function computeCoverage(
  references: { coverage_percent: number }[],
  current: { coverage_percent: number }
): number {
  if (references.length === 0) return 0;

  // Average coverage from references
  const refCoverage = references.reduce((acc, r) => acc + r.coverage_percent, 0) / references.length;
  
  // Weight current embedding coverage
  const weightedCoverage = (refCoverage * 0.7) + (current.coverage_percent * 0.3);
  
  return Math.min(100, Math.max(0, weightedCoverage));
}

/**
 * Check if identity state allows task execution
 */
export function isIdentityStateValid(
  current: IdentityStateEnum,
  required: IdentityStateEnum
): boolean {
  const stateOrder: Record<IdentityStateEnum, number> = {
    'NO_IDENTITY': 0,
    'INSUFFICIENT': 1,
    'DRIFT': 2,
    'ESTABLISHED': 3,
  };

  return stateOrder[current] >= stateOrder[required];
}

/**
 * Get human-readable state description (for UI display only)
 */
export function getIdentityStateDescription(state: IdentityStateEnum): string {
  const descriptions: Record<IdentityStateEnum, string> = {
    'NO_IDENTITY': 'No stable embedding established',
    'INSUFFICIENT': 'High variance detected, additional reference required',
    'ESTABLISHED': 'Identity stable within bounds',
    'DRIFT': 'Progressive deviation detected, re-verification required',
  };
  return descriptions[state];
}
