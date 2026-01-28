import { cn } from "@/lib/utils";
import { ReactNode } from "react";

interface DataPanelProps {
  title: string;
  icon?: ReactNode;
  children: ReactNode;
  className?: string;
}

export function DataPanel({ title, icon, children, className }: DataPanelProps) {
  return (
    <div className={cn("ecvm-panel", className)}>
      <div className="ecvm-panel-header">
        {icon}
        <span>{title}</span>
      </div>
      {children}
    </div>
  );
}

interface DataRowProps {
  label: string;
  value: ReactNode;
  mono?: boolean;
  className?: string;
}

export function DataRow({ label, value, mono = true, className }: DataRowProps) {
  return (
    <div className={cn("flex items-center justify-between py-1.5", className)}>
      <span className="text-xs text-muted-foreground">{label}</span>
      <span className={cn("text-sm", mono && "font-mono")}>{value}</span>
    </div>
  );
}
