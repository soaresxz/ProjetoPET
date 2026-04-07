"""
Pet Tracker - ESP32 MicroPython (Wokwi)

Simula coordenadas GPS de um pet e publica via MQTT.
Broker : HiveMQ público (broker.hivemq.com:1883)
Tópico : pets/{PET_ID}/location

Payload JSON publicado:
{
  "pet_id": "pet_01",
  "lat": -10.9472,
  "lng": -37.0731,
  "speed": 0.8,
  "step": 1,
  "timestamp": 3042
}
"""

import network
import time
import utime
import ujson
import urandom
from machine import Pin
from umqtt.simple import MQTTClient

# ─── Configurações WiFi ────────────────────────────────────────────────────────
WIFI_SSID     = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# ─── Configurações MQTT ───────────────────────────────────────────────────────
MQTT_BROKER    = "broker.hivemq.com"
MQTT_PORT      = 1883
MQTT_CLIENT_ID = "esp32_pet_tracker_01"  # Mude para rodar múltiplos pets

# ─── Configurações do Pet ─────────────────────────────────────────────────────
PET_ID      = "pet_01"
MQTT_TOPIC  = f"pets/{PET_ID}/location".encode()
STATUS_TOPIC = f"pets/{PET_ID}/status".encode()
CMD_TOPIC   = f"pets/{PET_ID}/cmd".encode()

# ─── Intervalo de publicação (segundos) ───────────────────────────────────────
PUBLISH_INTERVAL = 3  # RNF01: atualização em até 5 segundos

# ─── Coordenadas base: Aracaju, SE ───────────────────────────────────────────
BASE_LAT =  -10.9472
BASE_LNG =  -37.0731
MAX_OFFSET = 0.002   # ~200m de raio máximo

# ─── LEDs de status ───────────────────────────────────────────────────────────
led_wifi = Pin(2, Pin.OUT)   # Azul  - WiFi conectado
led_mqtt = Pin(4, Pin.OUT)   # Verde - publicando MQTT

# ─── Estado do pet ────────────────────────────────────────────────────────────
current_lat = BASE_LAT
current_lng = BASE_LNG
step_count  = 0

# ─── Cliente MQTT global ──────────────────────────────────────────────────────
mqtt_client = None


def connect_wifi():
    """Conecta à rede WiFi e aguarda até obter IP."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        return wlan

    print(f"Conectando ao WiFi '{WIFI_SSID}'", end="")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    attempts = 0
    while not wlan.isconnected() and attempts < 20:
        time.sleep(0.5)
        print(".", end="")
        attempts += 1

    if wlan.isconnected():
        led_wifi.on()
        print(f" OK! IP: {wlan.ifconfig()[0]}")
    else:
        print(" FALHOU. Reiniciando em 5s...")
        time.sleep(5)
        import machine
        machine.reset()

    return wlan


def on_mqtt_message(topic, msg):
    """Callback chamado ao receber mensagem em tópico assinado."""
    print(f"[CMD recebido] {topic.decode()} → {msg.decode()}")
    # Aqui você pode tratar comandos futuros (ex: mudar intervalo, resetar posição)


def connect_mqtt() -> MQTTClient:
    """Cria e retorna um cliente MQTT conectado ao broker."""
    client = MQTTClient(
        client_id=MQTT_CLIENT_ID,
        server=MQTT_BROKER,
        port=MQTT_PORT,
        keepalive=60,
    )
    client.set_callback(on_mqtt_message)

    print(f"Conectando ao broker '{MQTT_BROKER}'...", end="")
    client.connect()
    led_mqtt.on()
    print(" OK!")

    # Publica status online
    client.publish(STATUS_TOPIC, ujson.dumps({"status": "online"}))

    # Assina tópico de comandos
    client.subscribe(CMD_TOPIC)
    print(f"Inscrito em: {CMD_TOPIC.decode()}")

    return client


def simulate_movement():
    """Atualiza lat/lng simulando uma caminhada aleatória suave."""
    global current_lat, current_lng

    # ~±5 metros por passo (0.00004° ≈ 4.4m)
    delta_lat = (urandom.getrandbits(4) - 7) * 0.000045
    delta_lng = (urandom.getrandbits(4) - 7) * 0.000045

    current_lat += delta_lat
    current_lng += delta_lng

    # Limita ao raio máximo a partir do ponto base
    current_lat = max(BASE_LAT - MAX_OFFSET, min(BASE_LAT + MAX_OFFSET, current_lat))
    current_lng = max(BASE_LNG - MAX_OFFSET, min(BASE_LNG + MAX_OFFSET, current_lng))


def publish_location(client: MQTTClient):
    """Monta o payload e publica no broker MQTT."""
    global step_count
    step_count += 1

    speed = round((urandom.getrandbits(4) % 15) / 10, 1)  # 0.0 a 1.4 m/s

    payload = ujson.dumps({
        "pet_id":    PET_ID,
        "lat":       round(current_lat, 6),
        "lng":       round(current_lng, 6),
        "speed":     speed,
        "step":      step_count,
        "timestamp": utime.ticks_ms() // 1000,
    })

    client.publish(MQTT_TOPIC, payload)

    # Pisca LED para indicar publicação
    led_mqtt.off()
    time.sleep(0.08)
    led_mqtt.on()

    print(f"[step {step_count}] {payload}")


def main():
    global mqtt_client

    print("=" * 40)
    print("   Pet Tracker - ESP32 MicroPython")
    print("=" * 40)
    print(f"Pet ID  : {PET_ID}")
    print(f"Tópico  : {MQTT_TOPIC.decode()}")
    print(f"Broker  : {MQTT_BROKER}:{MQTT_PORT}")
    print("-" * 40)

    connect_wifi()
    mqtt_client = connect_mqtt()

    last_publish = utime.ticks_ms()

    while True:
        try:
            # Verifica mensagens recebidas (não bloqueante)
            mqtt_client.check_msg()

            now = utime.ticks_ms()
            if utime.ticks_diff(now, last_publish) >= PUBLISH_INTERVAL * 1000:
                simulate_movement()
                publish_location(mqtt_client)
                last_publish = now

        except OSError as e:
            print(f"Erro de conexão: {e}. Reconectando...")
            led_mqtt.off()
            time.sleep(2)
            try:
                mqtt_client = connect_mqtt()
            except Exception as ex:
                print(f"Falha ao reconectar: {ex}")
                time.sleep(5)

        time.sleep(0.1)  # Pequeno yield para não travar o loop


main()
