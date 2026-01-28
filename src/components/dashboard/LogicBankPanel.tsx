import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { Blocks, Lock, AlertTriangle } from "lucide-react";
import { useLogicModules } from "@/hooks/useLogicModules";
import { Skeleton } from "@/components/ui/skeleton";

export function LogicBankPanel() {
  const { data: modules, isLoading, error } = useLogicModules();

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Blocks className="h-5 w-5" />
            Logic Bank
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-16 w-full" />
          ))}
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Blocks className="h-5 w-5" />
            Logic Bank
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-destructive text-sm">Failed to load logic modules</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Blocks className="h-5 w-5" />
          Logic Bank
        </CardTitle>
        <CardDescription>Module registry and identity requirements (read-only)</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {modules && modules.length > 0 ? (
          modules.map((module) => {
            const requiredState = Number(module.required_identity_state) || 0;
            const deps = (module.dependencies as string[]) || [];
            
            return (
              <div 
                key={module.id} 
                className="flex items-center justify-between rounded-lg border p-3"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-sm">{module.module_name}</span>
                    <Lock className="h-3 w-3 text-muted-foreground" />
                  </div>
                  {module.description && (
                    <p className="text-xs text-muted-foreground">{module.description}</p>
                  )}
                  <div className="flex items-center gap-2">
                    <Badge variant="outline" className="text-xs">
                      Req: {requiredState}%
                    </Badge>
                    {deps.length > 0 && (
                      <Badge variant="secondary" className="text-xs">
                        {deps.length} deps
                      </Badge>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Switch 
                    checked={module.is_enabled ?? false} 
                    disabled 
                    aria-label="Module enabled state (read-only)"
                  />
                </div>
              </div>
            );
          })
        ) : (
          <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
            <AlertTriangle className="h-8 w-8 mb-2" />
            <p className="text-sm">No logic modules registered</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
