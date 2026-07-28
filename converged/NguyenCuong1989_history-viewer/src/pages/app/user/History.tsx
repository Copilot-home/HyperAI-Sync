import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Shield } from "lucide-react";

// Read-only execution log type
interface TaskExecutionLog {
  task_id: string;
  logic_id: string;
  verdict: "PASS" | "REJECT" | "HALT";
  executed_at: string;
}

// Mock read-only data source - in production, this would be fetched once
const taskExecutionLog: TaskExecutionLog[] = [
  { task_id: "TASK-001", logic_id: "LGC-AUTH-001", verdict: "PASS", executed_at: "2026-01-28T09:15:32Z" },
  { task_id: "TASK-002", logic_id: "LGC-DEPLOY-003", verdict: "REJECT", executed_at: "2026-01-28T09:14:21Z" },
  { task_id: "TASK-003", logic_id: "LGC-VALIDATE-007", verdict: "HALT", executed_at: "2026-01-28T09:12:45Z" },
  { task_id: "TASK-004", logic_id: "LGC-AUTH-001", verdict: "PASS", executed_at: "2026-01-28T08:55:10Z" },
  { task_id: "TASK-005", logic_id: "LGC-DEPLOY-002", verdict: "PASS", executed_at: "2026-01-28T08:42:33Z" },
  { task_id: "TASK-006", logic_id: "LGC-VALIDATE-004", verdict: "REJECT", executed_at: "2026-01-28T08:30:18Z" },
  { task_id: "TASK-007", logic_id: "LGC-SYNC-001", verdict: "HALT", executed_at: "2026-01-27T23:59:59Z" },
  { task_id: "TASK-008", logic_id: "LGC-AUTH-002", verdict: "PASS", executed_at: "2026-01-27T22:15:44Z" },
];

const formatTimestamp = (iso: string): string => {
  const date = new Date(iso);
  return date.toLocaleString("en-US", {
    year: "numeric",
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  });
};

const VerdictBadge = ({ verdict }: { verdict: TaskExecutionLog["verdict"] }) => {
  const variantMap = {
    PASS: "pass",
    REJECT: "reject",
    HALT: "halt",
  } as const;

  return (
    <Badge variant={variantMap[verdict]} className="font-mono text-xs">
      {verdict}
      {verdict === "HALT" && <span className="ml-1 opacity-60">•</span>}
    </Badge>
  );
};

const History = () => {
  // Read-only render - no state mutations, no side effects
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center gap-3">
            <Shield className="h-5 w-5 text-muted-foreground" />
            <div>
              <h1 className="text-lg font-semibold text-foreground font-mono">
                Execution History
              </h1>
              <p className="text-xs text-muted-foreground">
                ECVM-CS-1.0 • Read-Only Audit Surface
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Audit Log Table */}
      <main className="container mx-auto px-6 py-8">
        <div className="rounded-lg border border-border bg-card overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow className="hover:bg-transparent">
                <TableHead className="font-mono text-xs uppercase tracking-wider text-muted-foreground">
                  Task ID
                </TableHead>
                <TableHead className="font-mono text-xs uppercase tracking-wider text-muted-foreground">
                  Logic ID
                </TableHead>
                <TableHead className="font-mono text-xs uppercase tracking-wider text-muted-foreground">
                  Verdict
                </TableHead>
                <TableHead className="font-mono text-xs uppercase tracking-wider text-muted-foreground">
                  Executed At
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {taskExecutionLog.map((log) => (
                <TableRow
                  key={`${log.task_id}-${log.executed_at}`}
                  className="hover:bg-muted/30"
                >
                  <TableCell className="font-mono text-sm text-foreground">
                    {log.task_id}
                  </TableCell>
                  <TableCell className="font-mono text-sm text-muted-foreground">
                    {log.logic_id}
                  </TableCell>
                  <TableCell>
                    <VerdictBadge verdict={log.verdict} />
                  </TableCell>
                  <TableCell className="font-mono text-sm text-muted-foreground tabular-nums">
                    {formatTimestamp(log.executed_at)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        {/* Footer disclaimer */}
        <p className="mt-4 text-center text-xs text-muted-foreground">
          This view is read-only. No modifications permitted.
        </p>
      </main>
    </div>
  );
};

export default History;
