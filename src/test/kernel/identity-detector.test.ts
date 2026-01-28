/**
 * ECVM Identity Detector Tests - Kernel v0.1.3
 * TEST HARNESS · AUDITABLE · FAIL-CLOSED VERIFICATION
 */

import { describe, it, expect } from 'vitest';
import {
  computeIdentityState,
  isIdentityStateValid,
  IdentityValidationInput,
  IdentityEmbedding,
  DEFAULT_KERNEL_CONFIG,
} from '@/lib/kernel';

describe('Identity State Detector', () => {
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

  describe('NO_IDENTITY state', () => {
    it('returns NO_IDENTITY when no reference embeddings exist', () => {
      const input: IdentityValidationInput = {
        entity_id: 'test-entity',
        current_embedding: createEmbedding(0.5, 50),
        reference_embeddings: [],
      };

      const result = computeIdentityState(input);

      expect(result.state).toBe('NO_IDENTITY');
      expect(result.variance_score).toBe(1.0);
      expect(result.coverage_percent).toBe(0);
      expect(result.reasons).toContain('NO_REFERENCE_DATA');
    });

    it('returns NO_IDENTITY when reference_embeddings is undefined', () => {
      const input: IdentityValidationInput = {
        entity_id: 'test-entity',
        current_embedding: createEmbedding(0.5, 50),
        reference_embeddings: undefined as unknown as IdentityEmbedding[],
      };

      const result = computeIdentityState(input);

      expect(result.state).toBe('NO_IDENTITY');
    });
  });

  describe('INSUFFICIENT state', () => {
    it('returns INSUFFICIENT when coverage is below minimum', () => {
      const input: IdentityValidationInput = {
        entity_id: 'test-entity',
        current_embedding: createEmbedding(0.1, 50),
        reference_embeddings: [
          createEmbedding(0.1, 40),
          createEmbedding(0.1, 45),
        ],
      };

      const result = computeIdentityState(input);

      expect(result.state).toBe('INSUFFICIENT');
      expect(result.reasons.some(r => r.includes('COVERAGE_BELOW_MINIMUM'))).toBe(true);
    });

    it('returns INSUFFICIENT when variance exceeds established threshold', () => {
      const input: IdentityValidationInput = {
        entity_id: 'test-entity',
        current_embedding: createEmbedding(0.2, 80),
        reference_embeddings: [
          createEmbedding(0.2, 85),
          createEmbedding(0.25, 80),
        ],
      };

      const result = computeIdentityState(input);

      expect(result.state).toBe('INSUFFICIENT');
      expect(result.reasons.some(r => r.includes('VARIANCE_EXCEEDS'))).toBe(true);
    });
  });

  describe('DRIFT state', () => {
    it('returns DRIFT when variance exceeds drift threshold', () => {
      const input: IdentityValidationInput = {
        entity_id: 'test-entity',
        current_embedding: createEmbedding(0.4, 80),
        reference_embeddings: [
          createEmbedding(0.4, 85),
          createEmbedding(0.45, 80),
        ],
      };

      const result = computeIdentityState(input);

      expect(result.state).toBe('DRIFT');
      expect(result.reasons.some(r => r.includes('DRIFT_THRESHOLD'))).toBe(true);
    });

    it('DRIFT is not FAIL - it indicates long-term data insufficiency', () => {
      const input: IdentityValidationInput = {
        entity_id: 'test-entity',
        current_embedding: createEmbedding(0.5, 75),
        reference_embeddings: [createEmbedding(0.5, 80)],
      };

      const result = computeIdentityState(input);

      // DRIFT should have actionable reasons, not failure reasons
      expect(result.state).toBe('DRIFT');
      expect(result.variance_score).toBeGreaterThan(0);
      expect(result.coverage_percent).toBeGreaterThan(0);
    });
  });

  describe('ESTABLISHED state', () => {
    it('returns ESTABLISHED when all conditions are met', () => {
      const input: IdentityValidationInput = {
        entity_id: 'test-entity',
        current_embedding: createEmbedding(0.05, 90),
        reference_embeddings: [
          createEmbedding(0.05, 85),
          createEmbedding(0.06, 88),
          createEmbedding(0.04, 90),
        ],
      };

      const result = computeIdentityState(input);

      expect(result.state).toBe('ESTABLISHED');
      expect(result.variance_score).toBeLessThan(DEFAULT_KERNEL_CONFIG.variance_threshold_established);
      expect(result.coverage_percent).toBeGreaterThanOrEqual(DEFAULT_KERNEL_CONFIG.coverage_minimum_percent);
      expect(result.reasons).toContain('ALL_GATES_PASSED');
    });
  });

  describe('isIdentityStateValid', () => {
    it('ESTABLISHED satisfies ESTABLISHED requirement', () => {
      expect(isIdentityStateValid('ESTABLISHED', 'ESTABLISHED')).toBe(true);
    });

    it('ESTABLISHED satisfies INSUFFICIENT requirement', () => {
      expect(isIdentityStateValid('ESTABLISHED', 'INSUFFICIENT')).toBe(true);
    });

    it('INSUFFICIENT does not satisfy ESTABLISHED requirement', () => {
      expect(isIdentityStateValid('INSUFFICIENT', 'ESTABLISHED')).toBe(false);
    });

    it('NO_IDENTITY does not satisfy any requirement except NO_IDENTITY', () => {
      expect(isIdentityStateValid('NO_IDENTITY', 'NO_IDENTITY')).toBe(true);
      expect(isIdentityStateValid('NO_IDENTITY', 'INSUFFICIENT')).toBe(false);
      expect(isIdentityStateValid('NO_IDENTITY', 'ESTABLISHED')).toBe(false);
    });

    it('DRIFT does not satisfy ESTABLISHED requirement', () => {
      expect(isIdentityStateValid('DRIFT', 'ESTABLISHED')).toBe(false);
    });
  });

  describe('Custom kernel config', () => {
    it('respects custom variance thresholds', () => {
      const strictConfig = {
        ...DEFAULT_KERNEL_CONFIG,
        variance_threshold_established: 0.05,
        variance_threshold_drift: 0.1,
      };

      const input: IdentityValidationInput = {
        entity_id: 'test-entity',
        current_embedding: createEmbedding(0.08, 90),
        reference_embeddings: [createEmbedding(0.08, 85)],
      };

      // Would be ESTABLISHED with default config, but INSUFFICIENT with strict
      const result = computeIdentityState(input, strictConfig);
      expect(result.state).toBe('INSUFFICIENT');
    });

    it('respects custom coverage minimum', () => {
      const strictConfig = {
        ...DEFAULT_KERNEL_CONFIG,
        coverage_minimum_percent: 90,
      };

      const input: IdentityValidationInput = {
        entity_id: 'test-entity',
        current_embedding: createEmbedding(0.05, 85),
        reference_embeddings: [createEmbedding(0.05, 80)],
      };

      const result = computeIdentityState(input, strictConfig);
      expect(result.state).toBe('INSUFFICIENT');
    });
  });
});
