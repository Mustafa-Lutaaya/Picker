import random 

# Helper function to convert objects to dicts and remove SQLAlchemy internal field
def obj_to_dict(obj):
    d = obj.__dict__.copy()
    d.pop("_sa_instance_state", None)
    return d

# Helper function to extract display data from models
def format_ware(ware, ware_type):
    return {
        "lagerort": ware.lagerort_name,
        "mark": ware.mark_name,
        "type": ware_type,
        "richtung": ware.richtung_kürzung if hasattr(ware, 'richtung_kürzung') else ware.richtung.kürzung,
        "höhe": ware.höhe.nummer if hasattr(ware, 'höhe') else ware.höhe_nummer,
        "breite": ware.breite.nummer if hasattr(ware, 'breite') else ware.breite_nummer,
        "nummer": ware.id,
        "oberfläche": ware.oberfläche_name,
        "gewicht": ware.gewicht,
        "client_count": random.randint(1,5),
        "id": ware.id
    }
