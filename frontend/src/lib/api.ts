const BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");

export const getBaseUrl = () => BASE_URL;

// 🔥 FRONT PADRONIZADO COM "id"
export interface Pet {
  id: string;
  pet_name: string;
  owner_name?: string;
  owner_phone?: string;
  notes?: string;
  breed?: string;
  photo_url?: string;
  created_at?: string;
}

export interface Scan {
  id?: string;
  pet_id: string;
  scanned_at?: string;
  location?: string;
  latitude?: number;
  longitude?: number;
  message?: string;
  scanner_phone?: string;
}

// 🔧 função base de request
async function request<T>(path: string, opts: RequestInit = {}): Promise<T> {
  if (!BASE_URL) throw new Error("VITE_API_BASE_URL não configurada no .env");

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(opts.headers as Record<string, string> | undefined),
  };

  const res = await fetch(`${BASE_URL}${path}`, { ...opts, headers });

  if (!res.ok) {
    let msg = `Erro ${res.status}`;

    try {
      const j = await res.json();

      // 🔥 DEBUG COMPLETO (ESSENCIAL)
      console.log("ERRO BACKEND COMPLETO:", j);

      // 🔥 FastAPI padrão
      if (Array.isArray(j.detail)) {
        msg = j.detail
          .map((e: any) => `${e.loc?.join(".")}: ${e.msg}`)
          .join(", ");
      }
      // 🔥 caso venha array direto
      else if (Array.isArray(j)) {
        msg = j.map((e: any) => e.msg).join(", ");
      }
      // 🔥 fallback
      else {
        msg = j.detail || j.message || msg;
      }
    } catch {
      // se nem JSON vier
    }

    throw new Error(msg);
  }

  const ct = res.headers.get("content-type") || "";
  if (ct.includes("application/json")) return res.json();

  // fallback (QR blob, etc)
  // @ts-expect-error
  return res.blob();
}

// 🔥 NORMALIZAÇÃO
function normalizePet(p: any): Pet {
  return {
    id: p.id ?? p.pet_id,
    pet_name: p.pet_name,
    owner_name: p.owner_name,
    owner_phone: p.owner_phone,
    notes: p.notes,
    breed: p.breed,
    photo_url: p.photo_url,
    created_at: p.created_at,
  };
}

export const api = {
  // public
  getPet: async (id: string) => {
    const res = await request<any>(`/admin/pets/${id}`);
    return normalizePet(res);
  },

  postScan: (id: string, payload: Partial<Scan>) =>
    request<Scan>(`/scan/${id}`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // admin
  listPets: async () => {
    const res = await request<any[]>(`/admin/pets`);
    return res.map(normalizePet);
  },

  createPet: async (payload: Partial<Pet>) => {
    const res = await request<any>(`/admin/pets`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    return normalizePet(res);
  },

  deletePet: (id: string) =>
    request<unknown>(`/admin/pets/${id}`, { method: "DELETE" }),

  getScans: (id: string) =>
    request<Scan[]>(`/admin/pets/${id}/scans`),

  // QR
  getQrUrl: (id: string) => `${BASE_URL}/admin/pets/${id}/qr`,

  fetchQrBlob: async (id: string) => {
    const res = await fetch(`${BASE_URL}/admin/pets/${id}/qr`);
    if (!res.ok) throw new Error("Falha ao carregar QR");
    return res.blob();
  },
};
