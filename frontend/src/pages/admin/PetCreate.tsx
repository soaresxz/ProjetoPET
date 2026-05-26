import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import { toast } from "sonner";
import { ArrowLeft } from "lucide-react";

export default function PetCreate() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [phone, setPhone] = useState("");

  const formatPhone = (value: string) => {
    const numbers = value.replace(/\D/g, "");

    const limited = numbers.slice(0, 13);

    if (limited.length <= 2) {
      return `+${limited}`;
    }

    if (limited.length <= 4) {
      return `+${limited.slice(0, 2)} ${limited.slice(2)}`;
    }

    if (limited.length <= 9) {
      return `+${limited.slice(0, 2)} ${limited.slice(2, 4)} ${limited.slice(4)}`;
    }

    return `+${limited.slice(0, 2)} ${limited.slice(2, 4)} ${limited.slice(4, 9)}-${limited.slice(9)}`;
  };

  const submit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const data = new FormData(e.currentTarget);

    const rawPhone = (data.get("owner_phone") as string) || "";

    const formattedPhone =
      "+" + rawPhone.replace(/\D/g, "");

    const payload = {
      pet_name: (data.get("pet_name") as string) || "",
      owner_name: (data.get("owner_name") as string) || "",
      owner_phone: formattedPhone || "",
      breed: (data.get("breed") as string) || "",
      photo_url: (data.get("photo_url") as string) || "",
      notes: (data.get("notes") as string) || "",
    };

    console.log("ENVIANDO:", payload);

    if (!payload.pet_name || !payload.owner_phone) {
      toast.error("Nome do pet e telefone são obrigatórios.");
      return;
    }

    setLoading(true);
    try {
      const pet = await api.createPet(payload);

      const id = (pet as any).id ?? (pet as any).pet_id;

      toast.success("Pet cadastrado!");
      navigate(`/admin/pets/${id}/qr`);
    } catch (e: any) {
      console.error("ERRO CREATE:", e);
      toast.error(e.message || "Erro ao cadastrar pet");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <Button variant="ghost" onClick={() => navigate(-1)} className="-ml-3">
        <ArrowLeft className="mr-2 h-4 w-4" /> Voltar
      </Button>

      <div>
        <h1 className="text-3xl font-bold">Novo Pet</h1>
        <p className="text-muted-foreground text-sm">
          Cadastre um pet para gerar seu QR code.
        </p>
      </div>

      <Card className="p-6 shadow-soft">
        <form onSubmit={submit} className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">

            <div className="space-y-2">
              <Label htmlFor="pet_name">Nome do pet *</Label>
              <Input id="pet_name" name="pet_name" placeholder="Rex" />
            </div>

            <div className="space-y-2">
              <Label htmlFor="breed">Raça</Label>
              <Input id="breed" name="breed" placeholder="Vira-lata" />
            </div>

            <div className="space-y-2">
              <Label htmlFor="owner_name">Nome do dono</Label>
              <Input id="owner_name" name="owner_name" />
            </div>

            <div className="space-y-2">
              <Label htmlFor="owner_phone">Telefone do dono *</Label>
              <Input
                id="owner_phone"
                name="owner_phone"
                placeholder="+55 11 99999-9999"
                value={phone}
                onChange={(e) => {
                  const formatted = formatPhone(e.target.value);
                  setPhone(formatted);
                }}
              />
            </div>

          </div>

          <div className="space-y-2">
            <Label htmlFor="photo_url">URL da foto</Label>
            <Input id="photo_url" name="photo_url" placeholder="https://..." />
          </div>

          <div className="space-y-2">
            <Label htmlFor="notes">Observações</Label>
            <Textarea
              id="notes"
              name="notes"
              placeholder="Alergias, medicamentos, comportamento..."
              rows={4}
            />
          </div>

          <Button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-warm shadow-glow border-0"
          >
            {loading ? "Salvando..." : "Cadastrar e gerar QR"}
          </Button>
        </form>
      </Card>
    </div>
  );
}
