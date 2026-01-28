import { cn } from "@/lib/utils";
import { VerdictStatus, EntityStatus } from "@/types/ecvm";
import { CheckCircle, XCircle, AlertTriangle, Clock, Circle } from "lucide-react";

interface StatusBadgeProps {
  status: VerdictStatus | EntityStatus;
  className?: string;
}

const verdictConfig: Record<VerdictStatus, { icon: typeof CheckCircle; className: string }> = {
  PASS: {
    icon: CheckCircle,
    className: "bg-status-pass-bg text-status-pass-foreground border-status-pass/30",
  },
  REJECT: {
    icon: XCircle,
    className: "bg-status-reject-bg text-status-reject-foreground border-status-reject/30",
  },
  HALT: {
    icon: AlertTriangle,
    className: "bg-status-halt-bg text-status-halt-foreground border-status-halt/30",
  },
};

const entityConfig: Record<EntityStatus, { icon: typeof Circle; className: string }> = {
  active: {
    icon: CheckCircle,
    className: "bg-status-pass-bg text-status-pass-foreground border-status-pass/30",
  },
  pending: {
    icon: Clock,
    className: "bg-status-halt-bg text-status-halt-foreground border-status-halt/30",
  },
  suspended: {
    icon: XCircle,
    className: "bg-status-reject-bg text-status-reject-foreground border-status-reject/30",
  },
  unknown: {
    icon: Circle,
    className: "bg-status-pending-bg text-status-pending-foreground border-status-pending/30",
  },
};

export function StatusBadge({ status, className }: StatusBadgeProps) {
  const isVerdict = ['PASS', 'REJECT', 'HALT'].includes(status);
  const config = isVerdict 
    ? verdictConfig[status as VerdictStatus] 
    : entityConfig[status as EntityStatus];
  
  const Icon = config.icon;

  return (
    <span
      className={cn(
        "ecvm-status-badge border",
        config.className,
        className
      )}
    >
      <Icon className="h-3 w-3" />
      {status}
    </span>
  );
}
