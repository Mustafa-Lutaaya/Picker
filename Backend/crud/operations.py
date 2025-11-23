from fastapi import Request # Imports FastAPI request object
from sqlalchemy.orm import Session, joinedload, selectinload # Imports SQLAlchemy Session for DB operations, and loading strategies for relationships
from sqlalchemy import select # Imports the select construct for building SQL queries
from models.models import Tür, Mark, Richtung, Höhe, Breite, Oberfläche, Schlossart # Imports all SQLAlchemy ORM models
from schemas.schemas import CreateTür, CreateMark, CreateRichtung, CreateHöhe, CreateBreite, CreateOberfläche, CreateSchlossart # Imports Pydantic schemas for request validation and response formatting
from typing import Dict, Any, List, Union # Adds support for generic dictionary typing

# Mark OPERATIONS
class MarkCRUD:
    def create_mark(self, db: Session,  mark: CreateMark):
        new_mark = Mark(**mark.model_dump())# Creates new instance of CreateMark ORM Model.
        db.add(new_mark)  # Adds new mark object to the currrent database session
        db.commit() # Commits the session to save the new form permanently to the database
        db.refresh(new_mark) # Refreshes the new_mark object to get any updates made by the database like adding the auto generated id
        return new_mark  # Returns newly created mark instance with id
     
    # Function to get all marke from the database with active database session as parameter
    def get_all_marke(self, db: Session):
        return db.query(Mark).all() # Queries the Table, retrieves all rows and returns them as a list of Mark Objects 
    
    # Function to return a single mark by name with active database session as parameteres
    def get_mark_by_name(self, db: Session, name: str):
        return db.query(Mark).filter(Mark.name == name).first() # Queries the Mark Table filtering rows where the name Column matches the input. first() returns the first matching result or None if not exisitng
    
    # Function to update a Mark from the database identified by name
    def update_mark(self, db: Session, name: str, mark_data: CreateMark):
        M = self.get_mark_by_name(db, name) # Retrieves the Mark by name 
       
        if not M:
            return None # Returns none if Mark isnt found
        
        # Proceeds with updating if the Mark exists in the database,
        M.name = mark_data.name
        M.description = mark_data.description
        db.commit() # Commits the transaction to update the Mark data 
        db.refresh(M) # Refreshes the transaction to retrieve new Mark data 
        return M  # Returns the new info Mark instance 

    # Function to delete a Mark from the database identified by name
    def delete_mark(self, db: Session, name: str):
        M = self.get_mark_by_name(db, name) # Retrieves the Mark by name to ensure they exist before attempting deletion
        # Proceeds with deletion if the Mark exists in the database,
        if M:
            db.delete(M) # Marks the Mark for deletion in the current session
            db.commit() # Commit the transaction to remove the Mark from the database permanently
        return M  # Returns the deleted Mark instance or None if not found

    # Function to delete all Marke 
    def delete_all_marke(self, db: Session):
        M = self.get_all_marke(db) # Retrieves the Mark to ensure they exist before attempting deletion
        # Proceeds with deletion if the Mark exist in the database,
        for m in M:
            db.delete(m) # Marks the Mark for deletion in the current session
        db.commit() # Commits the transaction to remove the Mark from the database permanently
        return M  # Returns the deleted Mark instance or None if not found

# TÜR OPERATIONS
class TürCRUD:
    # Function to create a new Tür
    def create_tür(self, db: Session,  tür: CreateTür):
        new_tür = Tür(**tür.model_dump())
        db.add(new_tür)
        db.commit()
        db.refresh(new_tür) 
        return new_tür 
     
    # Function to get all türen from the database with active database session as parameter
    def get_all_türen(self, db: Session):
        return db.query(Tür).all()
    
    # Function to return a single tür by name with active database session as parameteres
    def get_tür_by_name(self, db: Session, name: str):
        return db.query(Tür).filter(Tür.name == name).first()
    
    # Function to update a Tür from the database identified by name
    def update_tür(self, db: Session, name: str, tür_data: CreateTür):
        T = self.get_tür_by_name(db, name)
       
        if not T:
            return None
        
        T.name = tür_data.name
        T.mark = tür_data.mark_name
        T.richtung = tür_data.richtung_name
        T.höhe = tür_data.hohe_name
        T.breite = tür_data.breite_name
        T.oberfläche = tür_data.oberfläche_name
        T.schlossart = tür_data.schlossart_name
        T.description = tür_data.description

        db.commit()
        db.refresh(T)
        return T

    # Function to delete a Tür from the database identified by name
    def delete_tür(self, db: Session, name: str):
        T = self.get_tür_by_name(db, name) 

        if T:
            db.delete(T)
            db.commit()
        return T

    # Function to delete all Türen
    def delete_all_türen(self, db: Session):
        T = self.get_all_türen(db)

        for t in T:
            db.delete(t) 
        db.commit() 
        return T
    
