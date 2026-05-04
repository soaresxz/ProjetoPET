import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api, Pet } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { PawPrint, Phone, MapPin, Heart, CheckCircle2 } from "lucide-react";
import { toast } from "sonner";

export default function PetScan() {
  const { id } = useParams();
  const [pet, setPet] = useState<Pet | null>(null);
  const [loading, setLoading] = useState(true);
  const [sent, setSent] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState({ message: "", scanner_phone: "", location: "" });
  const [coords, setCoords] = useState<{ lat?: number; lng?: number }>({});

  useEffect(() => {
    if (!id) return;
    (async () => {
      try { setPet(await api.getPet(id)); }
      catch (e: any) { toast.error(e.message); }
      finally { setLoading(false); }
    })();
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => setCoords({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
        () => {}
      );
    }
  }, [id]);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) return;
    setSubmitting(true);
    try {
      await api.postScan(id, {
        message: form.message,
        scanner_phone: form.scanner_phone,
        location: form.location,
        latitude: coords.lat,
        longitude: coords.lng,
      });
      setSent(true);
      toast.success("Dono notificado por SMS!");
    } catch (e: any) { toast.error(e.message); }
    finally { setSubmitting(false); }
  };

  if (loading) return <div className="min-h-screen grid place-items-center text-muted-foreground">Carregando...</div>;
  if (!pet) return <div className="min-h-screen grid place-items-center">Pet não encontrado.</div>;

  return (
    <div className="min-h-screen bg-gradient-hero py-8 px-4">
      <div className="max-w-md mx-auto space-y-5">
        <Card className="p-6 text-center shadow-glow border-primary/20">
          <div className="h-24 w-24 mx-auto rounded-full bg-gradient-warm grid place-items-center text-primary-foreground overflow-hidden mb-4 shadow-glow">
            {pet.photo_url ? <img src={pet.photo_url} alt={pet.pet_name} className="h-full w-full object-cover" /> : <PawPrint className="h-10 w-10" />}
          </div>
          <p className="text-sm text-muted-foreground mb-1">Você encontrou</p>
          <h1 className="text-3xl font-bold">{pet.pet_name}!</h1>
          {pet.breed && <p className="text-muted-foreground">{pet.breed}</p>}
          {pet.notes && (
            <div className="mt-4 p-3 rounded-lg bg-muted text-sm text-left">
              <p className="font-medium mb-1 flex items-center gap-1"><Heart className="h-3.5 w-3.5 text-primary" /> Importante</p>
              <p className="text-muted-foreground">{pet.notes}</p>
            </div>
          )}
          {pet.owner_phone && (
            <a href={`tel:${pet.owner_phone}`} className="mt-4 flex items-center justify-center gap-2 w-full bg-accent text-accent-foreground rounded-lg py-3 font-semibold shadow-soft">
              <Phone className="h-4 w-4" /> Ligar para o dono
            </a>
          )}
        </Card>

        {sent ? (
          <Card className="p-6 text-center shadow-soft">
            <CheckCircle2 className="mx-auto h-12 w-12 text-accent mb-2" />
            <h2 className="font-bold text-lg">Dono notificado!</h2>
            <p className="text-sm text-muted-foreground">Um SMS foi enviado com seus dados. Obrigado por ajudar! 🐾</p>
          </Card>
        ) : (
          <Card className="p-6 shadow-soft">
            <h2 className="font-semibold mb-1">Avise o dono</h2>
            <p className="text-sm text-muted-foreground mb-4">Envie uma mensagem rápida — o dono receberá um SMS na hora.</p>
            <form onSubmit={submit} className="space-y-3">
              <div className="space-y-1.5">
                <Label htmlFor="location" className="flex items-center gap-1 text-xs"><MapPin className="h-3 w-3" /> Onde encontrou</Label>
                <Input id="location" value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} placeholder="Ex.: Praça XV, perto da padaria" />
              </div>
              <div className="space-y-1.5">
                <Label htmlFor="phone" className="text-xs">Seu telefone (opcional)</Label>
                <Input id="phone" value={form.scanner_phone} onChange={(e) => setForm({ ...form, scanner_phone: e.target.value })} placeholder="+55 11 99999-9999" />
              </div>
              <div className="space-y-1.5">
                <Label htmlFor="msg" className="text-xs">Mensagem (opcional)</Label>
                <Textarea id="msg" value={form.message} onChange={(e) => setForm({ ...form, message: e.target.value })} placeholder="Está bem, levei pra dentro..." rows={3} />
              </div>
              {coords.lat && <p className="text-xs text-accent">📍 Localização do GPS será enviada</p>}
              <Button type="submit" disabled={submitting} className="w-full bg-gradient-warm shadow-glow border-0">
                {submitting ? "Enviando..." : "Notificar dono"}
              </Button>
            </form>
          </Card>
        )}
      </div>
    </div>
  );
}
