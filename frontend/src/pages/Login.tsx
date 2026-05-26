import { useNavigate, Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { PawPrint, ShieldCheck, ArrowRight } from "lucide-react";
import { loginAsAdmin, isAdmin } from "@/lib/auth";
import { toast } from "sonner";
import { useEffect } from "react";

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation() as { state?: { from?: { pathname?: string } } };
  const redirectTo = location.state?.from?.pathname || "/admin";

  useEffect(() => {
    if (isAdmin()) navigate(redirectTo, { replace: true });
  }, [navigate, redirectTo]);

  const handleLogin = () => {
    loginAsAdmin();
    toast.success("Bem-vindo, admin!");
    navigate(redirectTo, { replace: true });
  };

  return (
    <div className="min-h-screen bg-gradient-hero grid place-items-center px-4">
      <div className="w-full max-w-md space-y-6">
        <Link to="/" className="flex items-center justify-center gap-2 font-bold text-lg">
          <span className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-warm text-primary-foreground shadow-glow">
            <PawPrint className="h-5 w-5" />
          </span>
          EncontreMeuPet
        </Link>

        <Card className="p-8 shadow-soft space-y-6">
          <div className="text-center space-y-2">
            <div className="mx-auto grid h-12 w-12 place-items-center rounded-xl bg-muted">
              <ShieldCheck className="h-6 w-6 text-primary" />
            </div>
            <h1 className="text-2xl font-bold">Acesso ao painel</h1>
            <p className="text-sm text-muted-foreground">
              Área restrita para administradores. Esta é uma autenticação mockada para demonstração.
            </p>
          </div>

          <Button onClick={handleLogin} className="w-full bg-gradient-warm border-0 shadow-glow" size="lg">
            Entrar como admin <ArrowRight className="ml-1 h-4 w-4" />
          </Button>

          <p className="text-xs text-center text-muted-foreground">
            Sem backend real — salva <code className="px-1 rounded bg-muted">isAdmin</code> no localStorage.
          </p>
        </Card>
      </div>
    </div>
  );
}
