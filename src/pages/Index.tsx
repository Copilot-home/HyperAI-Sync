import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Shield, ArrowRight } from "lucide-react";

export default function Index() {
  const navigate = useNavigate();

  useEffect(() => {
    // Auto-redirect to user identity page after brief display
    const timer = setTimeout(() => {
      navigate("/app/user/identity");
    }, 2000);
    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      <div className="text-center space-y-6">
        <div className="flex items-center justify-center gap-3">
          <Shield className="h-10 w-10 text-foreground" />
          <h1 className="text-2xl font-mono font-semibold">ECVM.AGENT</h1>
        </div>
        <div className="space-y-1">
          <p className="text-sm font-mono text-muted-foreground">
            Hub Backup v2.0 | Context Renderer Mode
          </p>
          <p className="text-xs font-mono text-muted-foreground/70">
            ECVM-CS-1.0-MASTER
          </p>
        </div>
        <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
          <span className="h-2 w-2 rounded-full bg-status-pass animate-pulse-subtle" />
          <span className="font-mono">Initializing</span>
          <ArrowRight className="h-4 w-4" />
        </div>
      </div>
    </div>
  );
}
