import { useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Shield, ArrowRight, LogIn } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/hooks/useAuth";

export default function Index() {
  const navigate = useNavigate();
  const { user, loading } = useAuth();

  useEffect(() => {
    // Auto-redirect authenticated users
    if (user && !loading) {
      navigate("/app/user/identity");
    }
  }, [user, loading, navigate]);

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
            ECVM-CS-1.0-MASTER · Kernel v0.1.3
          </p>
        </div>
        
        {!loading && !user && (
          <div className="pt-4">
            <Button asChild variant="default" size="lg">
              <Link to="/auth" className="flex items-center gap-2">
                <LogIn className="h-4 w-4" />
                Sign In to Continue
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
          </div>
        )}

        {loading && (
          <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
            <span className="h-2 w-2 rounded-full bg-status-pass animate-pulse" />
            <span className="font-mono">Initializing</span>
          </div>
        )}
      </div>
    </div>
  );
}
