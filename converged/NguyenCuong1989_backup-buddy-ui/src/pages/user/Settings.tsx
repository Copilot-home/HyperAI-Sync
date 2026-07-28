import { useState } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { DataPanel, DataRow } from "@/components/ecvm/DataPanel";
import { WorkflowSettings, TaskType } from "@/types/ecvm";
import { Settings, Save, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

const taskTypeOptions: TaskType[] = ["image", "image_static", "video"];

export default function SettingsPage() {
  const [settings, setSettings] = useState<WorkflowSettings>({
    default_task_type: "image",
    auto_select_required_logic: true,
    max_concurrent_tasks: 3,
  });

  const [isDirty, setIsDirty] = useState(false);

  const handleChange = <K extends keyof WorkflowSettings>(
    key: K,
    value: WorkflowSettings[K]
  ) => {
    setSettings(prev => ({ ...prev, [key]: value }));
    setIsDirty(true);
  };

  const handleSave = () => {
    // In production: POST to settings endpoint
    toast.success("Settings saved");
    setIsDirty(false);
  };

  return (
    <AppLayout>
      <PageHeader
        title="Workflow Settings"
        subtitle="Bounded customization only"
        icon={<Settings className="h-5 w-5 text-muted-foreground" />}
        actions={
          <Button
            onClick={handleSave}
            disabled={!isDirty}
            className="font-mono text-sm"
          >
            <Save className="h-4 w-4 mr-2" />
            Save Changes
          </Button>
        }
      />

      <div className="p-6 space-y-6">
        {/* Constraint Notice */}
        <div className="ecvm-reason-panel flex items-start gap-3">
          <AlertCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
          <div>
            <div className="text-sm font-medium text-foreground/80 mb-1">
              Bounded Configuration
            </div>
            <div className="text-xs text-disabled-foreground">
              Settings are limited to workflow customization. Law and logic rule
              configurations cannot be modified from this interface. Contact
              administrator for policy changes.
            </div>
          </div>
        </div>

        {/* Default Task Type */}
        <DataPanel title="Default Task Type">
          <div className="flex gap-2">
            {taskTypeOptions.map((type) => (
              <button
                key={type}
                onClick={() => handleChange("default_task_type", type)}
                className={cn(
                  "px-4 py-2 rounded-md border text-sm font-mono transition-colors",
                  settings.default_task_type === type
                    ? "bg-primary text-primary-foreground border-primary"
                    : "bg-card border-border text-muted-foreground hover:text-foreground hover:border-foreground/30"
                )}
              >
                {type}
              </button>
            ))}
          </div>
          <p className="text-xs text-muted-foreground mt-2">
            Pre-selected task type when opening Generate page
          </p>
        </DataPanel>

        {/* Auto-select Required Logic */}
        <DataPanel title="Logic Selection Behavior">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm font-medium">Auto-select Required Logic</div>
              <div className="text-xs text-muted-foreground mt-0.5">
                Automatically select logic rules marked as required
              </div>
            </div>
            <Switch
              checked={settings.auto_select_required_logic}
              onCheckedChange={(checked) =>
                handleChange("auto_select_required_logic", checked)
              }
            />
          </div>
        </DataPanel>

        {/* Max Concurrent Tasks */}
        <DataPanel title="Concurrency Limits">
          <DataRow
            label="Max Concurrent Tasks"
            value={
              <select
                value={settings.max_concurrent_tasks}
                onChange={(e) =>
                  handleChange("max_concurrent_tasks", Number(e.target.value))
                }
                className="bg-muted border border-border rounded px-2 py-1 text-sm font-mono"
              >
                {[1, 2, 3, 5, 10].map((n) => (
                  <option key={n} value={n}>
                    {n}
                  </option>
                ))}
              </select>
            }
            mono={false}
          />
          <p className="text-xs text-muted-foreground mt-2">
            Maximum number of tasks that can be queued simultaneously
          </p>
        </DataPanel>

        {/* Read-only System Info */}
        <DataPanel title="System Information (Read-only)">
          <div className="space-y-1 text-muted-foreground">
            <DataRow label="API Version" value="v1.0.0" />
            <DataRow label="Law Override" value="DISABLED" />
            <DataRow label="Role" value="user" />
          </div>
        </DataPanel>
      </div>
    </AppLayout>
  );
}