# Richtung OPERATIONS
class RichtungCRUD:
    def create_richtung(self, db: Session,  richtung: CreateRichtung):
        new_richtung = Richtung(**richtung.model_dump())
        db.add(new_richtung)
        db.commit()
        db.refresh(new_richtung) 
        return new_richtung 
     
    # Function to get all richtungen from the database with active database session as parameter
    def get_all_richtungen(self, db: Session):
        return db.query(Richtung).all()
    
    # Function to return a single richtung by name with active database session as parameteres
    def get_richtung_by_name(self, db: Session, name: str):
        return db.query(Richtung).filter(Richtung.name == name).first()
    
    # Function to update a Richtung from the database identified by name
    def update_richtung(self, db: Session, name: str, richtung_data: CreateRichtung):
        R = self.get_richtung_by_name(db, name)
       
        if not R:
            return None
        
        R.name = richtung_data.name
        R.kürzung = richtung_data.kürzung
        R.description = richtung_data.description
        db.commit()
        db.refresh(R)
        return R

    # Function to delete a Richtung from the database identified by name
    def delete_richtung(self, db: Session, name: str):
        R = self.get_richtung_by_name(db, name) 

        if R:
            db.delete(R)
            db.commit()
        return R

    # Function to delete all Richtungen
    def delete_all_richtungen(self, db: Session):
        R = self.get_all_richtungen(db)

        for r in R:
            db.delete(r) 
        db.commit() 
        return R
    
# Höhe OPERATIONS
class HöheCRUD:
    # Function to create a new höhe
    def create_höhe(self, db: Session,  höhe: CreateHöhe):
        new_höhe = Höhe(**höhe.model_dump())
        db.add(new_höhe)
        db.commit()
        db.refresh(new_höhe) 
        return new_höhe 
     
    # Function to get all höhen from the database with active database session as parameter
    def get_all_höhen(self, db: Session):
        return db.query(Höhe).all()
    
    # Function to return a single höhe by name with active database session as parameteres
    def get_höhe_by_name(self, db: Session, name: str):
        return db.query(Höhe).filter(Höhe.name == name).first()
    
    # Function to update a Höhe from the database identified by name
    def update_höhe(self, db: Session, name: str, höhe_data: CreateHöhe):
        H = self.get_höhe_by_name(db, name)
       
        if not H:
            return None
        
        H.name = höhe_data.name
        H.nummer = höhe_data.nummer
        H.description = höhe_data.description
        db.commit()
        db.refresh(H)
        return H

    # Function to delete a Höhe from the database identified by name
    def delete_höhe(self, db: Session, name: str):
        H = self.get_höhe_by_name(db, name) 

        if H:
            db.delete(H)
            db.commit()
        return H

    # Function to delete all Höhen
    def delete_all_höhen(self, db: Session):
        H = self.get_all_höhen(db)

        for h in H:
            db.delete(h) 
        db.commit() 
        return H
    
