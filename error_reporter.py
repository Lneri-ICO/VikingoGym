import requests
import traceback
from datetime import datetime

WEBHOOK = "https://discord.com/api/webhooks/1475179699230474515/BUXUUe8fFErtH_WBW3_-P5TNEX8DoDQ0POA2B2ibo14dvBkXUbboxIREnXfWnvbfBj81"


def report_error(error, archivo="desconocido"):

    mensaje = f"""
🚨 ERROR EN VIKINGO GYM

Archivo: {archivo}

Error:
{str(error)}

Traceback:
{traceback.format_exc()}

Hora:
{datetime.now()}
"""

    try:
        requests.post(WEBHOOK, json={"content": mensaje})
    except:
        print("No se pudo enviar error a Discord")