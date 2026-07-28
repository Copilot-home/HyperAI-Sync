/**
 * ECVM Kernel Integration Tests - Kernel v0.1.3
 * END-TO-END TEST HARNESS · AUDITABLE
 * 
 * Tests the complete flow: Identity → Drift → Task Validation
 */

import { describe, it, expect } from 'vitest';
import {
  computeIdentityState,
  detectDrift,
  detectSystemicDrift,
  validateTask,
  IdentityValidationInput,
  IdentityEmbedding,
  TaskValidationInput,
  DEFAULT_KERNEL_CONFIG,
} from '@/lib/kernel';

describe('Kernel Integration', () => {
  // Test fixtures
  const createEmbedding = (
    variance: number,
    coverage: number
  ): IdentityEmbedding => ({
    entity_id: 'test-entity-id',
    identity_hash: 'hash-' + Math.random().toString(36),
    geometry_hash: 'geom-' + Math.random().toString(36),
    variance_score: variance,
    coverage_percent: coverage,
  });

  describe('Complete user flow: Upload → Generate', () => {
    it('blocks generation when no identity exists', () => {
      // Step 1: Check identity state (no reference)
      const identityInput: IdentityValidationInput = {
        entity_id: 'new-user',
        current_embedding: createEmbedding(0, 0),
        reference_embeddings: [],
      };
      const identityState = computeIdentityState(identityInput);
      expect(identityState.state).toBe('NO_IDENTITY');

      // Step 2: Attempt task validation
      const taskInput: TaskValidationInput = {
        task_id: 'task-1',
        entity_id: 'new-user',
        logic_id: 'image-gen-1',
        task_type: 'image',
        identity_state: identityState.state,
        required_identity_state: 'ESTABLISHED',
        logic_enabled: true,
      };
      const result = validateTask(taskInput);

      expect(result.verdict).toBe('REJECT');
      expect(result.reasons.some(r => r.includes('NO_IDENTITY'))).toBe(true);
    });

    it('allows generation when identity is established', () => {
      // Step 1: Establish identity with good reference data
      const identityInput: IdentityValidationInput = {
        entity_id: 'established-user',
        current_embedding: createEmbedding(0.05, 90),
        reference_embeddings: [
          createEmbedding(0.04, 88),
          createEmbedding(0.05, 85),
          createEmbedding(0.06, 90),
        ],
      };
      const identityState = computeIdentityState(identityInput);
      expect(identityState.state).toBe('ESTABLISHED');

      // Step 2: Validate task
      const taskInput: TaskValidationInput = {
        task_id: 'task-2',
        entity_id: 'established-user',
        logic_id: 'image-gen-1',
        task_type: 'image',
        identity_state: identityState.state,
        required_identity_state: 'ESTABLISHED',
        logic_enabled: true,
      };
      const result = validateTask(taskInput);

      expect(result.verdict).toBe('PASS');
    });

    it('halts generation when drift detected', () => {
      // Step 1: Identity goes into drift
      const identityInput: IdentityValidationInput = {
        entity_id: 'drifting-user',
        current_embedding: createEmbedding(0.5, 75),
        reference_embeddings: [createEmbedding(0.45, 80)],
      };
      const identityState = computeIdentityState(identityInput);
      expect(identityState.state).toBe('DRIFT');

      // Step 2: Detect drift explicitly
      const driftResult = detectDrift({
        entity_id: 'drifting-user',
        baseline_variance: 0.1,
        current_variance: identityState.variance_score,
        threshold: 0.15,
      });
      expect(driftResult.detected).toBe(true);
      expect(driftResult.drift_type).toBe('PER_NODE');

      // Step 3: Task validation HALTs
      const taskInput: TaskValidationInput = {
        task_id: 'task-3',
        entity_id: 'drifting-user',
        logic_id: 'image-gen-1',
        task_type: 'image',
        identity_state: identityState.state,
        required_identity_state: 'ESTABLISHED',
        logic_enabled: true,
      };
      const result = validateTask(taskInput);

      expect(result.verdict).toBe('HALT');
      expect(result.terminal).toBe(true);
    });
  });

  describe('Systemic drift detection flow', () => {
    it('detects systemic drift across multiple nodes', () => {
      const logic_id = 'problematic-logic-module';

      // Simulate multiple users with same logic experiencing drift
      const nodeResults = [
        { entity_id: 'user-1', variance: 0.4 },
        { entity_id: 'user-2', variance: 0.38 },
        { entity_id: 'user-3', variance: 0.42 },
        { entity_id: 'user-4', variance: 0.35 },
      ];

      // Each node detects drift
      const nodeDeltas = nodeResults.map(node => ({
        entity_id: node.entity_id,
        delta: node.variance - 0.1, // baseline was 0.1
      }));

      // Admin aggregates and detects systemic issue
      const systemicResult = detectSystemicDrift(nodeDeltas, logic_id);

      expect(systemicResult.detected).toBe(true);
      expect(systemicResult.drift_type).toBe('SYSTEMIC');
      expect(systemicResult.action_authority).toBe('ADMIN');
      expect(systemicResult.requires_action).toBe(true);
    });

    it('does not flag systemic when only 1-2 nodes affected', () => {
      const logic_id = 'mostly-stable-logic';

      const nodeDeltas = [
        { entity_id: 'user-1', delta: 0.35 },
        { entity_id: 'user-2', delta: 0.02 },
        { entity_id: 'user-3', delta: 0.01 },
        { entity_id: 'user-4', delta: 0.03 },
      ];

      const systemicResult = detectSystemicDrift(nodeDeltas, logic_id);

      expect(systemicResult.detected).toBe(false);
    });
  });

  describe('Gate sequence enforcement', () => {
    it('enforces gate 1 before gate 2 (logic before identity)', () => {
      // Even with good identity, disabled logic = REJECT
      const taskInput: TaskValidationInput = {
        task_id: 'task-gate-1',
        entity_id: 'good-user',
        logic_id: 'disabled-logic',
        task_type: 'image',
        identity_state: 'ESTABLISHED',
        required_identity_state: 'ESTABLISHED',
        logic_enabled: false, // Gate 1 fails
      };
      const result = validateTask(taskInput);

      expect(result.verdict).toBe('REJECT');
      expect(result.reasons).toContain('LOGIC_NOT_ENABLED');
    });

    it('enforces all gates must pass for PASS verdict', () => {
      const scenarios: { input: Partial<TaskValidationInput>; expectedVerdict: 'PASS' | 'REJECT' | 'HALT' }[] = [
        {
          input: { logic_enabled: true, identity_state: 'ESTABLISHED' },
          expectedVerdict: 'PASS',
        },
        {
          input: { logic_enabled: false, identity_state: 'ESTABLISHED' },
          expectedVerdict: 'REJECT',
        },
        {
          input: { logic_enabled: true, identity_state: 'INSUFFICIENT' },
          expectedVerdict: 'REJECT',
        },
        {
          input: { logic_enabled: true, identity_state: 'DRIFT' },
          expectedVerdict: 'HALT',
        },
        {
          input: { logic_enabled: true, identity_state: 'NO_IDENTITY' },
          expectedVerdict: 'REJECT',
        },
      ];

      for (const scenario of scenarios) {
        const taskInput: TaskValidationInput = {
          task_id: 'gate-test',
          entity_id: 'test-user',
          logic_id: 'test-logic',
          task_type: 'image',
          required_identity_state: 'ESTABLISHED',
          logic_enabled: true,
          identity_state: 'ESTABLISHED',
          ...scenario.input,
        };
        const result = validateTask(taskInput);
        expect(result.verdict).toBe(scenario.expectedVerdict);
      }
    });
  });

  describe('Fail-closed principle', () => {
    it('defaults to REJECT when state is ambiguous', () => {
      const taskInput: TaskValidationInput = {
        task_id: 'ambiguous-task',
        entity_id: 'test-user',
        logic_id: 'test-logic',
        task_type: 'image',
        identity_state: 'INSUFFICIENT',
        required_identity_state: 'ESTABLISHED',
        logic_enabled: true,
      };
      const result = validateTask(taskInput);

      // System does not guess or approximate
      expect(result.verdict).toBe('REJECT');
    });

    it('never returns intermediate states', () => {
      const taskInput: TaskValidationInput = {
        task_id: 'complete-task',
        entity_id: 'test-user',
        logic_id: 'test-logic',
        task_type: 'image',
        identity_state: 'ESTABLISHED',
        required_identity_state: 'ESTABLISHED',
        logic_enabled: true,
      };
      const result = validateTask(taskInput);

      // Verdict is always one of: PASS, REJECT, HALT
      expect(['PASS', 'REJECT', 'HALT']).toContain(result.verdict);
    });
  });
});
