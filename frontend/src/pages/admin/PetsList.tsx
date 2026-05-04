import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, Pet } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { QrCode, Trash2, Eye, Plus, Search, PawPrint } from "lucide-react";
import { toast } from "sonner";
import {
  AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent,
  AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger,
} from "@/components/ui/alert-dialog";

export default function PetsList() {
  const [pets, setPets] = useState<Pet[] | null>(null);
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const data = await api.listPets();
      setPets(data);
    } catch (e: any) {
      toast.error(e.message);
      setPets([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleDelete = async (id: string) => {
    try {
      await api.deletePet(id);
      toast.success("Pet removido");
      load();
    } catch (e: any) {
      toast.error(e.message);
    }
  };

  const filtered = (pets || []).filter(p =>
    !q ||
    p.pet_name?.toLowerCase().includes(q.toLowerCase()) ||
    p.owner_name?.toLowerCase().includes(q.toLowerCase())
  );
  
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-3xl font-bold">Pets</h1>
          <p className="text-muted-foreground text-sm">Gerencie todos os pets cadastrados.</p>
        </div>
        <Button asChild className="bg-gradient-warm shadow-glow border-0">
          <Link to="/admin/new">
            <Plus className="mr-2 h-4 w-4" /> Novo pet
          </Link>
        </Button>
      </div>

      <div className="relative max-w-md">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Buscar por nome ou dono..."
          className="pl-9"
        />
      </div>

      {loading ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map(i => (
            <Card key={i} className="h-40 animate-pulse bg-muted" />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <Card className="p-12 text-center">
          <PawPrint className="mx-auto h-12 w-12 text-muted-foreground mb-3" />
          <p className="text-muted-foreground">Nenhum pet encontrado.</p>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filtered.map((p) => (
            <Card key={p.id} className="p-5 shadow-soft hover:shadow-glow transition-shadow">
              <div className="flex items-start gap-4">
                <div className="h-14 w-14 rounded-xl bg-gradient-warm grid place-items-center text-primary-foreground shrink-0 overflow-hidden">
                  {p.photo_url ? (
                    <img src={p.photo_url} alt={p.pet_name} className="h-full w-full object-cover" />
                  ) : (
                    <PawPrint className="h-6 w-6" />
                  )}
                </div>

                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold truncate">{p.pet_name}</h3>
                  <p className="text-xs text-muted-foreground truncate">
                    {p.owner_name || "—"}
                  </p>
                  <p className="text-xs text-muted-foreground truncate">
                    {p.owner_phone || ""}
                  </p>
                </div>
              </div>

              <div className="mt-4 flex gap-2">
                <Button asChild size="sm" variant="outline" className="flex-1">
                  <Link to={`/admin/pets/${p.id}`}>
                    <Eye className="mr-1 h-3.5 w-3.5" /> Detalhes
                  </Link>
                </Button>

                <Button asChild size="sm" variant="outline">
                  <Link to={`/admin/pets/${p.id}/qr`}>
                    <QrCode className="h-3.5 w-3.5" />
                  </Link>
                </Button>

                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button size="sm" variant="outline" className="text-destructive hover:text-destructive">
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </AlertDialogTrigger>

                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>
                        Remover {p.pet_name}?
                      </AlertDialogTitle>
                      <AlertDialogDescription>
                        Esta ação não pode ser desfeita.
                      </AlertDialogDescription>
                    </AlertDialogHeader>

                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancelar</AlertDialogCancel>
                      <AlertDialogAction
                        onClick={() => handleDelete(p.id)}
                        className="bg-destructive text-destructive-foreground"
                      >
                        Remover
                      </AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}