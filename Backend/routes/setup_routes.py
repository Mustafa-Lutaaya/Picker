from fastapi import APIRouter, HTTPException, Depends, Query, Body # Imports APIRouter to create a modular group of API Routes, HTTPException for raising HTTP error responses
from sqlalchemy.orm import Session # Imports SQLAlchemy ORM database Session class for querying data
from database.database import get_db, engine, Base # Imports database configurations & dependency function to provide a database session for each request
from crud.operations import MarkCRUD, RichtungCRUD, HöheCRUD, BreiteCRUD, OberflächeCRUD, SchlossartCRUD # Imports CRUD operations for database interaction
from schemas.schemas import CreateTür, CreateMark, ReadMark, CreateRichtung, ReadRichtung, CreateHöhe, ReadHöhe, CreateBreite, ReadBreite, CreateOberfläche, ReadOberfläche, CreateSchlossart, ReadSchlossart # Imports Pydantic schemas for request validation and response formatting
from typing import List, Optional # Imports typing for Type hinting support

# Initializes CRUD operation classes
router = APIRouter() # Router configuration for administrative endpoints
mcrud = MarkCRUD() # Initializes Mark class instance to perform DB Operations
rcrud = RichtungCRUD() # Initializes Richtung class instance to perform DB Operations
hcrud = HöheCRUD() # Initializes Höhe class instance to perform DB Operations
bcrud = BreiteCRUD() # Initializes Breite class instance to perform DB Operations
ocrud = OberflächeCRUD() # Initializes Oberfläche class instance to perform DB Operations
scrud = SchlossartCRUD() # Initializes Schlossart class instance to perform DB Operations

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
@router.get("/höhen", response_model=list[ReadHöhe], response_model_exclude_none=True)  
def get_höhen(db: Session = Depends(get_db)):
    try: 
        return hcrud.get_all_höhen(db) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) # 

# Route to get single Höhe by name
@router.get("/höhe/{name}", response_model=ReadHöhe, response_model_exclude_none=True) 
def get_höhe(name: str, db: Session = Depends(get_db)): 
    höhe = hcrud.get_höhe_by_name(db, name)
    if not höhe:
        raise HTTPException(status_code=404, detail="Höhe not found") 
    return höhe

# Route to create a Höhe
@router.post("/höhen", response_model=ReadHöhe, response_model_exclude_none=True) 
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
@router.put("/update-höhe/{name}", response_model=ReadHöhe)
def update_höhe(name: str, höhe: CreateHöhe, db: Session = Depends(get_db)):
    updated = hcrud.update_höhe(db, name, höhe)
    if not updated:
        raise HTTPException(status_code=404, detail="Höhe not found")
    return updated

# Route to delete a Höhe using its name
@router.delete("/delete-höhe/{name}", response_model=ReadHöhe)
def delete_höhe(name: str, db: Session = Depends(get_db)): 
    H = hcrud.delete_höhe(db, name)  
    if not H:
        raise HTTPException(status_code=404, detail="Höhe not found") 
    return H

# Route to delete all Höhen
@router.delete("/höhen", response_model=List[ReadHöhe]) 
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
    
# Oberfläche ROUTES
# Route to get all Oberflächen from the database
@router.get("/oberflächen", response_model=list[ReadOberfläche], response_model_exclude_none=True)  
def get_oberflächen(db: Session = Depends(get_db)):
    try: 
        return ocrud.get_all_oberflächen(db) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) # 

# Route to get a single Oberfläche by name
@router.get("/oberfläche/{name}", response_model=ReadOberfläche, response_model_exclude_none=True) 
def get_oberfläche(name: str, db: Session = Depends(get_db)): 
    oberfläche = ocrud.get_oberfläche_by_name(db, name)
    if not oberfläche:
        raise HTTPException(status_code=404, detail="Oberfläche not found") 
    return oberfläche

# Route to create an Oberfläche
@router.post("/oberflächen", response_model=ReadOberfläche, response_model_exclude_none=True) 
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
@router.put("/update-oberfläche/{name}", response_model=ReadOberfläche)
def update_oberfläche(name: str, oberfläche: CreateOberfläche, db: Session = Depends(get_db)):
    updated = ocrud.update_oberfläche(db, name, oberfläche)
    if not updated:
        raise HTTPException(status_code=404, detail="Oberfläche not found")
    return updated

# Route to delete an Oberfläche using its name
@router.delete("/delete-oberfläche/{name}", response_model=ReadOberfläche)
def delete_oberfläche(name: str, db: Session = Depends(get_db)): 
    O = ocrud.delete_oberfläche(db, name)  
    if not O:
        raise HTTPException(status_code=404, detail="Oberfläche not found") 
    return O

# Route to delete all Oberflächen
@router.delete("/oberflächen", response_model=List[ReadOberfläche]) 
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