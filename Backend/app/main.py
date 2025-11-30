from fastapi import FastAPI, Depends  # Imports FastAPI class to create the main app instance
from fastapi.templating import Jinja2Templates  # Imports Jinja2 template support
from fastapi.staticfiles import StaticFiles # Serves Static Files Like CSS, JS & Images
from pathlib import Path # Provides object-oriented file system paths
from routes.setup_routes import router as setup_router # Imports Setup router instance from the setup_routes module and renames it as setup_router
from database.database import engine, Base, get_db
from crud.operations import TürCRUD , ZargeCRUD, KundeCRUD # Imports CRUD operations for database interaction
from sqlalchemy.orm import Session # Imports SQLAlchemy Session for DB operations, and loading strategies for relationships
from utilities.utils import obj_to_dict, format_ware
import random

Base.metadata.create_all(bind=engine)

# Initializes CRUD operation classes
tcrud = TürCRUD() # Initializes Tür class instance to perform DB Operations
zcrud = ZargeCRUD() # Initializes Zarge class instance to perform DB Operations
kcrud = KundeCRUD() # Initializes Kunde class instance to perform DB Operations

app = FastAPI(title="Picker", version="1.0.0") # Creates a FastAPI app instance

app.mount("/static", StaticFiles(directory="static"), name="static") # Serves static files under /static
templates = Jinja2Templates(directory=Path(__file__).parent.parent/"templates") # Setsup templates directory for Jinja2

# Registers routers for different features
app.include_router(setup_router, prefix="/api", tags=["Setup"]) # Adds the Setup router to the main app, prefixing all its routes with "/api" meaning every path inside the api_router will be available under "/api". The tags parameter groups the routes under a Backend tag in Swagger UI

Max_Kunden = 5 
Max_Pallet = 1000 

def generate_ladelist(db: Session):
    türen = tcrud.get_all_türen(db)
    zargen = zcrud.get_all_zargen(db)
    kunden = [obj_to_dict(k) for k in kcrud.get_all_kunden(db)]

    tour_kunden = random.sample(kunden, min(Max_Kunden, len(kunden)))

    ladelist = []

    for kunde in tour_kunden:
        pallet = {"Kunde": kunde, "Waren": [], "Gewicht": 0}
        waren = [(t, "Tür") for t in türen] + [(z, "Zarge") for z in zargen]
        random.shuffle(waren)

        for ware, ware_type in waren:
            formatted_ware = format_ware(ware, ware_type)
            count = formatted_ware["client_count"]
            total_weight = formatted_ware["gewicht"] * count

            if pallet["Gewicht"] + total_weight <= Max_Pallet:
                pallet["Waren"].append(formatted_ware)
                pallet["Gewicht"] += total_weight

        ladelist.append(pallet)

    return ladelist

@app.get("/ladelist")
def get_ladelist(db:Session=Depends(get_db)):
    return generate_ladelist(db)

@app.on_event("startup")
def run_on_startup():
    db:Session = next(get_db())
    try:
        data = generate_ladelist(db)
        print("Ladelist", data)
    finally:
        db.close()