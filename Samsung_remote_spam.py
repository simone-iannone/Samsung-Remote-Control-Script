# © 2026 Simone Iannone
# Script creato da Simone Iannone — https://github.com/tuo-username/tuo-repo
# Licenza: MIT


import websocket
import json
import base64
import time

# ===========================
# CONFIGURAZIONE (modifica questi parametri)
# ===========================

TV_IP = "*.*.*.*"       # IP della tua TV Samsung
PORT = 8002                    # Porta WebSocket sicura
DEVICE_NAME_RAW = "Test"   # Nome dispositivo (sarà codificato in base64)
VOLUME_UP_COUNT = 100           # Numero di volte da premere Volume Up
DELAY = 0.2                     # Ritardo tra i comandi (in secondi)

# ===========================
# Variabili globali
# ===========================
DEVICE_NAME = base64.b64encode(DEVICE_NAME_RAW.encode("utf-8")).decode("utf-8")
token = None  # Token che la TV fornisce dopo aver premuto "CONSENTI"

# ===========================
# Funzioni
# ===========================

def build_payload(cmd):
    """
    Crea il payload JSON per inviare un comando remoto alla TV.
    
    Parametri:
        cmd (str): Il comando da inviare (es. 'KEY_VOLUP', 'KEY_HOME', ecc.)
    
    Restituisce:
        str: JSON serializzato pronto per l'invio via WebSocket
    """
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
    """
    Callback quando la TV invia un messaggio WebSocket.
    Gestisce l'acquisizione del token e l'invio dei comandi.
    """
    global token
    try:
        data = json.loads(message)
        # Token ricevuto
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
    except Exception as e:
        print(f"[!] Errore parsing messaggio: {e}")

def on_open(ws):
    """
    Callback quando la connessione WebSocket è aperta.
    """
    print("[+] Connesso! Attendi il popup sulla TV e premi CONSENTI...")

# ===========================
# WebSocket URL
# ===========================
ws_url = f"wss://{TV_IP}:{PORT}/api/v2/channels/samsung.remote.control?name={DEVICE_NAME}"

# ===========================
# Avvio WebSocket
# ===========================
ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message)
ws.run_forever(sslopt={"cert_reqs": 0})  # Disabilita la verifica del certificato self-signed
