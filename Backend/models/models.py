from sqlalchemy import Column, Integer, String, ForeignKey # Defines columns and their data types in the database table
from sqlalchemy.orm import relationship  # Used to define relationships between ORM models 
from database.database import Base  # Imports the declarative base from the database module
from sqlalchemy import BigInteger

# MAIN ITEM MANAGEMENT
# ORM Model representing a row in the "Türen" table
class Tür(Base):
    __tablename__ = "Türen" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    mark_id = Column(Integer, ForeignKey("Marke.id"), nullable=False) # Links to the Mark
    richtung_id = Column(Integer, ForeignKey("Richtungen.id"), nullable=False) # Links to the Richtung
    höhe_id = Column(Integer, ForeignKey("Höhen.id"), nullable=False) # Links to the Höhe
    breite_id = Column(Integer, ForeignKey("Breiten.id"), nullable=False) # Links to the Breite
    oberfläche_id = Column(Integer, ForeignKey("Oberflächen.id"), nullable=False) # Links to the Oberfläche
    schlossart_id = Column(Integer, ForeignKey("Schlossarten.id"), nullable=False) # Links to the Schlossart
    menge = Column(Integer, nullable=False, default=1) # Inventory count
    lagerort_id = Column(Integer, ForeignKey("LargerOrte.id"), nullable=False)
    gewicht = Column(Integer, nullable=True)
    description = Column(String, nullable=True) # Adds an optional description
    
    def __repr__(self):
        mark = self.mark.name if self.mark else 'N/A'
        richtung = self.richtung.kürzung if self.richtung else 'N/A'
        höhe = self.höhe.nummer if self.höhe else 'N/A'
        breite = self.breite.nummer if self.breite else 'N/A'
        oberfläche = self.oberfläche.name if self.oberfläche else 'N/A'
        schlossart = self.schlossart.kürzung if self.schlossart else 'N/A'
        return f"Tür({mark} | {richtung} | H:{höhe} | B:{breite} | {oberfläche} | {schlossart})"

    @property
    def mark_name(self):
        return self.mark.name if self.mark else None
    
    @property
    def richtung_name(self):
        return self.richtung.name if self.richtung else None
    
    @property
    def höhe_name(self):
        return self.höhe.name if self.höhe else None
    
    @property
    def breite_name(self):
        return self.breite.name if self.breite else None
    
    @property
    def oberfläche_name(self):
        return self.oberfläche.name if self.oberfläche else None
    
    @property
    def schlossart_name(self):
        return self.schlossart.name if self.schlossart else None
    
    @property
    def lagerort_name(self):
        return self.lagerort.name if self.lagerort else None
    
    # Relationships 
    mark = relationship("Mark", back_populates="türen") # To Mark
    richtung = relationship("Richtung", back_populates="türen") # To Richtung
    höhe = relationship("Höhe", back_populates="türen") # To Höhe
    breite = relationship("Breite", back_populates="türen") # To Breite
    oberfläche = relationship("Oberfläche", back_populates="türen") # To Oberfläche
    schlossart = relationship("Schlossart", back_populates="türen") # To Schlossart
    lagerort = relationship("Lager", back_populates="türen")

