import { Shield, Lock, Unlock, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";

interface IdentityGateProps {
  identityState: string;
  entityId?: string;
  isLocked?: boolean;
  className?: string;
}

/**
 * ECVM Identity Gate Component
 * Per ECVM-CS-1.0: Visual indicator of identity state for gating decisions
 * This component ONLY displays state, does not make decisions
 */
export function IdentityGate({ identityState, entityId, isLocked, className }: IdentityGateProps) {
  const gateOpen = identityState === "ESTABLISHED";
  
  const stateConfig: Record<string, { icon: typeof AlertTriangle; color: string; bg: string }> = {
    NO_IDENTITY: { icon: Lock, color: "text-status-pending", bg: "bg-status-pending-bg" },
    INSUFFICIENT: { icon: Lock, color: "text-status-halt", bg: "bg-status-halt-bg" },
    ESTABLISHED: { icon: Unlock, color: "text-status-pass", bg: "bg-status-pass-bg" },
    DRIFT: { icon: AlertTriangle, color: "text-status-reject", bg: "bg-status-reject-bg" },
  };

  const config = stateConfig[identityState] || stateConfig.NO_IDENTITY;
  const Icon = config.icon;

  return (
    <div className={cn(
      "flex items-center gap-3 p-3 rounded-lg border",
      gateOpen ? "border-status-pass/30" : "border-status-halt/30",
      config.bg,
      className
    )}>
      <div className={cn("p-2 rounded-md", gateOpen ? "bg-status-pass/20" : "bg-background/50")}>
        <Icon className={cn("h-5 w-5", config.color)} />
      </div>
      
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className={cn(
            "text-xs font-mono uppercase tracking-wider px-2 py-0.5 rounded",
            config.bg,
            config.color.replace("text-", "text-") + "-foreground"
          )}>
            {identityState}
          </span>
          {isLocked && (
            <span title="Identity locked">
              <Shield className="h-3.5 w-3.5 text-muted-foreground" />
            </span>
          )}
        </div>
        {entityId && (
          <div className="text-xs font-mono text-muted-foreground mt-1 truncate">
            {entityId}
          </div>
        )}
      </div>

      <div className={cn(
        "text-xs font-mono uppercase tracking-wider",
        gateOpen ? "text-status-pass" : "text-status-halt"
      )}>
        {gateOpen ? "GATE OPEN" : "GATE CLOSED"}
      </div>
    </div>
  );
}
