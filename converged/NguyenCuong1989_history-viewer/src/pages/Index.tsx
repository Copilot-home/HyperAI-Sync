import { Link } from "react-router-dom";
import { Shield, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

const Index = () => {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <div className="text-center space-y-6">
        <div className="flex items-center justify-center gap-3">
          <Shield className="h-10 w-10 text-primary" />
          <h1 className="text-4xl font-bold font-mono text-foreground">ECVM</h1>
        </div>
        <p className="text-lg text-muted-foreground max-w-md">
          Execution Control Virtual Machine
        </p>
        <Link to="/app/user/history">
          <Button variant="outline" className="gap-2">
            View Execution History
            <ArrowRight className="h-4 w-4" />
          </Button>
        </Link>
      </div>
    </div>
  );
};

export default Index;
