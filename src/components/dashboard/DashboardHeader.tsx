import { Badge } from "@/components/ui/badge";
import { Shield, Lock } from "lucide-react";

export function DashboardHeader() {
  return (
    <header className="border-b bg-card">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
              <Shield className="h-6 w-6 text-primary" />
            </div>
            <div>
              <h1 className="text-xl font-semibold tracking-tight">
                APO/ECVM Control Panel
              </h1>
              <p className="text-sm text-muted-foreground">
                Identity-Preserving Generative System Dashboard
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="gap-1">
              <Lock className="h-3 w-3" />
              Read-Only Mode
            </Badge>
            <Badge variant="secondary">
              Audit Grade
            </Badge>
          </div>
        </div>
      </div>
    </header>
  );
}
