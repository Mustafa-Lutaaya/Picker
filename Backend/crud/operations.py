from sqlalchemy.orm import Session # Imports SQLAlchemy Session for DB operations, and loading strategies for relationships
from sqlalchemy.orm import joinedload
from models.models import Tür, Zarge, Mark, Richtung, Höhe, Breite, Oberfläche, Schlossart, Wandstärk, Zargenart, Kunde, Lager # Imports all SQLAlchemy ORM models
from schemas.schemas import CreateTür, CreateZarge, CreateMark, CreateRichtung, CreateHöhe, CreateBreite, CreateZargenart, CreateWandstärk, CreateOberfläche, CreateSchlossart, CreateKunde, CreateLagerOrt # Imports Pydantic schemas for request validation and response formatting

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

        mark = db.query(Mark).filter(Mark.name == tür.mark_name).first()
        richtung = db.query(Richtung).filter(Richtung.name == tür.richtung_name).first()
        höhe = db.query(Höhe).filter(Höhe.name == tür.hohe_name).first()
        breite = db.query(Breite).filter(Breite.name == tür.breite_name).first()
        oberfläche = db.query(Oberfläche).filter(Oberfläche.name == tür.oberfläche_name).first()
        schlossart = db.query(Schlossart).filter(Schlossart.name == tür.schlossart_name).first()
        lagerort = db.query(Lager).filter(Lager.name == tür.lagerort_name).first()

        if not all([mark, richtung, höhe, breite, oberfläche, schlossart, lagerort]):
            return None
        
        existing = (db.query(Tür)
            .filter(Tür.mark_id == mark.id, Tür.richtung_id == richtung.id,
                Tür.höhe_id == höhe.id, Tür.breite_id == breite.id,
                Tür.oberfläche_id == oberfläche.id,Tür.schlossart_id == schlossart.id, Tür.lagerort_id == lagerort.id
            )
            .first()
        )

        if existing:
            existing.menge += 1
            db.commit()
            db.refresh(existing)
            return existing
        

        new_tür = Tür(
            mark_id=mark.id,
            richtung_id=richtung.id,
            höhe_id=höhe.id,
            breite_id=breite.id,
            oberfläche_id=oberfläche.id,
            schlossart_id=schlossart.id,
            lagerort_id=lagerort.id, 
            description=tür.description,
            gewicht=tür.gewicht
        )

        db.add(new_tür)
        db.commit()
        db.refresh(new_tür) 
        return new_tür 
    
    # Function to get all türen from the database with active database session as parameter
    def get_all_türen(self, db: Session):
            return db.query(Tür).options(
                joinedload(Tür.oberfläche),
                joinedload(Tür.breite),
                joinedload(Tür.schlossart),
                joinedload(Tür.lagerort)
            ).all()

    
    # Function to return a single tür by name with active database session as parameteres
    def get_tür_by_name(self, db: Session, name: str):
        return db.query(Tür).filter(Tür.name == name).first()
    
    # Function to update a Tür from the database identified by name
    def update_tür(self, db: Session, name: str, tür_data: CreateTür):
        T = self.get_tür_by_name(db, name)
       
        if not T:
            return None
        
        mark = db.query(Mark).filter(Mark.name == tür_data.mark_name).first()
        richtung = db.query(Richtung).filter(Richtung.name == tür_data.richtung_name).first()
        höhe = db.query(Höhe).filter(Höhe.name == tür_data.hohe_name).first()
        breite = db.query(Breite).filter(Breite.name == tür_data.breite_name).first()
        oberfläche = db.query(Oberfläche).filter(Oberfläche.name == tür_data.oberfläche_name).first()
        schlossart = db.query(Schlossart).filter(Schlossart.name == tür_data.schlossart_name).first()
        lagerort = db.query(Lager).filter(Lager.name == tür_data.lagerort_name).first()

        if not all([mark, richtung, höhe, breite, oberfläche, schlossart]):
            return None
        
        T.name = tür_data.name
        T.mark = tür_data.mark_name
        T.richtung = tür_data.richtung_name
        T.höhe = tür_data.hohe_name
        T.breite = tür_data.breite_name
        T.oberfläche = tür_data.oberfläche_name
        T.schlossart = tür_data.schlossart_name
        T.lagerort_id = lagerort.id
        T.gewicht = tür_data.gewicht
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
    
