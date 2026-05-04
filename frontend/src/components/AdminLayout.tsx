import { NavLink, Outlet, Link, useNavigate } from "react-router-dom";
import { PawPrint, List, Plus, LogOut } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { logout } from "@/lib/auth";
import { toast } from "sonner";

const links = [
  { to: "/admin", label: "Pets", icon: List, end: true },
  { to: "/admin/new", label: "Novo Pet", icon: Plus },
];

export default function AdminLayout() {
  const navigate = useNavigate();
  const handleLogout = () => {
    logout();
    toast.success("Sessão encerrada");
    navigate("/login", { replace: true });
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-card/60 backdrop-blur sticky top-0 z-40">
        <div className="container flex h-16 items-center justify-between">
          <Link to="/" className="flex items-center gap-2 font-bold text-lg">
            <span className="grid h-9 w-9 place-items-center rounded-xl bg-gradient-warm text-primary-foreground shadow-glow">
              <PawPrint className="h-5 w-5" />
            </span>
            Pet QR Tracker
          </Link>
          <nav className="flex items-center gap-1">
            {links.map((l) => (
              <NavLink
                key={l.to}
                to={l.to}
                end={l.end}
                className={({ isActive }) =>
                  cn(
                    "flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                    isActive
                      ? "bg-primary text-primary-foreground shadow-soft"
                      : "text-muted-foreground hover:bg-muted hover:text-foreground"
                  )
                }
              >
                <l.icon className="h-4 w-4" />
                <span className="hidden sm:inline">{l.label}</span>
              </NavLink>
            ))}
            <Button
              variant="ghost"
              size="sm"
              onClick={handleLogout}
              className="ml-1 text-muted-foreground hover:text-foreground"
            >
              <LogOut className="h-4 w-4" />
              <span className="hidden sm:inline">Sair</span>
            </Button>
          </nav>
        </div>
      </header>
      <main className="container py-8">
        <Outlet />
      </main>
    </div>
  );
}
