from fastapi import APIRouter, HTTPException, Depends # Imports APIRouter to create a modular group of API Routes, HTTPException for raising HTTP error responses
from sqlalchemy.orm import Session # Imports SQLAlchemy ORM database Session class for querying data
from database.database import get_db # Imports database configurations & dependency function to provide a database session for each request
from crud.operations import MarkCRUD, RichtungCRUD, HöheCRUD, BreiteCRUD, WandstärkCRUD, OberflächeCRUD, SchlossartCRUD, ZargenartCRUD, TürCRUD , ZargeCRUD, KundeCRUD, LagerOrtCRUD # Imports CRUD operations for database interaction
from schemas.schemas import (CreateTür, ReadTür, BulkCreateTüren, CreateZarge, ReadZarge, BulkCreateZargen, 
                            CreateMark, ReadMark, CreateRichtung, ReadRichtung, CreateHöhe, ReadHöhe, CreateBreite, ReadBreite, CreateOberfläche, ReadOberfläche, 
                            CreateWandstärk, ReadWandstärk, CreateSchlossart, ReadSchlossart, CreateZargenart, ReadZargenart, CreateKunde, ReadKunde, CreateLagerOrt, ReadLagerOrt, BulkCreateLagerOrt) # Imports Pydantic schemas for request validation and response formatting
from typing import List # Imports typing for Type hinting support

# Initializes CRUD operation classes
router = APIRouter() # Router configuration for administrative endpoints
tcrud = TürCRUD() # Initializes Tür class instance to perform DB Operations
zcrud = ZargeCRUD() # Initializes Zarge class instance to perform DB Operations
mcrud = MarkCRUD() # Initializes Mark class instance to perform DB Operations
rcrud = RichtungCRUD() # Initializes Richtung class instance to perform DB Operations
hcrud = HöheCRUD() # Initializes Höhe class instance to perform DB Operations
bcrud = BreiteCRUD() # Initializes Breite class instance to perform DB Operations
wcrud = WandstärkCRUD() # Initializes Wandstärk class instance to perform DB Operations
ocrud = OberflächeCRUD() # Initializes Oberfläche class instance to perform DB Operations
scrud = SchlossartCRUD() # Initializes Schlossart class instance to perform DB Operations
zzcrud = ZargenartCRUD() # Initializes Zargenart class instance to perform DB Operations
kcrud = KundeCRUD() # Initializes Kunde class instance to perform DB Operations
lcrud = LagerOrtCRUD() # Initializes Kunde class instance to perform DB Operations

# MARK ROUTES
# Route to get all Marke from the database
@router.get("/marke", response_model=list[ReadMark], response_model_exclude_none=True)  # GET /mark/ returns a list of Marke
def get_marke(db: Session = Depends(get_db)): # Injects DB Session dependency
    try: 
        return mcrud.get_all_marke(db) # Calls Crud function to retrieve all Marke and returns them as a list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) # Handles unexpected errors and returns HTTP 500

# Route to get single Mark by name
@router.get("/marke/{name}", response_model=ReadMark, response_model_exclude_none=True) # GET /mark/{name} fetches one Mark
def get_mark(name: str, db: Session = Depends(get_db)): # Accepts name as path parameter and injects DB session
    mark = mcrud.get_mark_by_name(db, name) # Calls the CRUD function to get the Mark by name
    if not mark:
        raise HTTPException(status_code=404, detail="Mark not found") # Returns 404 if Mark doesn't exist
    return mark # Returns the found mark

# Route to create a mark
@router.post("/marke", response_model=ReadMark, response_model_exclude_none=True) # POST /marke/ with response using pydantic schema
def create_mark(mark: CreateMark, db: Session = Depends(get_db)): # Accepts Mark data and injects Db Session dependency
    exisiting = mcrud.get_mark_by_name(db, mark.name) # Checks if Mark already exists
    if exisiting:
        raise HTTPException(status_code=400, detail="Mark already exists") # Prevents Duplicates
    try:
        new_mark = mcrud.create_mark(db, mark) # Calls crud function to create a new Mark
        return new_mark # Returns the newly created Mark
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Handles any unexpected database or logic errors

