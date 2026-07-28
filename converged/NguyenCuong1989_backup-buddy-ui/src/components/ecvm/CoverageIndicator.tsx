import { cn } from "@/lib/utils";

interface CoverageIndicatorProps {
  percent: number;
  className?: string;
}

export function CoverageIndicator({ percent, className }: CoverageIndicatorProps) {
  const getColorClass = (p: number) => {
    if (p >= 80) return "bg-coverage-high";
    if (p >= 50) return "bg-coverage-mid";
    return "bg-coverage-low";
  };

  const getTextColorClass = (p: number) => {
    if (p >= 80) return "text-coverage-high";
    if (p >= 50) return "text-coverage-mid";
    return "text-coverage-low";
  };

  return (
    <div className={cn("space-y-1", className)}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-mono text-muted-foreground">COVERAGE</span>
        <span className={cn("text-sm font-mono font-medium", getTextColorClass(percent))}>
          {percent.toFixed(1)}%
        </span>
      </div>
      <div className="h-1.5 bg-muted rounded-full overflow-hidden">
        <div
          className={cn("h-full rounded-full transition-all duration-500", getColorClass(percent))}
          style={{ width: `${Math.min(100, Math.max(0, percent))}%` }}
        />
      </div>
    </div>
  );
}
