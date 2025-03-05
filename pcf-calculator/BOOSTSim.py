import base64
import json
import os
import redis

from my_function.models.material_dto import MaterialDto

DATEIPFAD = "pfad/zur/datei.geo"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_KEY = "geo_file_base64"

#Änderung_ template Werte gegen tatsächliche Werte aus Geo ersetzt 
material_dicke = MaterialDto.thickness
material_art = MaterialDto.foil_type 


def datei_zu_base64(pfad):
    with open(pfad, "rb") as datei:
        return base64.b64encode(datei.read()).decode("utf-8")

def hole_datei():
    if os.path.exists(DATEIPFAD):
        return datei_zu_base64(DATEIPFAD)
    else:
        try:
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
            data = r.get(REDIS_KEY)
            if data:
                return data
        except Exception as e:
            print(f"Fehler beim Abrufen aus Redis: {e}")
    return None

def parse():
    base64_string = hole_datei()
    
    if base64_string:
        payload = {
            "file_name": os.path.basename(DATEIPFAD),
            "file_content": base64_string,
            "material_dicke": material_dicke,
            "material_art": material_art
        }
        return json.dumps(payload, indent=4) 
        
    return json.dumps({"error": "Keine Datei gefunden!"}, indent=4)

if __name__ == "__main__":
    print(parse())