# Route to update a Mark using its name
@router.put("/update-mark/{name}", response_model=ReadMark) # PUT /update-mark/{name} updates a Mark
def update_mark(name: str, mark: CreateMark, db: Session = Depends(get_db)): # Accepts name, updated data, and injects DB session
    updated = mcrud.update_mark(db, name, mark)  # Calls CRUD function that finds and updates the Mark using its name
    if not updated:
        raise HTTPException(status_code=404, detail="Mark not found") # Raises error if Mark isnt found
    return updated # Returns the updated Mark

# Route to delete a Mark using its name
@router.delete("/delete-mark/{name}", response_model=ReadMark) # DELETE /delete-amrk/{name} removes a Mark
def delete_mark(name: str, db: Session = Depends(get_db)): # Accepts name as path parameter and injects DB session
    M = mcrud.delete_mark(db, name)  # Calls CRUD delete function that finds and deletes cMark using its name
    if not M:
        raise HTTPException(status_code=404, detail="Mark not found") # Raises error if Mark isnt found
    return M # Returns the deleted Mark

# Route to delete all Marke
@router.delete("/marke", response_model=List[ReadMark]) # DELETE /marke removes all Marke
def delete_all_marke(db: Session = Depends(get_db)): # Injects DB session dependency
    try:
        M = mcrud.get_all_marke(db)  # Retrieves all Marke to check if any exist
        if not M:
            raise HTTPException(status_code=404, detail="No Marke found") # Raises error if no Marke are found
        
        deleted = mcrud.delete_all_marke(db) # Calls CRUD function to delete all Marke
        return deleted # Returns list of deleted Marke
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) # Handles unexpected errors and returns HTTP 500

# TÜREN ROUTES
# Route to get all Türen from the database
@router.get("/tueren", response_model=list[ReadTür], response_model_exclude_none=True)  
def get_türen(db: Session = Depends(get_db)):
    try:
        türen = tcrud.get_all_türen(db)

        result = []
        for t in türen:
            result.append(ReadTür(
                id=t.id,
                menge=t.menge,
                mark_name=t.mark.name,
                richtung_name=t.richtung.name,
                hohe_name=t.höhe.name,
                breite_name=t.breite.name,
                oberfläche_name=t.oberfläche.name,
                schlossart_name=t.schlossart.name,
                lagerort_name=t.lagerort.name,
                gewicht=t.gewicht,
                description=t.description
            ))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) # 

# Route to get a single Tür by name
@router.get("/tuer/{name}", response_model=ReadTür, response_model_exclude_none=True) 
def get_tür(name: str, db: Session = Depends(get_db)): 
    tür = tcrud.get_tür_by_name(db, name)
    if not tür:
        raise HTTPException(status_code=404, detail="Tür not found") 
    return tür

