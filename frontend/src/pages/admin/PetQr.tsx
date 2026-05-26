import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, getBaseUrl } from "@/lib/api";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Download, Printer, Copy, Check } from "lucide-react";
import { toast } from "sonner";

export default function PetQr() {
  const { id } = useParams();
  const [src, setSrc] = useState<string>("");
  const [copied, setCopied] = useState(false);
  const scanUrl = id ? `${getBaseUrl()}/pet/${id}` : "";

  useEffect(() => {
    if (!id) return;
    (async () => {
      try {
        const blob = await api.fetchQrBlob(id);
        setSrc(URL.createObjectURL(blob));
      } catch (e: any) { toast.error(e.message); }
    })();
    return () => { if (src) URL.revokeObjectURL(src); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const copy = async () => {
    try {

      if (navigator.clipboard) {
        await navigator.clipboard.writeText(scanUrl);

      } else {
        const textArea = document.createElement("textarea");

        textArea.value = scanUrl;

        document.body.appendChild(textArea);

        textArea.select();

        document.execCommand("copy");

        document.body.removeChild(textArea);
      }

      setCopied(true);

      setTimeout(() => setCopied(false), 1500);

    } catch (err) {
      console.error("Erro ao copiar:", err);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <Button asChild variant="ghost" className="-ml-3">
        <Link to={`/admin/pets/${id}`}><ArrowLeft className="mr-2 h-4 w-4" /> Voltar</Link>
      </Button>

      <Card className="p-8 text-center shadow-soft">
        <h1 className="text-2xl font-bold mb-2">QR Code do pet</h1>
        <p className="text-muted-foreground text-sm mb-6">Imprima e coloque na coleira.</p>
        <div className="mx-auto w-64 h-64 bg-white rounded-2xl border p-4 shadow-glow grid place-items-center">
          {src ? <img src={src} alt="QR Code" className="w-full h-full object-contain" /> : <span className="text-muted-foreground text-sm">Carregando...</span>}
        </div>
        <div className="mt-6 flex flex-wrap justify-center gap-2">
          <Button asChild className="bg-gradient-warm border-0">
            <a href={src} download={`pet-${id}-qr.png`}><Download className="mr-2 h-4 w-4" /> Baixar</a>
          </Button>
          <Button variant="outline" onClick={() => window.print()}>
            <Printer className="mr-2 h-4 w-4" /> Imprimir
          </Button>
        </div>
        <div className="mt-6 flex items-center gap-2 text-xs text-muted-foreground bg-muted rounded-lg p-3">
          <span className="truncate flex-1 text-left font-mono">{scanUrl}</span>
          <Button size="sm" variant="ghost" onClick={copy}>
            {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
          </Button>
        </div>
      </Card>
    </div>
  );
}