# ORM Model representing a row in the "Zargen" table
class Zarge(Base):
    __tablename__ = "Zargen" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    mark_id = Column(Integer, ForeignKey("Marke.id"), nullable=False) # Links to the Mark
    richtung_id = Column(Integer, ForeignKey("Richtungen.id"), nullable=False) # Links to the Richtung
    höhe_id = Column(Integer, ForeignKey("Höhen.id"), nullable=False) # Links to the Höhe
    breite_id = Column(Integer, ForeignKey("Breiten.id"), nullable=False) # Links to the Breite
    wandstärke_id = Column(Integer, ForeignKey("Wandstärken.id"), nullable=False) # Links to the Wandstärke
    oberfläche_id = Column(Integer, ForeignKey("Oberflächen.id"), nullable=False) # Links to the Oberfläche
    zargenart_id = Column(Integer, ForeignKey("Zargenarten.id"), nullable=False) # Links to the Oberfläche
    lagerort_id = Column(Integer, ForeignKey("LargerOrte.id"), nullable=False)
    menge = Column(Integer, nullable=False, default=1) # Inventory count
    gewicht = Column(Integer, nullable=True)
    description = Column(String, nullable=True) # Adds an optional description

    def __repr__(self):
        mark = self.mark.name if self.mark else 'N/A'
        richtung = self.richtung.kürzung if self.richtung else 'N/A'
        höhe = self.höhe.nummer if self.höhe else 'N/A'
        breite = self.breite.nummer if self.breite else 'N/A'
        wandstärke = self.wandstärke.nummer if self.wandstärke else 'N/A'
        zargenart = self.zargenart.kürzung if self.zargenart else 'N/A'
        return f"Zarge({mark} | {richtung} | H:{höhe} | B:{breite} | W:{wandstärke} | {zargenart})"

    @property
    def mark_name(self):
        return self.mark.name if self.mark else None
    
    @property
    def richtung_name(self):
        return self.richtung.name if self.richtung else None
    
    @property
    def höhe_name(self):
        return self.höhe.name if self.höhe else None
    
    @property
    def breite_name(self):
        return self.breite.name if self.breite else None
    
    @property
    def wandstärke_name(self):
        return self.wandstärke.name if self.wandstärke else None
    
    @property
    def oberfläche_name(self):
        return self.oberfläche.name if self.oberfläche else None
    
    @property
    def zargenart_name(self):
        return self.zargenart.name if self.zargenart else None
    
    @property
    def lagerort_name(self):
        return self.lagerort.name if self.lagerort else None
    
    
    # Relationships 
    mark = relationship("Mark", back_populates="zargen") # To Mark
    richtung = relationship("Richtung", back_populates="zargen") # To Richtung
    höhe = relationship("Höhe", back_populates="zargen") # To Höhe
    breite = relationship("Breite", back_populates="zargen") # To Breite
    wandstärke = relationship("Wandstärk", back_populates="zargen") # To Wandstärke
    zargenart= relationship("Zargenart", back_populates="zargen") # To Zargenart
    oberfläche = relationship("Oberfläche", back_populates="zargen") # To Oberfläche
    lagerort = relationship("Lager", back_populates="zargen")



# REQUIRED SPECIFICATIONS MODELS
# ORM Model representing a row in the "Mark" table
class Mark(Base):
    __tablename__ = "Marke" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    name = Column(String, nullable=False, unique=True)  # Adds a Main Name column that stores strings and is required
    description = Column(String, nullable=True) # Adds an optional description
    
    def __repr__(self):
        return f"{self.name}"
    
    türen = relationship("Tür", back_populates="mark", cascade="all, delete-orphan", single_parent=True) # Relationship back to the tür
    zargen = relationship("Zarge", back_populates="mark", cascade="all, delete-orphan", single_parent=True) # Relationship back to the Zarge
    
# ORM Model representing a row in the "Richtung" table
class Richtung(Base):
    __tablename__ = "Richtungen" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    name = Column(String, nullable=False, unique=True)  # Adds a Main Name column that stores strings and is required
    kürzung = Column(String, nullable=False, unique=True)  # Adds a kürzung Name column that stores strings and is required
    description = Column(String, nullable=True) # Adds an optional description
    
    def __repr__(self):
        return f"{self.kürzung}"
    
    türen = relationship("Tür", back_populates="richtung", cascade="all, delete-orphan", single_parent=True) # Relationship back to the tür
    zargen = relationship("Zarge", back_populates="richtung", cascade="all, delete-orphan", single_parent=True) # Relationship back to the Zarge

# ORM Model representing a row in the "Höhe" table
class Höhe(Base):
    __tablename__ = "Höhen" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    name = Column(String, nullable=False, unique=True)  # Adds a Main Name column that stores strings and is required
    nummer = Column(Integer, index=True, nullable=False) # Adds a Number field for the specific höhe
    description = Column(String, nullable=True) # Adds an optional description
    
    def __repr__(self):
        return f"{self.nummer}"
    
    türen = relationship("Tür", back_populates="höhe", cascade="all, delete-orphan", single_parent=True) # Relationship back to the tür
    zargen = relationship("Zarge", back_populates="höhe", cascade="all, delete-orphan", single_parent=True) # Relationship back to the Zarge

