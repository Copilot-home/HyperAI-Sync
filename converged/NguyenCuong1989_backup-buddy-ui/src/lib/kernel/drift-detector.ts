/**
 * ECVM Drift Detector - Kernel v0.1.3
 * LOCKED · LAW-COMPLIANT · FAIL-CLOSED
 * 
 * Detects and classifies drift:
 * - PER_NODE: Single user node, insufficient personal data
 * - SYSTEMIC: Multiple nodes, LogicModule mismatch
 * 
 * Authority matrix enforced at detection time.
 */

import {
  DriftType,
  DriftDetectionInput,
  DriftDetectionResult,
  KernelConfig,
  DEFAULT_KERNEL_CONFIG,
} from './types';

/**
 * Detect drift from variance delta
 */
export function detectDrift(
  input: DriftDetectionInput,
  config: KernelConfig = DEFAULT_KERNEL_CONFIG
): DriftDetectionResult {
  const delta = Math.abs(input.current_variance - input.baseline_variance);
  const detected = delta > input.threshold;

  if (!detected) {
    return {
      detected: false,
      drift_type: null,
      severity: 0,
      delta,
      requires_action: false,
      action_authority: null,
    };
  }

  // Classify drift type
  const driftType = classifyDriftType(input);
  
  // Compute severity (0-1 scale)
  const severity = computeDriftSeverity(delta, config.drift_severity_threshold);
  
  // Determine authority for resolution
  const authority = driftType === 'PER_NODE' ? 'USER' : 'ADMIN';

  return {
    detected: true,
    drift_type: driftType,
    severity,
    delta,
    requires_action: severity >= config.drift_severity_threshold,
    action_authority: authority,
  };
}

/**
 * Classify drift as PER_NODE or SYSTEMIC
 * 
 * Rules (LOCKED):
 * - entity_id present, no logic_id → PER_NODE
 * - logic_id present → SYSTEMIC
 * - Both present → SYSTEMIC (logic issue affects node)
 */
function classifyDriftType(input: DriftDetectionInput): DriftType {
  if (input.logic_id) {
    return 'SYSTEMIC';
  }
  return 'PER_NODE';
}

/**
 * Compute drift severity on 0-1 scale
 */
function computeDriftSeverity(delta: number, threshold: number): number {
  if (delta <= 0) return 0;
  // Severity scales with how much delta exceeds threshold
  const ratio = delta / threshold;
  return Math.min(1.0, ratio);
}

/**
 * Aggregate drift events to detect systemic pattern
 */
export function detectSystemicDrift(
  nodeDeltas: { entity_id: string; delta: number }[],
  logic_id: string,
  config: KernelConfig = DEFAULT_KERNEL_CONFIG
): DriftDetectionResult {
  // Count nodes exceeding threshold
  const affectedNodes = nodeDeltas.filter(
    n => n.delta > config.drift_severity_threshold
  );

  if (affectedNodes.length < config.systemic_drift_node_threshold) {
    // Not enough nodes affected → not systemic
    return {
      detected: false,
      drift_type: null,
      severity: 0,
      delta: 0,
      requires_action: false,
      action_authority: null,
    };
  }

  // Systemic drift confirmed
  const avgDelta = affectedNodes.reduce((a, n) => a + n.delta, 0) / affectedNodes.length;
  const severity = computeDriftSeverity(avgDelta, config.drift_severity_threshold);

  return {
    detected: true,
    drift_type: 'SYSTEMIC',
    severity,
    delta: avgDelta,
    requires_action: true,
    action_authority: 'ADMIN',
  };
}

/**
 * Get resolution action for drift type
 */
export function getDriftResolution(driftType: DriftType): {
  action: string;
  authority: 'USER' | 'ADMIN';
  description: string;
} {
  if (driftType === 'PER_NODE') {
    return {
      action: 'REQUEST_ADDITIONAL_REFERENCE',
      authority: 'USER',
      description: 'Upload additional reference data to restore identity stability',
    };
  }
  
  return {
    action: 'DISABLE_LOGIC_MODULE',
    authority: 'ADMIN',
    description: 'Disable or revise the affected LogicModule',
  };
}
