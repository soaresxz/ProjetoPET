# 🐾 Pet Tracker — Backend

Backend em FastAPI que recebe localizações de pets via MQTT e expõe uma API REST.

## Fluxo
```
ESP32 (Wokwi) → MQTT (HiveMQ) → FastAPI subscriber → SQLite → API REST
```

## Como rodar

```bash
# 1. Suba o container
docker compose up --build

# 2. Acesse a documentação interativa
http://localhost:8000/docs
```

## Rotas da API

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Health check |
| GET | `/pets` | Lista todos os pets com última localização |
| GET | `/pets/{pet_id}/location` | Última localização do pet |
| GET | `/pets/{pet_id}/history` | Histórico de trajeto (paginado) |
| DELETE | `/pets/{pet_id}/history` | Apaga histórico de um pet |

### Parâmetros de paginação do histórico
- `limit` — quantos registros retornar (padrão: 100, máx: 1000)
- `offset` — pular N registros

## Estrutura
```
backend/
├── app/
│   ├── main.py            # FastAPI + rotas
│   ├── mqtt_subscriber.py # Subscriber MQTT (thread background)
│   ├── database.py        # SQLAlchemy + SQLite
│   ├── models.py          # Tabela locations
│   └── schemas.py         # Schemas Pydantic
├── data/                  # Banco SQLite (gerado automaticamente)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Tópicos MQTT escutados
- `pets/+/location` — localização de qualquer pet

## Payload esperado
```json
{
  "pet_id": "pet_01",
  "lat": -10.947200,
  "lng": -37.073100,
  "speed": 0.8,
  "step": 42
}
```