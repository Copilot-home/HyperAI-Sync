import { AlertCircle } from "lucide-react";
import { DisableReason } from "@/types/ecvm";
import { cn } from "@/lib/utils";

interface ReasonPanelProps {
  reasons: DisableReason[];
  className?: string;
}

export function ReasonPanel({ reasons, className }: ReasonPanelProps) {
  if (reasons.length === 0) return null;

  return (
    <div className={cn("ecvm-reason-panel", className)}>
      <div className="flex items-center gap-2 mb-2 text-disabled-foreground">
        <AlertCircle className="h-4 w-4" />
        <span className="uppercase tracking-wider text-[10px] font-medium">Action Disabled</span>
      </div>
      <div className="space-y-2">
        {reasons.map((reason, index) => (
          <div key={index} className="space-y-0.5">
            <div className="text-foreground/80">[{reason.code}] {reason.message}</div>
            <div className="text-disabled-foreground text-[11px] pl-2 border-l border-disabled">
              {reason.technical_detail}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
