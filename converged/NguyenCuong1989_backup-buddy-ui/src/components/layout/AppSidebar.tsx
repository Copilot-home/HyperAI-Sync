import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";
import {
  User,
  Sparkles,
  History,
  Settings,
  LayoutDashboard,
  Database,
  AlertTriangle,
  Activity,
  FileText,
  Shield,
} from "lucide-react";

const userNavItems = [
  { path: "/app/user/identity", label: "Identity", icon: User },
  { path: "/app/user/generate", label: "Generate", icon: Sparkles },
  { path: "/app/user/history", label: "History", icon: History },
  { path: "/app/user/settings", label: "Settings", icon: Settings },
];

const adminNavItems = [
  { path: "/app/admin/overview", label: "Overview", icon: LayoutDashboard },
  { path: "/app/admin/logic-bank", label: "Logic Bank", icon: Database },
  { path: "/app/admin/unmet-logic", label: "Unmet Logic", icon: AlertTriangle },
  { path: "/app/admin/drift", label: "Drift", icon: Activity },
  { path: "/app/admin/audit", label: "Audit", icon: FileText },
];

export function AppSidebar() {
  const location = useLocation();

  return (
    <aside className="w-56 bg-sidebar border-r border-sidebar-border flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-sidebar-border">
        <div className="flex items-center gap-2">
          <Shield className="h-5 w-5 text-sidebar-foreground" />
          <span className="font-mono text-sm font-semibold text-sidebar-foreground">
            ECVM.AGENT
          </span>
        </div>
        <div className="mt-1 text-[10px] font-mono text-sidebar-foreground/50 uppercase tracking-wider">
          Hub Backup v2.0
        </div>
      </div>

      {/* User Navigation */}
      <nav className="p-3 space-y-1">
        <div className="ecvm-section-title px-3 py-2 text-sidebar-foreground/50">
          User Context
        </div>
        {userNavItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                "ecvm-nav-item",
                isActive ? "ecvm-nav-item-active" : "ecvm-nav-item-inactive"
              )}
            >
              <item.icon className="h-4 w-4" />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Admin Navigation */}
      <nav className="p-3 space-y-1 border-t border-sidebar-border">
        <div className="ecvm-section-title px-3 py-2 text-sidebar-foreground/50">
          Admin Context
        </div>
        {adminNavItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                "ecvm-nav-item",
                isActive ? "ecvm-nav-item-active" : "ecvm-nav-item-inactive"
              )}
            >
              <item.icon className="h-4 w-4" />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="mt-auto p-4 border-t border-sidebar-border">
        <div className="text-[10px] font-mono text-sidebar-foreground/40 space-y-0.5">
          <div>ECVM-CS-1.0-MASTER</div>
          <div>Context Renderer Mode</div>
          <div className="flex items-center gap-1.5 mt-2">
            <span className="h-1.5 w-1.5 rounded-full bg-status-pass animate-pulse-subtle" />
            <span>System Online</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