# ZARGE OPERATIONS
class ZargeCRUD:
    # Function to create a new Zarge
    def create_zarge(self, db: Session, zarge: CreateZarge):
        mark = db.query(Mark).filter(Mark.name == zarge.mark_name).first()
        richtung = db.query(Richtung).filter(Richtung.name == zarge.richtung_name).first()
        höhe = db.query(Höhe).filter(Höhe.name == zarge.hohe_name).first()
        breite = db.query(Breite).filter(Breite.name == zarge.breite_name).first()
        wandstärke = db.query(Wandstärk).filter(Wandstärk.name == zarge.wandstärke_name).first()
        oberfläche = db.query(Oberfläche).filter(Oberfläche.name == zarge.oberfläche_name).first()
        zargenart = db.query(Zargenart).filter(Zargenart.name == zarge.zargenart_name).first()
        lagerort = db.query(Lager).filter(Lager.name == zarge.lagerort_name).first()

        if not all([mark, richtung, höhe, breite, wandstärke, oberfläche, zargenart, lagerort]):
            return None

        existing = db.query(Zarge).filter(
            Zarge.mark_id==mark.id,
            Zarge.richtung_id==richtung.id,
            Zarge.höhe_id==höhe.id,
            Zarge.breite_id==breite.id,
            Zarge.wandstärke_id==wandstärke.id,
            Zarge.oberfläche_id==oberfläche.id,
            Zarge.zargenart_id==zargenart.id,
            Zarge.lagerort_id==lagerort.id
        ).first()

        if existing:
            existing.menge += 1
            db.commit()
            db.refresh(existing)
            return existing

        new_zarge = Zarge(
            mark_id=mark.id,
            richtung_id=richtung.id,
            höhe_id=höhe.id,
            breite_id=breite.id,
            wandstärke_id=wandstärke.id,
            oberfläche_id=oberfläche.id,
            zargenart_id=zargenart.id,
            lagerort_id=lagerort.id,
            description=zarge.description,
            gewicht=zarge.gewicht
        )
        db.add(new_zarge)
        db.commit()
        db.refresh(new_zarge)
        return new_zarge
    
    # Function to get all Zargen
    def get_all_zargen(self, db: Session):
        return db.query(Zarge).all()
    
    # Function to get a single Zarge by name
    def get_zarge_by_name(self, db: Session, name: str):
        return db.query(Zarge).filter(Zarge.name == name).first()
    
    # Function to update a Zarge
    def update_zarge(self, db: Session, name: str, zarge: CreateZarge):
        Z = self.get_zarge_by_name(db, name)
        if not Z:
            return None
        
        mark = db.query(Mark).filter(Mark.name == zarge.mark_name).first()
        richtung = db.query(Richtung).filter(Richtung.name == zarge.richtung_name).first()
        höhe = db.query(Höhe).filter(Höhe.name == zarge.hohe_name).first()
        breite = db.query(Breite).filter(Breite.name == zarge.breite_name).first()
        wandstärke = db.query(Wandstärk).filter(Wandstärk.name == zarge.wandstärke_name).first()
        oberfläche = db.query(Oberfläche).filter(Oberfläche.name == zarge.oberfläche_name).first()
        zargenart = db.query(Zargenart).filter(Zargenart.name == zarge.zargenart_name).first()
        lagerort = db.query(Lager).filter(Lager.name == zarge.lagerort_name).first()

        if not all([mark, richtung, höhe, breite, wandstärke, oberfläche, zargenart, lagerort]):
            return None
        
        Z.name = zarge.name
        Z.mark = zarge.mark_name
        Z.richtung = zarge.richtung_name
        Z.höhe = zarge.hohe_name
        Z.breite = zarge.breite_name
        Z.wandstärke = zarge.wandstärke_name
        Z.oberfläche = zarge.oberfläche_name
        Z.zargenart = zarge.zargenart_name
        Z.lagerort_id = lagerort.id
        Z.gewicht = Zarge.gewicht
        Z.description = zarge.description

        db.commit()
        db.refresh(Z)

        return Z
    
    # Function to delete a single zarge
    def delete_zarge(self, db: Session, name: str):
        Z = self.get_zarge_by_name(db, name)
        if Z:
            db.delete(Z)
            db.commit()
        return Z
    
    # Function to delete all zargen
    def delete_all_zargen(self, db: Session):
        Z = self.get_all_zargen(db)
        for z in Z:
            db.delete(z)
        db.commit()
        return Z
        
    
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
    
# Wandstärke OPERATIONS
class WandstärkCRUD:
    # Function to create a wandstärk
    def create_wandstärk(self, db: Session, wandstärk: CreateWandstärk):
        new_w = Wandstärk(**wandstärk.model_dump())
        db.add(new_w)
        db.commit()
        db.refresh(new_w)
        return new_w
    
    # Function to get all wandstärken
    def get_all_wandstärken(self, db: Session):
        return db.query(Wandstärk).all()
    
    # Function to get a single wandstärk by name
    def get_wandstärk_by_name(self, db: Session, name: str):
        return db.query(Wandstärk).filter(Wandstärk.name == name).first()
    
    # Function to update a wandstärk
    def update_wandstärk(self, db: Session, name: str, wandstärk_data: CreateWandstärk):
        W = self.get_wandstärk_by_name(db, name)
        if not W:
            return None
        W.name = wandstärk_data.name
        W.nummer = wandstärk_data.nummer
        W.description = wandstärk_data.description
        db.commit()
        db.refresh(W)
        return W
    
    # Function to delete a wandstärk
    def delete_wandstärk(self, db: Session, name: str):
        W = self.get_wandstärk_by_name(db, name)
        if W:
            db.delete(W)
            db.commit()
        return W
    
    # Function to delete all wandstärken
    def delete_all_wandstärken(self, db: Session):
        all_w = self.get_all_wandstärken(db)
        for w in all_w:
            db.delete(w)
        db.commit()
        return all_w

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