# Route to create a new Tür
@router.post("/tueren", response_model=ReadTür, response_model_exclude_none=True) 
def create_tür(tür: CreateTür, db: Session = Depends(get_db)): 
    try:
        new_tür = tcrud.create_tür(db, tür)

        return ReadTür(
            id=new_tür.id,
            menge=new_tür.menge,
            mark_name=new_tür.mark.name,
            richtung_name=new_tür.richtung.name,
            hohe_name=new_tür.höhe.name,
            breite_name=new_tür.breite.name,
            oberfläche_name=new_tür.oberfläche.name,
            schlossart_name=new_tür.schlossart.name,
            lagerort_name=new_tür.lagerort.name,
            gewicht=new_tür.gewicht,
            description=new_tür.description
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bulk-create", response_model=List[ReadTür])
def bulk_create_türen(data: BulkCreateTüren, db: Session = Depends(get_db)):
    nueue_türen = []

    for tür in data.türen:
        türen = tcrud.create_tür(db, tür)

        if türen:
            nueue_türen.append(türen)

    return [ReadTür(
        id=t.id,
        menge=t.menge,
        mark_name=t.mark.name,
        richtung_name=t.richtung.name,
        hohe_name=t.höhe.name,
        breite_name=t.breite.name,
        oberfläche_name=t.oberfläche.name,
        schlossart_name=t.schlossart.name,
        lagerort_name=t.lagerort.name,
        gewicht=t.gewicht,
        description=t.description)
    for t in nueue_türen
]

# Route to update a Tür using its name
@router.put("/update-tuer/{name}", response_model=ReadTür)
def update_tür(name: str, tür: CreateTür, db: Session = Depends(get_db)):
    updated = tcrud.update_tür(db, name, tür)
    if not updated:
        raise HTTPException(status_code=404, detail="Tür not found")
    return updated

# Route to delete a Tür using its name
@router.delete("/delete-tuer/{name}", response_model=ReadTür)
def delete_tür(name: str, db: Session = Depends(get_db)): 
    T = tcrud.delete_tür(db, name)  
    if not T:
        raise HTTPException(status_code=404, detail="Tür not found") 
    return T

# Route to delete all Türen
@router.delete("/tueren", response_model=List[ReadTür]) 
def delete_all_türen(db: Session = Depends(get_db)):
    try:
        T = tcrud.get_all_türen(db)
        if not T:
            raise HTTPException(status_code=404, detail="No Türen found")
        
        deleted = tcrud.delete_all_türen(db)
        return deleted 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ZARGEN ROUTES
# Route to get all Zargen
@router.get("/zargen", response_model=List[ReadZarge], response_model_exclude_none=True)
def get_zargen(db: Session = Depends(get_db)):
    try:
        zargen = zcrud.get_all_zargen(db)
        result = []
        for z in zargen:
            result.append(ReadZarge(
                id=z.id,
                menge=z.menge,
                mark_name=z.mark.name,
                richtung_name=z.richtung.name,
                hohe_name=z.höhe.name,
                breite_name=z.breite.name,
                wandstärke_name=z.wandstärke.name,
                oberfläche_name=z.oberfläche.name,
                zargenart_name=z.zargenart.name,
                lagerort_name=z.lagerort.name,
                gewicht=z.gewicht,
                description=z.description
            ))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route to get a single Zarge by name
@router.get("/zarge/{name}", response_model=ReadZarge, response_model_exclude_none=True)
def get_zarge(name: str, db: Session = Depends(get_db)):
    zarge = zcrud.get_zarge_by_name(db, name)

    if not zarge:
        raise HTTPException(status_code=404, detail="Zarge not found")
    
    return ReadZarge(
        id=zarge.id,
        menge=zarge.menge,
        mark_name=zarge.mark.name,
        richtung_name=zarge.richtung.name,
        hohe_name=zarge.höhe.name,
        breite_name=zarge.breite.name,
        wandstärke_name=zarge.wandstärke.name,
        oberfläche_name=zarge.oberfläche.name,
        zargenart_name=zarge.zargenart.name,
        lagerort_name=zarge.lagerort.name,
        gewicht=zarge.gewicht,
        description=zarge.description
    )


# Route to create a new Zarge
@router.post("/zargen", response_model=ReadZarge, response_model_exclude_none=True)
def create_zarge(zarge: CreateZarge, db: Session = Depends(get_db)):
    try:
        new_zarge = zcrud.create_zarge(db, zarge)

        return ReadZarge(
            id=new_zarge.id,
            menge=new_zarge.menge,
            mark_name=new_zarge.mark.name,
            richtung_name=new_zarge.richtung.name,
            hohe_name=new_zarge.höhe.name,
            breite_name=new_zarge.breite.name,
            wandstärke_name=new_zarge.wandstärke.name,
            oberfläche_name=new_zarge.oberfläche.name,
            zargenart_name=new_zarge.zargenart.name,
            lagerort_name=new_zarge.lagerort.name,
            gewicht=new_zarge.gewicht,
            description=new_zarge.description
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route to Bulk create Zargen
@router.post("/bulk-create-zargen", response_model=List[ReadZarge])
def bulk_create_zargen(data: BulkCreateZargen, db: Session = Depends(get_db)):
    created_zargen = []

    for zarge in data.zargen:
        z = zcrud.create_zarge(db, zarge)
        if z:
            created_zargen.append(z)

    return [
        ReadZarge(
            id=z.id,
            menge=z.menge,
            mark_name=z.mark.name,
            richtung_name=z.richtung.name,
            hohe_name=z.höhe.name,
            breite_name=z.breite.name,
            wandstärke_name=z.wandstärke.name,
            oberfläche_name=z.oberfläche.name,
            zargenart_name=z.zargenart.name,
            lagerort_name=z.lagerort.name,
            gewicht=z.gewicht,
            description=z.description
        )
        for z in created_zargen
    ]

# Route to update a Zarge by name
@router.put("/update-zarge/{name}", response_model=ReadZarge)
def update_zarge(name: str, zarge: CreateZarge, db: Session = Depends(get_db)):
    updated = zcrud.update_zarge(db, name, zarge)
    if not updated:
        raise HTTPException(status_code=404, detail="Zarge not found")
    return updated


# Route to delete a Zarge by name
@router.delete("/delete-zarge/{name}", response_model=ReadZarge)
def delete_zarge(name: str, db: Session = Depends(get_db)):
    Z = zcrud.delete_zarge(db, name)
    if not Z:
        raise HTTPException(status_code=404, detail="Zarge not found")
    return Z


# Route to delete all Zargen
@router.delete("/zargen", response_model=List[ReadZarge])
def delete_all_zargen(db: Session = Depends(get_db)):
    try:
        all_zargen = zcrud.get_all_zargen(db)
        if not all_zargen:
            raise HTTPException(status_code=404, detail="No Zargen found")
        deleted = zcrud.delete_all_zargen(db)
        return deleted
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# RICHTUNG ROUTES
# Route to get all Richtungen from the database
@router.get("/richtungen", response_model=list[ReadRichtung], response_model_exclude_none=True)  
def get_richtungen(db: Session = Depends(get_db)):
    try: 
        return rcrud.get_all_richtungen(db) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) # 

# Route to get single Richtung by name
@router.get("/richtung/{name}", response_model=ReadRichtung, response_model_exclude_none=True) 
def get_richtung(name: str, db: Session = Depends(get_db)): 
    richtung = rcrud.get_richtung_by_name(db, name)
    if not richtung:
        raise HTTPException(status_code=404, detail="Richtung not found") 
    return richtung

# Route to create a RIchtung
@router.post("/richtungen", response_model=ReadRichtung, response_model_exclude_none=True) 
def create_richtung(richtung: CreateRichtung, db: Session = Depends(get_db)): 
    exisiting = rcrud.get_richtung_by_name(db, richtung.name) 
    if exisiting:
        raise HTTPException(status_code=400, detail="Richtung already exists")
    try:
        new_richtung = rcrud.create_richtung(db, richtung)
        return new_richtung 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

# Route to update a Richtung using its name
@router.put("/update-richtung/{name}", response_model=ReadRichtung)
def update_richtung(name: str, richtung: CreateRichtung, db: Session = Depends(get_db)):
    updated = rcrud.update_richtung(db, name, richtung)
    if not updated:
        raise HTTPException(status_code=404, detail="Richtung not found")
    return updated

# Route to delete a Richtung using its name
@router.delete("/delete-richtung/{name}", response_model=ReadRichtung)
def delete_richtung(name: str, db: Session = Depends(get_db)): 
    R = rcrud.delete_richtung(db, name)  
    if not R:
        raise HTTPException(status_code=404, detail="Richtung not found") 
    return R

# Route to delete all Richtungen
@router.delete("/richtungen", response_model=List[ReadRichtung]) 
def delete_all_richtungen(db: Session = Depends(get_db)):
    try:
        R = rcrud.get_all_richtungen(db)
        if not R:
            raise HTTPException(status_code=404, detail="No Richtungen found")
        
        deleted = rcrud.delete_all_richtungen(db)
        return deleted 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Höhe ROUTES
# Route to get all Höhen from the database
@router.get("/hoehen", response_model=list[ReadHöhe], response_model_exclude_none=True)  
def get_höhen(db: Session = Depends(get_db)):
    try: 
        return hcrud.get_all_höhen(db) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) # 

