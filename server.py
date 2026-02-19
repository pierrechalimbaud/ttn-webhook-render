from flask import Flask, request
import requests, base64

app = Flask(__name__)

# ---------------------------------------------------
# CONFIGURATION TTN / TTS
# ---------------------------------------------------
API_KEY = "NNSXS.3HKTCMSEV3ZHPOGTJBVQTXSTRDE6U7W7342IGPY.LFR2OVBNHL3BZCRLARR7AYIY4JTPJNVJEB6COCSXSRD7F3TALEXQ"  # doit inclure Write downlink application traffic
APP_ID = "my-first-app-chalimbaud"
DEVICE_ID_NIV = "mesure-haut-prof"
DEVICE_ID_IMG = "capt-image-prof"
CLUSTER = "eu1"  # souvent eu1, à vérifier dans TTN


TTS_URL = f"https://{CLUSTER}.cloud.thethings.network/api/v3/as/applications/{APP_ID}/devices/{DEVICE_ID_NIV}/down/push"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ---------------------------------------------------
# 1. RECEPTION UPLINK DEPUIS TTN
# ---------------------------------------------------

changer = True
@app.post("/ttn")
def receive_uplink():
    global changer
    data = request.json
    print("Uplink reçu de ", data['end_DEVICE_ID_NIVs']['DEVICE_ID_NIV'], " :")
    print("Time :",data['received_at'])
    
    if data['end_DEVICE_ID_NIVs']['DEVICE_ID_NIV'] == DEVICE_ID_NIV:
        print("Distance : ",data['uplink_message']['decoded_payload']['Distance'])
        print("Batterie : ",data['uplink_message']['decoded_payload']['Bat'])
        if int(data['uplink_message']['decoded_payload']['Distance']) < 60 :
            print('!!!!! Attention distance < 60cm!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    elif data['end_DEVICE_ID_NIVs']['DEVICE_ID_NIV'] == DEVICE_ID_IMG:
        print("uplink : ",data['uplink_message'])

    # Exemple : envoi automatique d'un downlink
    # if changer :
    #     send_downlink("01000010")  # payload hex
    #     print("reglage période à 16s")
    #     changer = False
    # else :
    #     send_downlink("01000020")  # payload hex
    #     print("reglage période à 32s")
    #     changer = True

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