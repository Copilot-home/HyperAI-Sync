/**
 * ECVM Kernel Edge Function Tests
 * Test harness for _shared/kernel.ts in Deno runtime
 * Kernel v0.1.3 · FAIL-CLOSED VERIFICATION
 */

import "https://deno.land/std@0.224.0/dotenv/load.ts";
import { assertEquals, assertExists } from "https://deno.land/std@0.224.0/assert/mod.ts";
import {
  validateTask,
  isIdentityStateValid,
  isVerdictExecutable,
  isVerdictTerminal,
  TaskValidationInput,
  IdentityStateEnum,
  DEFAULT_KERNEL_CONFIG,
} from "./kernel.ts";

// ============================================
// IDENTITY STATE VALIDATION TESTS
// ============================================

Deno.test("isIdentityStateValid: ESTABLISHED meets ESTABLISHED requirement", () => {
  const result = isIdentityStateValid("ESTABLISHED", "ESTABLISHED");
  assertEquals(result, true);
});

Deno.test("isIdentityStateValid: ESTABLISHED meets INSUFFICIENT requirement", () => {
  const result = isIdentityStateValid("ESTABLISHED", "INSUFFICIENT");
  assertEquals(result, true);
});

Deno.test("isIdentityStateValid: ESTABLISHED meets NO_IDENTITY requirement", () => {
  const result = isIdentityStateValid("ESTABLISHED", "NO_IDENTITY");
  assertEquals(result, true);
});

Deno.test("isIdentityStateValid: INSUFFICIENT fails ESTABLISHED requirement", () => {
  const result = isIdentityStateValid("INSUFFICIENT", "ESTABLISHED");
  assertEquals(result, false);
});

Deno.test("isIdentityStateValid: NO_IDENTITY fails ESTABLISHED requirement", () => {
  const result = isIdentityStateValid("NO_IDENTITY", "ESTABLISHED");
  assertEquals(result, false);
});

Deno.test("isIdentityStateValid: DRIFT always invalid (terminal state)", () => {
  assertEquals(isIdentityStateValid("DRIFT", "NO_IDENTITY"), false);
  assertEquals(isIdentityStateValid("DRIFT", "INSUFFICIENT"), false);
  assertEquals(isIdentityStateValid("DRIFT", "ESTABLISHED"), false);
});

// ============================================
// TASK VALIDATION TESTS
// ============================================

function createTaskInput(overrides: Partial<TaskValidationInput> = {}): TaskValidationInput {
  return {
    task_id: "test-task-001",
    entity_id: "test-entity-001",
    logic_id: "test-logic-001",
    task_type: "image",
    identity_state: "ESTABLISHED",
    required_identity_state: "ESTABLISHED",
    logic_enabled: true,
    ...overrides,
  };
}

Deno.test("validateTask: PASS when all gates pass", () => {
  const input = createTaskInput();
  const result = validateTask(input);

  assertEquals(result.verdict, "PASS");
  assertEquals(result.terminal, false);
  assertEquals(result.reasons.includes("ALL_GATES_PASSED"), true);
});

Deno.test("validateTask: REJECT when logic disabled", () => {
  const input = createTaskInput({ logic_enabled: false });
  const result = validateTask(input);

  assertEquals(result.verdict, "REJECT");
  assertEquals(result.terminal, false);
  assertEquals(result.reasons.includes("LOGIC_NOT_ENABLED"), true);
});

Deno.test("validateTask: REJECT when identity insufficient", () => {
  const input = createTaskInput({
    identity_state: "INSUFFICIENT",
    required_identity_state: "ESTABLISHED",
  });
  const result = validateTask(input);

  assertEquals(result.verdict, "REJECT");
  assertEquals(result.terminal, false);
  assertEquals(result.reasons.some((r) => r.includes("IDENTITY_STATE_INSUFFICIENT")), true);
});

Deno.test("validateTask: HALT when identity is DRIFT (terminal)", () => {
  const input = createTaskInput({
    identity_state: "DRIFT",
    required_identity_state: "ESTABLISHED",
  });
  const result = validateTask(input);

  assertEquals(result.verdict, "HALT");
  assertEquals(result.terminal, true);
});

Deno.test("validateTask: gate order - logic check before identity check", () => {
  // Both logic disabled AND identity in DRIFT
  // Logic gate should fail first (order matters for debugging)
  const input = createTaskInput({
    logic_enabled: false,
    identity_state: "DRIFT",
  });
  const result = validateTask(input);

  assertEquals(result.verdict, "REJECT");
  assertEquals(result.reasons.includes("LOGIC_NOT_ENABLED"), true);
});

// ============================================
// VERDICT HELPER TESTS
// ============================================

Deno.test("isVerdictExecutable: only PASS is executable", () => {
  assertEquals(isVerdictExecutable("PASS"), true);
  assertEquals(isVerdictExecutable("REJECT"), false);
  assertEquals(isVerdictExecutable("HALT"), false);
});

Deno.test("isVerdictTerminal: only HALT is terminal", () => {
  assertEquals(isVerdictTerminal("HALT"), true);
  assertEquals(isVerdictTerminal("PASS"), false);
  assertEquals(isVerdictTerminal("REJECT"), false);
});

// ============================================
// CONFIG TESTS
// ============================================

Deno.test("DEFAULT_KERNEL_CONFIG: has required threshold values", () => {
  assertExists(DEFAULT_KERNEL_CONFIG.variance_threshold_established);
  assertExists(DEFAULT_KERNEL_CONFIG.variance_threshold_drift);
  assertExists(DEFAULT_KERNEL_CONFIG.coverage_minimum_percent);
  assertExists(DEFAULT_KERNEL_CONFIG.drift_severity_threshold);
  assertExists(DEFAULT_KERNEL_CONFIG.systemic_drift_node_threshold);

  assertEquals(DEFAULT_KERNEL_CONFIG.variance_threshold_established, 0.15);
  assertEquals(DEFAULT_KERNEL_CONFIG.variance_threshold_drift, 0.35);
  assertEquals(DEFAULT_KERNEL_CONFIG.coverage_minimum_percent, 70);
});

// ============================================
// EDGE CASES
// ============================================

Deno.test("validateTask: NO_IDENTITY with NO_IDENTITY requirement passes", () => {
  const input = createTaskInput({
    identity_state: "NO_IDENTITY",
    required_identity_state: "NO_IDENTITY",
  });
  const result = validateTask(input);

  assertEquals(result.verdict, "PASS");
});

Deno.test("validateTask: result includes task_id", () => {
  const input = createTaskInput({ task_id: "unique-task-123" });
  const result = validateTask(input);

  assertEquals(result.task_id, "unique-task-123");
});

Deno.test("validateTask: all task types work with valid state", () => {
  const taskTypes: Array<"image_static" | "image" | "video" | "validation"> = [
    "image_static",
    "image",
    "video",
    "validation",
  ];

  for (const taskType of taskTypes) {
    const input = createTaskInput({ task_type: taskType });
    const result = validateTask(input);
    assertEquals(result.verdict, "PASS", `Failed for task_type: ${taskType}`);
  }
});
