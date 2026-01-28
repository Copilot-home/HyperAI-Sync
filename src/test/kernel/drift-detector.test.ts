/**
 * ECVM Drift Detector Tests - Kernel v0.1.3
 * TEST HARNESS · AUDITABLE · FAIL-CLOSED VERIFICATION
 */

import { describe, it, expect } from 'vitest';
import {
  detectDrift,
  detectSystemicDrift,
  getDriftResolution,
  DEFAULT_KERNEL_CONFIG,
} from '@/lib/kernel';

describe('Drift Detector', () => {
  describe('detectDrift', () => {
    it('returns no drift when delta is below threshold', () => {
      const result = detectDrift({
        entity_id: 'test-entity',
        baseline_variance: 0.1,
        current_variance: 0.12,
        threshold: 0.1,
      });

      expect(result.detected).toBe(false);
      expect(result.drift_type).toBeNull();
      expect(result.requires_action).toBe(false);
    });

    it('detects PER_NODE drift when entity_id present and no logic_id', () => {
      const result = detectDrift({
        entity_id: 'test-entity',
        baseline_variance: 0.1,
        current_variance: 0.35,
        threshold: 0.1,
      });

      expect(result.detected).toBe(true);
      expect(result.drift_type).toBe('PER_NODE');
      expect(result.action_authority).toBe('USER');
    });

    it('detects SYSTEMIC drift when logic_id present', () => {
      const result = detectDrift({
        entity_id: 'test-entity',
        logic_id: 'test-logic',
        baseline_variance: 0.1,
        current_variance: 0.35,
        threshold: 0.1,
      });

      expect(result.detected).toBe(true);
      expect(result.drift_type).toBe('SYSTEMIC');
      expect(result.action_authority).toBe('ADMIN');
    });

    it('classifies as SYSTEMIC when both entity_id and logic_id present', () => {
      // Per spec: Both present → SYSTEMIC (logic issue affects node)
      const result = detectDrift({
        entity_id: 'test-entity',
        logic_id: 'test-logic',
        baseline_variance: 0.1,
        current_variance: 0.4,
        threshold: 0.1,
      });

      expect(result.drift_type).toBe('SYSTEMIC');
    });

    it('computes severity based on delta magnitude', () => {
      const lowSeverity = detectDrift({
        entity_id: 'test-entity',
        baseline_variance: 0.1,
        current_variance: 0.25,
        threshold: 0.1,
      });

      const highSeverity = detectDrift({
        entity_id: 'test-entity',
        baseline_variance: 0.1,
        current_variance: 0.5,
        threshold: 0.1,
      });

      expect(highSeverity.severity).toBeGreaterThan(lowSeverity.severity);
    });

    it('requires action when severity exceeds threshold', () => {
      const result = detectDrift(
        {
          entity_id: 'test-entity',
          baseline_variance: 0.1,
          current_variance: 0.5,
          threshold: 0.1,
        },
        DEFAULT_KERNEL_CONFIG
      );

      expect(result.requires_action).toBe(true);
    });
  });

  describe('detectSystemicDrift', () => {
    it('does not detect systemic drift when few nodes affected', () => {
      const nodeDeltas = [
        { entity_id: 'entity-1', delta: 0.3 },
        { entity_id: 'entity-2', delta: 0.05 },
        { entity_id: 'entity-3', delta: 0.02 },
      ];

      const result = detectSystemicDrift(nodeDeltas, 'test-logic');

      expect(result.detected).toBe(false);
      expect(result.drift_type).toBeNull();
    });

    it('detects systemic drift when threshold nodes affected', () => {
      const nodeDeltas = [
        { entity_id: 'entity-1', delta: 0.35 },
        { entity_id: 'entity-2', delta: 0.4 },
        { entity_id: 'entity-3', delta: 0.38 },
        { entity_id: 'entity-4', delta: 0.42 },
      ];

      const result = detectSystemicDrift(nodeDeltas, 'test-logic');

      expect(result.detected).toBe(true);
      expect(result.drift_type).toBe('SYSTEMIC');
      expect(result.action_authority).toBe('ADMIN');
      expect(result.requires_action).toBe(true);
    });

    it('computes average delta across affected nodes', () => {
      const nodeDeltas = [
        { entity_id: 'entity-1', delta: 0.3 },
        { entity_id: 'entity-2', delta: 0.4 },
        { entity_id: 'entity-3', delta: 0.5 },
      ];

      const result = detectSystemicDrift(nodeDeltas, 'test-logic');

      expect(result.delta).toBeCloseTo(0.4, 1);
    });

    it('respects custom systemic threshold', () => {
      const nodeDeltas = [
        { entity_id: 'entity-1', delta: 0.35 },
        { entity_id: 'entity-2', delta: 0.4 },
      ];

      const customConfig = {
        ...DEFAULT_KERNEL_CONFIG,
        systemic_drift_node_threshold: 2,
      };

      const result = detectSystemicDrift(nodeDeltas, 'test-logic', customConfig);

      expect(result.detected).toBe(true);
    });
  });

  describe('getDriftResolution', () => {
    it('returns USER authority for PER_NODE drift', () => {
      const resolution = getDriftResolution('PER_NODE');

      expect(resolution.authority).toBe('USER');
      expect(resolution.action).toBe('REQUEST_ADDITIONAL_REFERENCE');
    });

    it('returns ADMIN authority for SYSTEMIC drift', () => {
      const resolution = getDriftResolution('SYSTEMIC');

      expect(resolution.authority).toBe('ADMIN');
      expect(resolution.action).toBe('DISABLE_LOGIC_MODULE');
    });
  });

  describe('Authority matrix enforcement', () => {
    it('PER_NODE drift can only be resolved by user node', () => {
      const result = detectDrift({
        entity_id: 'test-entity',
        baseline_variance: 0.1,
        current_variance: 0.4,
        threshold: 0.1,
      });

      expect(result.drift_type).toBe('PER_NODE');
      expect(result.action_authority).toBe('USER');

      const resolution = getDriftResolution('PER_NODE');
      expect(resolution.authority).toBe('USER');
    });

    it('SYSTEMIC drift can only be resolved by admin node', () => {
      const result = detectDrift({
        logic_id: 'test-logic',
        baseline_variance: 0.1,
        current_variance: 0.4,
        threshold: 0.1,
      });

      expect(result.drift_type).toBe('SYSTEMIC');
      expect(result.action_authority).toBe('ADMIN');

      const resolution = getDriftResolution('SYSTEMIC');
      expect(resolution.authority).toBe('ADMIN');
    });
  });
});
