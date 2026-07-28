import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Lock, Scale, Eye, Fingerprint, Mic, MessageSquare, Zap } from "lucide-react";

const AXES_DEFINITIONS = [
  { 
    id: "visual", 
    name: "Visual Identity", 
    icon: Eye, 
    description: "Facial landmarks, body structure, distinctive features" 
  },
  { 
    id: "biometric", 
    name: "Biometric Signature", 
    icon: Fingerprint, 
    description: "Unique biological markers and patterns" 
  },
  { 
    id: "vocal", 
    name: "Vocal Pattern", 
    icon: Mic, 
    description: "Voice timbre, speech patterns, acoustic signature" 
  },
  { 
    id: "behavioral", 
    name: "Behavioral", 
    icon: MessageSquare, 
    description: "Mannerisms, expressions, characteristic movements" 
  },
  { 
    id: "temporal", 
    name: "Temporal Coherence", 
    icon: Zap, 
    description: "Consistency across time and frame sequences" 
  },
];

export function AxesPanel() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Scale className="h-5 w-5" />
          Identity Axes (Law)
          <Lock className="h-4 w-4 text-muted-foreground" />
        </CardTitle>
        <CardDescription>
          Immutable identity preservation dimensions — read-only, no mutation allowed
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid gap-3">
          {AXES_DEFINITIONS.map((axis) => {
            const Icon = axis.icon;
            return (
              <div 
                key={axis.id}
                className="flex items-center gap-3 rounded-lg border bg-muted/30 p-3"
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-md bg-background border">
                  <Icon className="h-5 w-5 text-muted-foreground" />
                </div>
                <div className="flex-1 space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-sm">{axis.name}</span>
                    <Badge variant="outline" className="text-xs">
                      LOCKED
                    </Badge>
                  </div>
                  <p className="text-xs text-muted-foreground">{axis.description}</p>
                </div>
              </div>
            );
          })}
        </div>
        <p className="mt-4 text-xs text-muted-foreground text-center">
          These axes define the identity preservation law and cannot be modified from this interface.
        </p>
      </CardContent>
    </Card>
  );
}
