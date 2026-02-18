from flask import Flask, request
import requests, base64

app = Flask(__name__)

# ---------------------------------------------------
# CONFIGURATION TTN / TTS
# ---------------------------------------------------
API_KEY = "TA_CLE_API_TTN"  # doit inclure Write downlink application traffic
APP_ID = "ton_application_id"
DEVICE_ID = "ton_device_id"
CLUSTER = "eu1"  # souvent eu1, à vérifier dans TTN

TTS_URL = f"https://{CLUSTER}.cloud.thethings.network/api/v3/as/applications/{APP_ID}/devices/{DEVICE_ID}/down/push"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ---------------------------------------------------
# 1. RECEPTION UPLINK DEPUIS TTN
# ---------------------------------------------------
@app.post("/ttn")
def receive_uplink():
    data = request.json
    print("Uplink reçu :", data)

    # Exemple : envoi automatique d'un downlink
    send_downlink("010203")  # payload hex

    return "OK", 200


# ---------------------------------------------------
# 2. ENVOI DOWNLINK VERS TTN
# ---------------------------------------------------
def send_downlink(hex_payload):
    payload_bytes = bytes.fromhex(hex_payload)
    payload_b64 = base64.b64encode(payload_bytes).decode()

    body = {
        "downlinks": [
            {
                "frm_payload": payload_b64,
                "f_port": 1,
                "priority": "NORMAL"
            }
        ]
    }

    r = requests.post(TTS_URL, json=body, headers=headers)
    print("Réponse downlink :", r.status_code, r.text)


@app.get("/")
def home():
    return "Serveur Webhook TTN opérationnel."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)