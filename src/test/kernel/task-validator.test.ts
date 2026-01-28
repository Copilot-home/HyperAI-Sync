/**
 * ECVM Task Validator Tests - Kernel v0.1.3
 * TEST HARNESS · AUDITABLE · FAIL-CLOSED VERIFICATION
 */

import { describe, it, expect } from 'vitest';
import {
  validateTask,
  validateTaskBatch,
  isVerdictExecutable,
  isVerdictTerminal,
  TaskValidationInput,
} from '@/lib/kernel';

describe('Task Validator', () => {
  const createTaskInput = (
    overrides: Partial<TaskValidationInput> = {}
  ): TaskValidationInput => ({
    task_id: 'test-task-id',
    entity_id: 'test-entity-id',
    logic_id: 'test-logic-id',
    task_type: 'image',
    identity_state: 'ESTABLISHED',
    required_identity_state: 'ESTABLISHED',
    logic_enabled: true,
    ...overrides,
  });

  describe('validateTask', () => {
    it('returns PASS when all gates pass', () => {
      const input = createTaskInput();
      const result = validateTask(input);

      expect(result.verdict).toBe('PASS');
      expect(result.terminal).toBe(false);
      expect(result.reasons).toContain('ALL_GATES_PASSED');
    });

    it('returns REJECT when logic is not enabled', () => {
      const input = createTaskInput({ logic_enabled: false });
      const result = validateTask(input);

      expect(result.verdict).toBe('REJECT');
      expect(result.terminal).toBe(false);
      expect(result.reasons).toContain('LOGIC_NOT_ENABLED');
    });

    it('returns REJECT when identity state is insufficient', () => {
      const input = createTaskInput({
        identity_state: 'INSUFFICIENT',
        required_identity_state: 'ESTABLISHED',
      });
      const result = validateTask(input);

      expect(result.verdict).toBe('REJECT');
      expect(result.terminal).toBe(false);
      expect(result.reasons.some(r => r.includes('IDENTITY_STATE_INSUFFICIENT'))).toBe(true);
    });

    it('returns HALT when identity state is DRIFT (terminal)', () => {
      const input = createTaskInput({
        identity_state: 'DRIFT',
        required_identity_state: 'ESTABLISHED',
      });
      const result = validateTask(input);

      expect(result.verdict).toBe('HALT');
      expect(result.terminal).toBe(true);
    });

    it('returns REJECT for NO_IDENTITY when ESTABLISHED required', () => {
      const input = createTaskInput({
        identity_state: 'NO_IDENTITY',
        required_identity_state: 'ESTABLISHED',
      });
      const result = validateTask(input);

      expect(result.verdict).toBe('REJECT');
      expect(result.reasons.some(r => r.includes('NO_IDENTITY'))).toBe(true);
    });

    it('returns PASS when ESTABLISHED satisfies INSUFFICIENT requirement', () => {
      const input = createTaskInput({
        identity_state: 'ESTABLISHED',
        required_identity_state: 'INSUFFICIENT',
      });
      const result = validateTask(input);

      expect(result.verdict).toBe('PASS');
    });
  });

  describe('isVerdictExecutable', () => {
    it('PASS is executable', () => {
      expect(isVerdictExecutable('PASS')).toBe(true);
    });

    it('REJECT is not executable', () => {
      expect(isVerdictExecutable('REJECT')).toBe(false);
    });

    it('HALT is not executable', () => {
      expect(isVerdictExecutable('HALT')).toBe(false);
    });
  });

  describe('isVerdictTerminal', () => {
    it('HALT is terminal', () => {
      expect(isVerdictTerminal('HALT')).toBe(true);
    });

    it('PASS is not terminal', () => {
      expect(isVerdictTerminal('PASS')).toBe(false);
    });

    it('REJECT is not terminal', () => {
      expect(isVerdictTerminal('REJECT')).toBe(false);
    });
  });

  describe('validateTaskBatch', () => {
    it('validates all tasks when no HALT', () => {
      const inputs = [
        createTaskInput({ task_id: 'task-1' }),
        createTaskInput({ task_id: 'task-2' }),
        createTaskInput({ task_id: 'task-3' }),
      ];

      const results = validateTaskBatch(inputs);

      expect(results).toHaveLength(3);
      expect(results.every(r => r.verdict === 'PASS')).toBe(true);
    });

    it('stops on first HALT (fail-closed)', () => {
      const inputs = [
        createTaskInput({ task_id: 'task-1' }),
        createTaskInput({
          task_id: 'task-2',
          identity_state: 'DRIFT',
        }),
        createTaskInput({ task_id: 'task-3' }),
      ];

      const results = validateTaskBatch(inputs);

      // Should stop after task-2 (HALT)
      expect(results).toHaveLength(2);
      expect(results[0].verdict).toBe('PASS');
      expect(results[1].verdict).toBe('HALT');
      expect(results[1].terminal).toBe(true);
    });

    it('continues through REJECT (non-terminal)', () => {
      const inputs = [
        createTaskInput({ task_id: 'task-1' }),
        createTaskInput({
          task_id: 'task-2',
          logic_enabled: false,
        }),
        createTaskInput({ task_id: 'task-3' }),
      ];

      const results = validateTaskBatch(inputs);

      expect(results).toHaveLength(3);
      expect(results[0].verdict).toBe('PASS');
      expect(results[1].verdict).toBe('REJECT');
      expect(results[2].verdict).toBe('PASS');
    });
  });

  describe('Kernel law enforcement', () => {
    it('verdict is immutable once issued', () => {
      const input = createTaskInput();
      const result = validateTask(input);

      // Attempting to modify verdict should not be possible
      // (TypeScript readonly enforcement in production)
      expect(result.verdict).toBe('PASS');
      
      // Re-validating same input produces same result
      const result2 = validateTask(input);
      expect(result2.verdict).toBe(result.verdict);
    });

    it('no retry after REJECT', () => {
      const input = createTaskInput({ logic_enabled: false });
      const result = validateTask(input);

      expect(result.verdict).toBe('REJECT');
      
      // Same input without change still fails
      const result2 = validateTask(input);
      expect(result2.verdict).toBe('REJECT');
    });

    it('no recovery after HALT', () => {
      const input = createTaskInput({ identity_state: 'DRIFT' });
      const result = validateTask(input);

      expect(result.verdict).toBe('HALT');
      expect(result.terminal).toBe(true);
      
      // Terminal means no retry possible
      // UI should show STOP screen
    });
  });
});
