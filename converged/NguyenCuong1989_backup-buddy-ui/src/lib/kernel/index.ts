/**
 * ECVM Kernel - v0.1.3
 * LOCKED · LAW-COMPLIANT · FAIL-CLOSED
 * 
 * Monolithic Kernel Entry Point
 * Exports all kernel functions and types for testing and integration.
 */

// Types
export * from './types';

// Identity Detection
export {
  computeIdentityState,
  isIdentityStateValid,
  getIdentityStateDescription,
} from './identity-detector';

// Drift Detection
export {
  detectDrift,
  detectSystemicDrift,
  getDriftResolution,
} from './drift-detector';

// Task Validation
export {
  validateTask,
  validateTaskBatch,
  isVerdictExecutable,
  isVerdictTerminal,
  getVerdictDescription,
} from './task-validator';