# Route to get single Höhe by name
@router.get("/hoehe/{name}", response_model=ReadHöhe, response_model_exclude_none=True) 
def get_höhe(name: str, db: Session = Depends(get_db)): 
    höhe = hcrud.get_höhe_by_name(db, name)
    if not höhe:
        raise HTTPException(status_code=404, detail="Höhe not found") 
    return höhe

# Route to create a Höhe
@router.post("/hoehen", response_model=ReadHöhe, response_model_exclude_none=True) 
def create_höhe(höhe: CreateHöhe, db: Session = Depends(get_db)): 
    exisiting = hcrud.get_höhe_by_name(db, höhe.name) 
    if exisiting:
        raise HTTPException(status_code=400, detail="Höhe already exists")
    try:
        new_höhe = hcrud.create_höhe(db, höhe)
        return new_höhe
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

# Route to update a Höhe using its name
@router.put("/update-hoehe/{name}", response_model=ReadHöhe)
def update_höhe(name: str, höhe: CreateHöhe, db: Session = Depends(get_db)):
    updated = hcrud.update_höhe(db, name, höhe)
    if not updated:
        raise HTTPException(status_code=404, detail="Höhe not found")
    return updated

# Route to delete a Höhe using its name
@router.delete("/delete-hoehe/{name}", response_model=ReadHöhe)
def delete_höhe(name: str, db: Session = Depends(get_db)): 
    H = hcrud.delete_höhe(db, name)  
    if not H:
        raise HTTPException(status_code=404, detail="Höhe not found") 
    return H

