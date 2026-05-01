# 🐾 Pet QR Tracker

Sistema de monitoramento de pets via QR code na coleira.
Quando alguém encontra o pet e escaneia o QR, o dono recebe um SMS com a localização de quem achou.

## Fluxo completo

```
Coleira com QR → celular de quem achou → pede GPS → FastAPI → SMS Twilio → dono
```

## Configuração

### 1. Crie o arquivo `.env`
```bash
cp .env.example .env
```
Preencha com suas credenciais do [painel Twilio](https://console.twilio.com):
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=seu_token
TWILIO_FROM_NUMBER=+15551234567
BASE_URL=http://localhost:8000
```

### 2. Suba o container
```bash
docker compose up --build
```

### 3. Acesse a documentação
```
http://localhost:8000/docs
```

## Rotas da API

### Públicas (usadas pelo celular de quem achou o pet)
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/pet/{pet_id}` | Página com dados do pet + botão de localização |
| POST | `/scan/{pet_id}` | Envia localização → dispara SMS ao dono |

### Admin (gerenciamento)
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/admin/pets` | Cadastra um pet |
| GET | `/admin/pets` | Lista todos os pets |
| GET | `/admin/pets/{pet_id}/qr` | Baixa o QR code PNG para imprimir |
| GET | `/admin/pets/{pet_id}/scans` | Histórico de escaneamentos |
| DELETE | `/admin/pets/{pet_id}` | Remove um pet |

## Como cadastrar um pet (exemplo)

```bash
curl -X POST http://localhost:8000/admin/pets \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "pet_01",
    "pet_name": "Rex",
    "owner_name": "João Silva",
    "owner_phone": "+5579999999999"
  }'
```

## Como gerar o QR code para imprimir

```
GET http://localhost:8000/admin/pets/pet_01/qr
```
Baixa um arquivo `qr_pet_01.png` pronto para imprimir e colocar na coleira.

## SMS recebido pelo dono

```
🐾 Seu pet Rex foi encontrado!
Alguém escaneou a coleira agora.
Localização de quem achou:
https://maps.google.com/?q=-10.947200,-37.073100
```

## Estrutura do projeto

```
pet-qr/
├── app/
│   ├── main.py            ← FastAPI + todas as rotas
│   ├── sms.py             ← Integração Twilio
│   ├── qr_service.py      ← Geração do QR code
│   ├── database.py        ← SQLite via SQLAlchemy
│   ├── models.py          ← Tabelas: pets, scans
│   ├── schemas.py         ← Schemas Pydantic
│   └── templates/
│       └── pet_scan.html  ← Página exibida ao escanear
├── data/                  ← Banco SQLite (gerado automaticamente)
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Observação sobre geolocalização

O navegador só permite acesso ao GPS em páginas servidas via **HTTPS**.
Em desenvolvimento local (`localhost`) funciona normalmente.
Em produção, use um domínio com certificado SSL (ex: via Nginx + Let's Encrypt).
```