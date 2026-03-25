import websocket
import json
import base64
import time


# ===========================
# CONFIGURAZIONE (modifica questi parametri)
# ===========================

TV_IP = "192.168.0.*"       # IP della TV
PORT = 8002                    # Porta WebSocket sicura
DEVICE_NAME = base64.b64encode(b"Test").decode("utf-8")  # Nome dispositivo in base64
VOLUME_UP_COUNT = 2           # Numero di volte da premere Volume Up
DELAY = 0.1                     # Delay tra un comando e l'altro

token = None


def build_payload(cmd):
    """Crea il payload JSON per il comando remoto"""
    return json.dumps({
        "method": "ms.remote.control",
        "params": {
            "Cmd": "Click",
            "DataOfCmd": cmd,
            "Option": "false",
            "TypeOfRemote": "SendRemoteKey",
            "deviceName": DEVICE_NAME,
            "token": token
        }
    })

def on_message(ws, message):
    global token
    try:
        data = json.loads(message)
        # Ricezione token dalla TV
        if data.get("event") == "ms.channel.connect":
            token = data["data"]["token"]
            print(f"[💀 TOKEN TROVATO 💀] {token}")
            print(f"[>] Invio Volume Up {VOLUME_UP_COUNT} volte...")
            for i in range(VOLUME_UP_COUNT):
                ws.send(build_payload("KEY_VOLUP"))
                print(f"[>] Volume Up {i+1}")
                time.sleep(DELAY)
            print("[✅ Comandi completati!]")
        elif data.get("event") == "ms.error":
            print(f"[!] TV errore: {data['data']['message']}")
        else:
            print(f"[TV RX] {data}")
    except Exception:
        pass

def on_open(ws):
    print("[+] Connesso! Attendi il popup sulla TV e premi CONSENTI...")

# URL WebSocket con porta 8002
ws_url = f"wss://{TV_IP}:{PORT}/api/v2/channels/samsung.remote.control?name={DEVICE_NAME}"
ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message)
ws.run_forever(sslopt={"cert_reqs": 0})