# Route to delete all Höhen
@router.delete("/hoehen", response_model=List[ReadHöhe]) 
def delete_all_höhen(db: Session = Depends(get_db)):
    try:
        H = hcrud.get_all_höhen(db)
        if not H:
            raise HTTPException(status_code=404, detail="No Höhen found")
        
        deleted = hcrud.delete_all_höhen(db)
        return deleted 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Breite ROUTES
# Route to get all Breiten from the database
@router.get("/breiten", response_model=list[ReadBreite], response_model_exclude_none=True)  
def get_breiten(db: Session = Depends(get_db)):
    try: 
        return bcrud.get_all_breiten(db) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) # 

# Route to get a single Breite by name
@router.get("/breite/{name}", response_model=ReadBreite, response_model_exclude_none=True) 
def get_breite(name: str, db: Session = Depends(get_db)): 
    breite = bcrud.get_breite_by_name(db, name)
    if not breite:
        raise HTTPException(status_code=404, detail="Breite not found") 
    return breite

# Route to create a Breite
@router.post("/breiten", response_model=ReadBreite, response_model_exclude_none=True) 
def create_breite(breite: CreateBreite, db: Session = Depends(get_db)): 
    exisiting = bcrud.get_breite_by_name(db, breite.name) 
    if exisiting:
        raise HTTPException(status_code=400, detail="Breite already exists")
    try:
        new_breite = bcrud.create_breite(db, breite)
        return new_breite
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

# Route to update a Breite using its name
@router.put("/update-breite/{name}", response_model=ReadBreite)
def update_breite(name: str, breite: CreateBreite, db: Session = Depends(get_db)):
    updated = bcrud.update_breite(db, name, breite)
    if not updated:
        raise HTTPException(status_code=404, detail="Breite not found")
    return updated

# Route to delete a Breite using its name
@router.delete("/delete-breite/{name}", response_model=ReadBreite)
def delete_breite(name: str, db: Session = Depends(get_db)): 
    B = bcrud.delete_breite(db, name)  
    if not B:
        raise HTTPException(status_code=404, detail="Breite not found") 
    return B

# Route to delete all Breiten
@router.delete("/breiten", response_model=List[ReadBreite]) 
def delete_all_breiten(db: Session = Depends(get_db)):
    try:
        B = bcrud.get_all_breiten(db)
        if not B:
            raise HTTPException(status_code=404, detail="No Breiten found")
        
        deleted = bcrud.delete_all_breiten(db)
        return deleted 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# WANDSTÄRKE ROUTES
