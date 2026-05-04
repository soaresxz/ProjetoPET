import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, Pet, Scan } from "@/lib/api";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, QrCode, MapPin, Phone, Clock, PawPrint } from "lucide-react";
import { toast } from "sonner";

export default function PetDetail() {
  const { id } = useParams();
  const [pet, setPet] = useState<Pet | null>(null);
  const [scans, setScans] = useState<Scan[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    
    console.log(window.location.pathname)
    console.log(id)
    if (!id) return;

    const loadData = async () => {
      setLoading(true);

      try {
        const p = await api.getPet(id);
        console.log("PET:", p);
        setPet(p);
      } catch (e: any) {
        console.log("ERRO PET:", e);
        toast.error("Erro ao carregar pet");
        setPet(null);
      }

      try {
        const s = await api.getScans(id);
        setScans(s);
      } catch (e: any) {
        console.log("ERRO SCANS:", e);
        toast.error("Erro ao carregar scans");
      }

      setLoading(false);
    };

    loadData();
  }, [id]);

  if (loading) return <div className="text-muted-foreground">Carregando...</div>;
  if (!pet) return <div>Pet não encontrado.</div>;

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <Button asChild variant="ghost" className="-ml-3">
        <Link to="/admin">
          <ArrowLeft className="mr-2 h-4 w-4" /> Voltar
        </Link>
      </Button>

      <Card className="p-6 shadow-soft">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="flex items-start gap-4">
            <div className="h-20 w-20 rounded-2xl bg-gradient-warm grid place-items-center text-primary-foreground overflow-hidden">
              {pet.photo_url ? (
                <img src={pet.photo_url} alt={pet.pet_name} className="h-full w-full object-cover" />
              ) : (
                <PawPrint className="h-8 w-8" />
              )}
            </div>

            <div>
              <h1 className="text-3xl font-bold">{pet.pet_name}</h1>

              {pet.breed && (
                <p className="text-muted-foreground">{pet.breed}</p>
              )}

              <div className="mt-2 text-sm text-muted-foreground space-y-1">
                {pet.owner_name && (
                  <p>
                    Dono: <span className="text-foreground">{pet.owner_name}</span>
                  </p>
                )}

                {pet.owner_phone && (
                  <p className="flex items-center gap-1">
                    <Phone className="h-3.5 w-3.5" /> {pet.owner_phone}
                  </p>
                )}
              </div>
            </div>
          </div>

          <Button asChild className="bg-gradient-warm shadow-glow border-0">
            <Link to={`/admin/pets/${pet.id}/qr`}>
              <QrCode className="mr-2 h-4 w-4" /> Ver QR Code
            </Link>
          </Button>
        </div>

        {pet.notes && (
          <div className="mt-4 p-4 rounded-lg bg-muted text-sm">
            <p className="font-medium mb-1">Observações</p>
            <p className="text-muted-foreground whitespace-pre-wrap">
              {pet.notes}
            </p>
          </div>
        )}
      </Card>

      <div>
        <h2 className="text-xl font-semibold mb-3">
          Histórico de scans ({scans.length})
        </h2>

        {scans.length === 0 ? (
          <Card className="p-8 text-center text-muted-foreground">
            Ainda nenhum scan registrado.
          </Card>
        ) : (
          <div className="space-y-3">
            {scans.map((s, i) => (
              <Card key={s.id || i} className="p-4 shadow-soft">
                <div className="flex items-start gap-3">
                  <div className="grid h-9 w-9 place-items-center rounded-lg bg-secondary/10 text-secondary shrink-0">
                    <MapPin className="h-4 w-4" />
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex flex-wrap justify-between gap-2">
                      <p className="font-medium">
                        {s.location || "Localização desconhecida"}
                      </p>

                      {s.scanned_at && (
                        <p className="text-xs text-muted-foreground flex items-center gap-1">
                          <Clock className="h-3 w-3" />{" "}
                          {new Date(s.scanned_at).toLocaleString("pt-BR")}
                        </p>
                      )}
                    </div>

                    {s.message && (
                      <p className="text-sm text-muted-foreground mt-1">
                        "{s.message}"
                      </p>
                    )}

                    {s.scanner_phone && (
                      <p className="text-xs text-muted-foreground mt-1">
                        Contato: {s.scanner_phone}
                      </p>
                    )}

                    {s.latitude && s.longitude && (
                      <a
                        className="text-xs text-primary hover:underline"
                        target="_blank"
                        rel="noreferrer"
                        href={`https://maps.google.com/?q=${s.latitude},${s.longitude}`}
                      >
                        Ver no mapa →
                      </a>
                    )}
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}