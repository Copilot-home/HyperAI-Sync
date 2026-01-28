import { useQuery } from "@tanstack/react-query";
import { TaskExecutionLog } from "@/types/ecvm";

// Mock endpoint - in production this would query task_execution_log table
async function fetchTaskHistory(): Promise<TaskExecutionLog[]> {
  await new Promise(resolve => setTimeout(resolve, 600));
  
  return [
    {
      id: "log_001",
      task_id: "task_a7b3c9",
      entity_id: "ent_7f3a9c2d",
      task_type: "image",
      verdict: "PASS",
      logic_applied: ["lg_face_detect", "lg_age_verify"],
      executed_at: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
      execution_time_ms: 1247,
      metadata: {},
    },
    {
      id: "log_002",
      task_id: "task_b8c4d0",
      entity_id: "ent_7f3a9c2d",
      task_type: "video",
      verdict: "HALT",
      logic_applied: ["lg_motion_track", "lg_liveness"],
      executed_at: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
      execution_time_ms: 3892,
      metadata: { halt_reason: "motion_threshold_exceeded" },
    },
    {
      id: "log_003",
      task_id: "task_c9d5e1",
      entity_id: "ent_7f3a9c2d",
      task_type: "image_static",
      verdict: "REJECT",
      logic_applied: ["lg_face_detect", "lg_doc_match"],
      executed_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
      execution_time_ms: 892,
      metadata: { reject_code: "FACE_MISMATCH" },
    },
    {
      id: "log_004",
      task_id: "task_d0e6f2",
      entity_id: "ent_7f3a9c2d",
      task_type: "image",
      verdict: "PASS",
      logic_applied: ["lg_face_detect", "lg_age_verify", "lg_liveness"],
      executed_at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
      execution_time_ms: 2103,
      metadata: {},
    },
  ];
}

export function useTaskHistory() {
  return useQuery({
    queryKey: ["task-history"],
    queryFn: fetchTaskHistory,
    staleTime: 30000,
    refetchOnWindowFocus: false,
  });
}