# Route to get all Wandstärke from the database
@router.get("/wandstaerken", response_model=List[ReadWandstärk], response_model_exclude_none=True)
def get_wandstärken(db: Session = Depends(get_db)):
    try:
        return wcrud.get_all_wandstärken(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route to get a single Wandstärk by name
@router.get("/wandstaerk/{name}", response_model=ReadWandstärk, response_model_exclude_none=True)
def get_wandstärk(name: str, db: Session = Depends(get_db)):
    W = wcrud.get_wandstärk_by_name(db, name)
    if not W:
        raise HTTPException(status_code=404, detail="Wandstärk not found")
    return W

# Route to get a create a Wandstärk
@router.post("/wandstaerken", response_model=ReadWandstärk, response_model_exclude_none=True)
def create_wandstärke(wandstärk: CreateWandstärk, db: Session = Depends(get_db)):
    if wcrud.get_wandstärk_by_name(db, wandstärk.name):
        raise HTTPException(status_code=400, detail="Wandstärk already exists")
    return wcrud.create_wandstärk(db, wandstärk)

# Route to get a update a Wandstärk
@router.put("/update-wandstaerk/{name}", response_model=ReadWandstärk)
def update_wandstärke(name: str, wandstärk: CreateWandstärk, db: Session = Depends(get_db)):
    updated = wcrud.update_wandstärk(db, name, wandstärk)
    if not updated:
        raise HTTPException(status_code=404, detail="Wandstärk not found")
    return updated

# Route to get a delete a Wandstärk
@router.delete("/delete-wandstaerke/{name}", response_model=ReadWandstärk)
def delete_wandstärke(name: str, db: Session = Depends(get_db)):
    W = wcrud.delete_wandstärk(db, name)
    if not W:
        raise HTTPException(status_code=404, detail="Wandstärk not found")
    return W

# Route to get a delete all Wandstärken
@router.delete("/wandstaerken", response_model=List[ReadWandstärk])
def delete_all_wandstärken(db: Session = Depends(get_db)):
    deleted = wcrud.delete_all_wandstärken(db)
    if not deleted:
        raise HTTPException(status_code=404, detail="No Wandstärken found")
    return deleted
    
# Oberfläche ROUTES
# Route to get all Oberflächen from the database
@router.get("/oberflaechen", response_model=list[ReadOberfläche], response_model_exclude_none=True)  
def get_oberflächen(db: Session = Depends(get_db)):
    try: 
        return ocrud.get_all_oberflächen(db) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) # 

# Route to get a single Oberfläche by name
@router.get("/oberflaeche/{name}", response_model=ReadOberfläche, response_model_exclude_none=True) 
def get_oberfläche(name: str, db: Session = Depends(get_db)): 
    oberfläche = ocrud.get_oberfläche_by_name(db, name)
    if not oberfläche:
        raise HTTPException(status_code=404, detail="Oberfläche not found") 
    return oberfläche

# Route to create an Oberfläche
@router.post("/oberflaechen", response_model=ReadOberfläche, response_model_exclude_none=True) 
def create_oberfläche(oberfläche: CreateOberfläche, db: Session = Depends(get_db)): 
    exisiting = ocrud.get_oberfläche_by_name(db, oberfläche.name) 
    if exisiting:
        raise HTTPException(status_code=400, detail="oberfläche already exists")
    try:
        new_oberfläche = ocrud.create_oberfläche(db, oberfläche)
        return new_oberfläche
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

# Route to update an Oberfläche using its name
@router.put("/update-oberflaeche/{name}", response_model=ReadOberfläche)
def update_oberfläche(name: str, oberfläche: CreateOberfläche, db: Session = Depends(get_db)):
    updated = ocrud.update_oberfläche(db, name, oberfläche)
    if not updated:
        raise HTTPException(status_code=404, detail="Oberfläche not found")
    return updated

# Route to delete an Oberfläche using its name
@router.delete("/delete-oberflaeche/{name}", response_model=ReadOberfläche)
def delete_oberfläche(name: str, db: Session = Depends(get_db)): 
    O = ocrud.delete_oberfläche(db, name)  
    if not O:
        raise HTTPException(status_code=404, detail="Oberfläche not found") 
    return O

# Route to delete all Oberflächen
@router.delete("/oberflaechen", response_model=List[ReadOberfläche]) 
def delete_all_oberflächen(db: Session = Depends(get_db)):
    try:
        O = ocrud.get_all_oberflächen(db)
        if not O:
            raise HTTPException(status_code=404, detail="No Oberflächen found")
        
        deleted = ocrud.delete_all_oberflächen(db)
        return deleted 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Schlossart ROUTES
# Route to get all Schlossarten from the database
@router.get("/schlossarten", response_model=list[ReadSchlossart], response_model_exclude_none=True)  
def get_schlossarten(db: Session = Depends(get_db)):
    try: 
        return scrud.get_all_shlossarten(db) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) # 

# Route to get a single Schlossart by name
@router.get("/schlossart/{name}", response_model=ReadSchlossart, response_model_exclude_none=True) 
def get_schlossart(name: str, db: Session = Depends(get_db)): 
    sart = scrud.get_schlossart_by_name(db, name)
    if not sart:
        raise HTTPException(status_code=404, detail="Schlossart not found") 
    return sart