# Breite OPERATIONS
class BreiteCRUD:
    # Function to create a new Breite
    def create_breite(self, db: Session,  breite: CreateBreite):
        new_breite = Breite(**breite.model_dump())
        db.add(new_breite)
        db.commit()
        db.refresh(new_breite) 
        return new_breite
     
    # Function to get all breiten from the database with active database session as parameter
    def get_all_breiten(self, db: Session):
        return db.query(Breite).all()
    
    # Function to return a single breite by name with active database session as parameteres
    def get_breite_by_name(self, db: Session, name: str):
        return db.query(Breite).filter(Breite.name == name).first()
    
    # Function to update a Breite from the database identified by name
    def update_breite(self, db: Session, name: str, breite_data: CreateBreite):
        B = self.get_breite_by_name(db, name)
       
        if not B:
            return None
        
        B.name = breite_data.name
        B.nummer = breite_data.nummer
        B.description = breite_data.description
        db.commit()
        db.refresh(B)
        return B

    # Function to delete Breite from the database identified by name
    def delete_breite(self, db: Session, name: str):
        B = self.get_breite_by_name(db, name) 

        if B:
            db.delete(B)
            db.commit()
        return B

    # Function to delete all Breiten
    def delete_all_breiten(self, db: Session):
        B = self.get_all_breiten(db)

        for b in B:
            db.delete(b) 
        db.commit() 
        return B

# Oberfläche OPERATIONS
class OberflächeCRUD:
    # Function to create a new Oberfläche
    def create_oberfläche(self, db: Session,  oberfläche: CreateOberfläche):
        new_oberfläche = Oberfläche(**oberfläche.model_dump())
        db.add(new_oberfläche)
        db.commit()
        db.refresh(new_oberfläche) 
        return new_oberfläche
     
    # Function to get all Oberflächen from the database with active database session as parameter
    def get_all_oberflächen(self, db: Session):
        return db.query(Oberfläche).all()
    
    # Function to return a single Oberfläche by name with active database session as parameteres
    def get_oberfläche_by_name(self, db: Session, name: str):
        return db.query(Oberfläche).filter(Oberfläche.name == name).first()
    
    # Function to update an Obefläche from the database identified by name
    def update_oberfläche(self, db: Session, name: str, oberfläche_data: CreateOberfläche):
        O = self.get_oberfläche_by_name(db, name)
       
        if not O:
            return None
        
        O.name = oberfläche_data.name
        O.description = oberfläche_data.description
        db.commit()
        db.refresh(O)
        return O

    # Function to delete an Oberfläche from the database identified by name
    def delete_oberfläche(self, db: Session, name: str):
        O = self.get_oberfläche_by_name(db, name) 

        if O:
            db.delete(O)
            db.commit()
        return O

    # Function to delete all Oberflächen
    def delete_all_oberflächen(self, db: Session):
        O = self.get_all_oberflächen(db)

        for o in O:
            db.delete(o) 
        db.commit() 
        return O

# Schlossart OPERATIONS
class SchlossartCRUD:
    # Function to create a new schlossart
    def create_schlossart(self, db: Session,  sart: CreateSchlossart):
        new_sart = Schlossart(**sart.model_dump())
        db.add(new_sart)
        db.commit()
        db.refresh(new_sart) 
        return new_sart
     
    # Function to get all schlossarten from the database with active database session as parameter
    def get_all_shlossarten(self, db: Session):
        return db.query(Schlossart).all()
    
    # Function to return a single schlossart by name with active database session as parameteres
    def get_schlossart_by_name(self, db: Session, name: str):
        return db.query(Schlossart).filter(Schlossart.name == name).first()
    
    # Function to update a Schlossart from the database identified by name
    def update_schlossart(self, db: Session, name: str, sart_data: CreateSchlossart):
        S = self.get_schlossart_by_name(db, name)
       
        if not S:
            return None
        
        S.name = sart_data.name
        S.kürzung = sart_data.kürzung
        S.description = sart_data.description
        db.commit()
        db.refresh(S)
        return S

    # Function to delete a Schlossart from the database identified by name
    def delete_schlossart(self, db: Session, name: str):
        S = self.get_schlossart_by_name(db, name) 

        if S:
            db.delete(S)
            db.commit()
        return S

    # Function to delete all Schlossarten
    def delete_all_schlossarten(self, db: Session):
        S = self.get_all_shlossarten(db)

        for s in S:
            db.delete(s) 
        db.commit() 
        return S