# ORM Model representing a row in the "Breite" table
class Breite(Base):
    __tablename__ = "Breiten" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    name = Column(String, nullable=False, unique=True)  # Adds a Main Name column that stores strings and is required
    nummer = Column(Integer, index=True, nullable=False) # Adds a Number field for the specific Breite
    description = Column(String, nullable=True) # Adds an optional description
    
    def __repr__(self):
        return f"{self.nummer}"
    
    türen = relationship("Tür", back_populates="breite", cascade="all, delete-orphan", single_parent=True) # Relationship back to the tür
    zargen = relationship("Zarge", back_populates="breite", cascade="all, delete-orphan", single_parent=True) # Relationship back to the Zarge

# ORM Model representing a row in the "Wandstärk" table
class Wandstärk(Base):
    __tablename__ = "Wandstärken" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    name = Column(String, nullable=False, unique=True)  # Adds a Main Name column that stores strings and is required
    nummer = Column(Integer, index=True, nullable=False) # Adds a Number field for the specific Breite
    description = Column(String, nullable=True) # Adds an optional description
    
    def __repr__(self):
        return f"{self.nummer}"
    
    zargen = relationship("Zarge", back_populates="wandstärke", cascade="all, delete-orphan", single_parent=True) # Relationship back to the Zarge


# ORM Model representing a row in the "Oberfläche" table
class Oberfläche(Base):
    __tablename__ = "Oberflächen" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    name = Column(String, nullable=False, unique=True)  # Adds a Main Name column that stores strings and is required
    description = Column(String, nullable=True) # Adds an optional description
    
    def __repr__(self):
        return f"{self.name}"
    
    türen = relationship("Tür", back_populates="oberfläche", cascade="all, delete-orphan", single_parent=True) # Relationship back to the tür
    zargen = relationship("Zarge", back_populates="oberfläche", cascade="all, delete-orphan", single_parent=True) # Relationship back to the Zarge

# OPTIONAL SPECIFICATIONS
# ORM Model representing a row in the "Schlossart" table
class Schlossart(Base):
    __tablename__ = "Schlossarten" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    name = Column(String, nullable=False, unique=True)  # Adds a Main Name column that stores strings and is required
    kürzung = Column(String, nullable=False, unique=True)  # Adds a kürzung Name column that stores strings and is required
    description = Column(String, nullable=True) # Adds an optional description
    
    def __repr__(self):
        return f"{self.kürzung}"
    
    türen = relationship("Tür", back_populates="schlossart", cascade="all, delete-orphan", single_parent=True) # Relationship back to the tür

# ORM Model representing a row in the "Zargenart" table
class Zargenart(Base):
    __tablename__ = "Zargenarten" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    name = Column(String, nullable=False, unique=True)  # Adds a Main Name column that stores strings and is required
    kürzung = Column(String, nullable=False, unique=True)  # Adds a kürzung Name column that stores strings and is required
    description = Column(String, nullable=True) # Adds an optional description
    
    def __repr__(self):
        return f"{self.kürzung}"
    
    zargen = relationship("Zarge", back_populates="zargenart", cascade="all, delete-orphan", single_parent=True) # Relationship back to the Zarge


# ORM Model representing a row in the "Kunden" table
class Kunde(Base):
    __tablename__ = "Kunden" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    name = Column(String, nullable=False, unique=True)  # Adds a Main Name column that stores strings and is required
    adresse = Column(String, nullable=False, unique=True)  # Adds a Adresse column that stores strings and is required
    tel = Column(BigInteger, index=True, nullable=False) # Adds a Number field for the Telephone Number using BigInteger
    email = Column(String, nullable=True) # Adds an optional description

# ORM Model representing a row in the "Largerort" table
class Lager(Base):
    __tablename__ = "LargerOrte" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    name = Column(String, nullable=False, unique=True)  # Adds a Main Name column that stores strings and is required

    def __repr__(self):
        return f"{self.name}"

    türen = relationship("Tür", back_populates="lagerort")
    zargen = relationship("Zarge", back_populates="lagerort")