# Route to create a Schlossart
@router.post("/schlossarten", response_model=ReadSchlossart, response_model_exclude_none=True) 
def create_schlossart(sart: CreateSchlossart, db: Session = Depends(get_db)): 
    exisiting = scrud.get_schlossart_by_name(db, sart.name) 
    if exisiting:
        raise HTTPException(status_code=400, detail="Schlossart already exists")
    try:
        new_sart = scrud.create_schlossart(db, sart)
        return new_sart
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

# Route to update a Schlossart using its name
@router.put("/update-schlossart/{name}", response_model=ReadSchlossart)
def update_schlossart(name: str, sart: CreateSchlossart, db: Session = Depends(get_db)):
    updated = scrud.update_schlossart(db, name, sart)
    if not updated:
        raise HTTPException(status_code=404, detail="Schlossart not found")
    return updated

# Route to delete a Schlossart using its name
@router.delete("/delete-schlossart/{name}", response_model=ReadSchlossart)
def delete_schlossart(name: str, db: Session = Depends(get_db)): 
    S = scrud.delete_schlossart(db, name)  
    if not S:
        raise HTTPException(status_code=404, detail="Schlossart not found") 
    return S

# Route to delete all Schlossarten
@router.delete("/schlossarten", response_model=List[ReadSchlossart]) 
def delete_all_schlossarten(db: Session = Depends(get_db)):
    try:
        S = scrud.get_all_shlossarten(db)
        if not S:
            raise HTTPException(status_code=404, detail="No Schlossarten found")
        
        deleted = scrud.delete_all_schlossarten(db)
        return deleted 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# ZARGENART ROUTES
# Route to get all zargenarten
@router.get("/zargenarten", response_model=List[ReadZargenart], response_model_exclude_none=True)
def get_zargenarten(db: Session = Depends(get_db)):
    try:
        return zzcrud.get_all_zargenarten(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route to get a zargenart
@router.get("/zargenart/{name}", response_model=ReadZargenart, response_model_exclude_none=True)
def get_zargenart(name: str, db: Session = Depends(get_db)):
    Z = zzcrud.get_zargenart_by_name(db, name)
    if not Z:
        raise HTTPException(status_code=404, detail="Zargenart not found")
    return Z

# Route to create a zargenart
@router.post("/zargenarten", response_model=ReadZargenart, response_model_exclude_none=True)
def create_zargenart(zargenart: CreateZargenart, db: Session = Depends(get_db)):
    if zzcrud.get_zargenart_by_name(db, zargenart.name):
        raise HTTPException(status_code=400, detail="Zargenart already exists")
    return zzcrud.create_zargenart(db, zargenart)

# Route to update a zargenart
@router.put("/update-zargenart/{name}", response_model=ReadZargenart)
def update_zargenart(name: str, zargenart: CreateZargenart, db: Session = Depends(get_db)):
    updated = zzcrud.update_zargenart(db, name, zargenart)
    if not updated:
        raise HTTPException(status_code=404, detail="Zargenart not found")
    return updated

# Route to delete a zargenart
@router.delete("/delete-zargenart/{name}", response_model=ReadZargenart)
def delete_zargenart(name: str, db: Session = Depends(get_db)):
    Z = zzcrud.delete_zargenart(db, name)
    if not Z:
        raise HTTPException(status_code=404, detail="Zargenart not found")
    return Z

# Route to delete all zargenarten
@router.delete("/zargenarten", response_model=List[ReadZargenart])
def delete_all_zargenarten(db: Session = Depends(get_db)):
    deleted = zzcrud.delete_all_zargenarten(db)
    if not deleted:
        raise HTTPException(status_code=404, detail="No Zargenarten found")
    return deleted
    
# Kunde ROUTES
# Route to get all Kunden from the database
@router.get("/kunden", response_model=list[ReadKunde], response_model_exclude_none=True)  
def get_kunden(db: Session = Depends(get_db)):
    try: 
        return kcrud.get_all_kunden(db) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) # 

# Route to get a single Kunde by name
@router.get("/kunde/{name}", response_model=ReadKunde, response_model_exclude_none=True) 
def get_kunde(name: str, db: Session = Depends(get_db)): 
    kunde = kcrud.get_kunde_by_name(db, name)
    if not kunde:
        raise HTTPException(status_code=404, detail="Kunde not found") 
    return kunde