# ZARGENART OPERATIONS
class ZargenartCRUD:
    # Function to create a new Zargenart
    def create_zargenart(self, db: Session, zargenart: CreateZargenart):
        new_z = Zargenart(**zargenart.model_dump())
        db.add(new_z)
        db.commit()
        db.refresh(new_z)
        return new_z
    
    # Function to get all zargenarten
    def get_all_zargenarten(self, db: Session):
        return db.query(Zargenart).all()
    
    # Function to get a single zargenart by name
    def get_zargenart_by_name(self, db: Session, name: str):
        return db.query(Zargenart).filter(Zargenart.name == name).first()
    
    # Function to update all zargenarten
    def update_zargenart(self, db: Session, name: str, zargenart_data: CreateZargenart):
        Z = self.get_zargenart_by_name(db, name)
        if not Z:
            return None
        Z.name = zargenart_data.name
        Z.kürzung = zargenart_data.kürzung
        Z.description = zargenart_data.description
        db.commit()
        db.refresh(Z)
        return Z
    
    # Function to delete a zargenart
    def delete_zargenart(self, db: Session, name: str):
        Z = self.get_zargenart_by_name(db, name)
        if Z:
            db.delete(Z)
            db.commit()
        return Z
    
    # Function to delete all zargenarten
    def delete_all_zargenarten(self, db: Session):
        all_z = self.get_all_zargenarten(db)
        for z in all_z:
            db.delete(z)
        db.commit()
        return all_z
    
# Kunden OPERATIONS
class KundeCRUD:
    # Function to create a new Kunde
    def create_kunde(self, db: Session,  kunde: CreateKunde):
        new_kunde = Kunde(**kunde.model_dump())
        db.add(new_kunde)
        db.commit()
        db.refresh(new_kunde) 
        return new_kunde
     
    # Function to get all kunden from the database with active database session as parameter
    def get_all_kunden(self, db: Session):
        return db.query(Kunde).all()
    
    # Function to return a single kunde by name with active database session as parameteres
    def get_kunde_by_name(self, db: Session, name: str):
        return db.query(Kunde).filter(Kunde.name == name).first()
    
    # Function to update a Kunde from the database identified by name
    def update_kunde(self, db: Session, name: str, kunde_data: CreateKunde):
        K = self.get_kunde_by_name(db, name)
       
        if not K:
            return None
        
        K.name = kunde_data.name
        K.adresse = kunde_data.adresse
        K.email = kunde_data.email
        K.tel = kunde_data.tel
        db.commit()
        db.refresh(K)
        return K

    # Function to delete a Kunde from the database identified by name
    def delete_kunde(self, db: Session, name: str):
        K = self.get_kunde_by_name(db, name) 

        if K:
            db.delete(K)
            db.commit()
        return K

    # Function to delete all Kunden
    def delete_all_kunden(self, db: Session):
        K = self.get_all_kunden(db)

        for k in K:
            db.delete(k) 
        db.commit() 
        return K
    
# Kunden OPERATIONS
class LagerOrtCRUD:
    # Function to create a new Lager Ort
    def create_lagerort(self, db: Session,  lagerort: CreateLagerOrt):
        new_lagerort = Lager(**lagerort.model_dump())
        db.add(new_lagerort)
        db.commit()
        db.refresh(new_lagerort) 
        return new_lagerort
    
     # Function to create a Lagerorte in bulk
    def create_lagerort_bulk(self, db: Session, lagerorte: list[CreateLagerOrt]):
        new_orte = []
        for ort in lagerorte:
            new_ort = self.create_lagerort(db, ort)
            new_orte.append(new_ort)
        return new_orte

    # Function to get all Lagerorten from the database with active database session as parameter
    def get_all_lagerorten(self, db: Session):
        return db.query(Lager).all()
    
    # Function to return a single lager ort by name with active database session as parameteres
    def get_lagerort_by_name(self, db: Session, name: str):
        return db.query(Lager).filter(Lager.name == name).first()
    
    # Function to update a Lager Ort from the database identified by name
    def update_lagerort(self, db: Session, name: str, lager_data: CreateLagerOrt):
        L = self.get_lagerort_by_name(db, name)
       
        if not L:
            return None
        
        L.name = lager_data.name

        db.commit()
        db.refresh(L)
        return L

    # Function to delete a Lager Ort from the database identified by name
    def delete_lagerort(self, db: Session, name: str):
        L = self.get_lagerort_by_name(db, name) 

        if L:
            db.delete(L)
            db.commit()
        return L

    # Function to delete all LagerOrten
    def delete_all_lagerorten(self, db: Session):
        L = self.get_all_lagerorten(db)

        for l in L:
            db.delete(l) 
        db.commit() 
        return L