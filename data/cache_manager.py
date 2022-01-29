import json

VERIFIER_DATA = {}
WEAKNESS_DATA = {}
TYPE_DATA = {}

async def Cache_Data():

    """Caches the static data for faster access"""

    global VERIFIER_DATA, WEAKNESS_DATA, TYPE_DATA

    with open("data/data.json", "r") as f_out:
        data = json.loads(f_out.read())
        VERIFIER_DATA = data["verifier"]

    with open("data/weakness_data.json", "r") as f_out:
        data = json.loads(f_out.read())
        WEAKNESS_DATA = data

    with open("data/type_data.json", "r") as f_out:
        data = json.loads(f_out.read())
        TYPE_DATA = data