# Route to create a Kunde
@router.post("/kunden", response_model=ReadKunde, response_model_exclude_none=True) 
def create_kunde(kunde: CreateKunde, db: Session = Depends(get_db)): 
    exisiting = kcrud.get_kunde_by_name(db, kunde.name) 
    if exisiting:
        raise HTTPException(status_code=400, detail="Kunde already exists")
    try:
        new_kunde = kcrud.create_kunde(db, kunde)
        return new_kunde
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

# Route to update a Kunde using their name
@router.put("/update-kunde/{name}", response_model=ReadKunde)
def update_kunde(name: str, kunde: CreateKunde, db: Session = Depends(get_db)):
    updated = kcrud.update_kunde(db, name, kunde)
    if not updated:
        raise HTTPException(status_code=404, detail="Kunde not found")
    return updated

# Route to delete a Kunde using their name
@router.delete("/delete-kunde/{name}", response_model=ReadKunde)
def delete_kunde(name: str, db: Session = Depends(get_db)): 
    K = kcrud.delete_kunde(db, name)  
    if not K:
        raise HTTPException(status_code=404, detail="Kunde not found") 
    return K

# Route to delete all Kunden
@router.delete("/Kunden", response_model=List[ReadKunde]) 
def delete_all_kunden(db: Session = Depends(get_db)):
    try:
        K = kcrud.get_all_kunden(db)
        if not K:
            raise HTTPException(status_code=404, detail="No Kunden found")
        
        deleted = kcrud.delete_all_kunden(db)
        return deleted 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Largerorte ROUTES
# Route to get all Lagerorte from the database
@router.get("/lagerorte", response_model=list[ReadLagerOrt], response_model_exclude_none=True)  
def get_largerorte(db: Session = Depends(get_db)):
    try: 
        return lcrud.get_all_lagerorten(db) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) # 

# Route to get a single Largerort by name
@router.get("/largerort/{name}", response_model=ReadLagerOrt, response_model_exclude_none=True) 
def get_largerort(name: str, db: Session = Depends(get_db)): 
    ort = lcrud.get_lagerort_by_name(db, name)
    if not ort:
        raise HTTPException(status_code=404, detail="Largerort not found") 
    return ort

# Route to create a Largerort
@router.post("/largerorte", response_model=ReadLagerOrt, response_model_exclude_none=True) 
def create_lagerort(ort: CreateLagerOrt, db: Session = Depends(get_db)): 
    exisiting = lcrud.get_lagerort_by_name(db, ort.name) 
    if exisiting:
        raise HTTPException(status_code=400, detail="Lagerort already exists")
    try:
        new_ort = lcrud.create_lagerort(db, ort)
        return new_ort
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

# Route to update a Lagerort using their name
@router.put("/update-lagerort/{name}", response_model=ReadLagerOrt)
def update_lagerort(name: str, ort: CreateLagerOrt, db: Session = Depends(get_db)):
    updated = lcrud.update_lagerort(db, name, ort)
    if not updated:
        raise HTTPException(status_code=404, detail="Lagerort not found")
    return updated

# Route to delete a Lagerort using their name
@router.delete("/delete-lagerort/{name}", response_model=ReadLagerOrt)
def delete_lagerort(name: str, db: Session = Depends(get_db)): 
    L = lcrud.delete_lagerort(db, name)  
    if not L:
        raise HTTPException(status_code=404, detail="Lagerort not found") 
    return L

# Route to delete all Kunden
@router.delete("/lagerorten", response_model=List[ReadLagerOrt]) 
def delete_all_lagerorten(db: Session = Depends(get_db)):
    try:
        L = lcrud.get_all_lagerorten(db)
        if not L:
            raise HTTPException(status_code=404, detail="No Lagerorten found")
        
        deleted = lcrud.delete_all_lagerorten(db)
        return deleted 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/lagerorte/bulk", response_model=list[ReadLagerOrt])
def create_lagerorte_bulk(data: BulkCreateLagerOrt, db: Session = Depends(get_db)):
    try:
        new_lagerorte = []

        for lagerort in data.lagerorte:

            existing = lcrud.get_lagerort_by_name(db, lagerort.name)
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail=f"Lagerort '{lagerort.name}' already exists."
                )

            created = lcrud.create_lagerort(db, lagerort)
            new_lagerorte.append(created)

        return new_lagerorte

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

