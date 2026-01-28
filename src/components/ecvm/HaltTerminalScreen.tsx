import { Shield, XOctagon } from "lucide-react";
import { DisableReason } from "@/types/ecvm";
import { cn } from "@/lib/utils";

interface HaltTerminalScreenProps {
  reason: DisableReason;
  taskId?: string;
  className?: string;
}

/**
 * ECVM Terminal Screen for HALT verdict
 * Per ECVM-CS-1.0: HALT = terminal, no retry allowed
 * This component renders when a task receives HALT verdict
 */
export function HaltTerminalScreen({ reason, taskId, className }: HaltTerminalScreenProps) {
  return (
    <div className={cn(
      "min-h-[60vh] flex items-center justify-center",
      className
    )}>
      <div className="max-w-md w-full mx-auto text-center space-y-6">
        {/* Terminal Icon */}
        <div className="flex justify-center">
          <div className="p-6 rounded-full bg-status-halt-bg border-2 border-status-halt/30">
            <XOctagon className="h-16 w-16 text-status-halt" />
          </div>
        </div>

        {/* Title */}
        <div>
          <h1 className="text-2xl font-mono font-bold text-status-halt-foreground">
            SYSTEM HALT
          </h1>
          <p className="text-sm text-muted-foreground mt-2 font-mono">
            Verdict: HALT (Terminal)
          </p>
        </div>

        {/* Reason Panel */}
        <div className="ecvm-reason-panel text-left">
          <div className="flex items-center gap-2 mb-3">
            <Shield className="h-4 w-4 text-disabled-foreground" />
            <span className="text-xs font-mono uppercase tracking-wider text-disabled-foreground">
              Halt Reason
            </span>
          </div>
          <div className="space-y-2">
            <div className="text-sm font-medium text-foreground/80">
              [{reason.code}] {reason.message}
            </div>
            <div className="text-xs text-disabled-foreground font-mono">
              {reason.technical_detail}
            </div>
          </div>
        </div>

        {/* Task ID if available */}
        {taskId && (
          <div className="text-xs font-mono text-muted-foreground">
            task_id: {taskId}
          </div>
        )}

        {/* ECVM Notice - No Retry */}
        <div className="pt-4 border-t border-border">
          <p className="text-xs text-muted-foreground">
            Per ECVM-CS-1.0: HALT is terminal. No retry or recovery is permitted.
          </p>
          <p className="text-xs text-muted-foreground mt-1">
            Contact administrator if this halt is unexpected.
          </p>
        </div>

        {/* NO RETRY BUTTON - This is intentional per ECVM spec */}
      </div>
    </div>
  );
}
