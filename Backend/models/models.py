from sqlalchemy import Column, Integer, String, ForeignKey # Defines columns and their data types in the database table
from sqlalchemy.orm import relationship  # Used to define relationships between ORM models 
from database.database import Base  # Imports the declarative base from the database module

# MAIN ITEM MANAGEMENT
# ORM Model representing a row in the "Türen" table
class Tür(Base):
    __tablename__ = "Türen" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    mark_id = Column(Integer, ForeignKey("Marke.id"), nullable=False) # Links to the Mark
    richtung_id = Column(Integer, ForeignKey("Richtung.id"), nullable=False) # Links to the Richtung
    höhe_id = Column(Integer, ForeignKey("Höhe.id"), nullable=False) # Links to the Höhe
    breite_id = Column(Integer, ForeignKey("Breite.id"), nullable=False) # Links to the Breite
    oberfläche_id = Column(Integer, ForeignKey("Oberfläche.id"), nullable=False) # Links to the Oberfläche
    schlossart_id = Column(Integer, ForeignKey("Schlossart.id"), nullable=False) # Links to the Schlossart
    description = Column(String, nullable=True) # Adds an optional description

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
    
    # Relationships 
    mark = relationship("Mark", back_populates="türen") # To Mark
    richtung = relationship("Richtung", back_populates="türen") # To Richtung
    höhe = relationship("Höhe", back_populates="türen") # To Höhe
    breite = relationship("Breite", back_populates="türen") # To Breite
    oberfläche = relationship("Oberfläche", back_populates="türen") # To Oberfläche
    schlossart = relationship("Schlossart", back_populates="türen") # To Schlossart

# REQUIRED SPECIFICATIONS MODELS
# ORM Model representing a row in the "Mark" table
class Mark(Base):
    __tablename__ = "Mark" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    name = Column(String, nullable=False, unique=True)  # Adds a Main Name column that stores strings and is required
    description = Column(String, nullable=True) # Adds an optional description
    
    türen = relationship("Tür", back_populates="mark", cascade="all, delete-orphan", single_parent=True) # Relationship back to the tür

# ORM Model representing a row in the "Richtung" table
class Richtung(Base):
    __tablename__ = "Richtung" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    name = Column(String, nullable=False, unique=True)  # Adds a Main Name column that stores strings and is required
    kürzung = Column(String, nullable=False, unique=True)  # Adds a kürzung Name column that stores strings and is required
    description = Column(String, nullable=True) # Adds an optional description
    
    türen = relationship("Tür", back_populates="richtung", cascade="all, delete-orphan", single_parent=True) # Relationship back to the tür

# ORM Model representing a row in the "Höhe" table
class Höhe(Base):
    __tablename__ = "Höhe" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    name = Column(String, nullable=False, unique=True)  # Adds a Main Name column that stores strings and is required
    nummer = Column(Integer, index=True, nullable=False) # Adds a Number field for the specific höhe
    description = Column(String, nullable=True) # Adds an optional description
    
    türen = relationship("Tür", back_populates="höhe", cascade="all, delete-orphan", single_parent=True) # Relationship back to the tür

# ORM Model representing a row in the "Breite" table
class Breite(Base):
    __tablename__ = "Breite" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    name = Column(String, nullable=False, unique=True)  # Adds a Main Name column that stores strings and is required
    nummer = Column(Integer, index=True, nullable=False) # Adds a Number field for the specific Breite
    description = Column(String, nullable=True) # Adds an optional description
    
    türen = relationship("Tür", back_populates="breite", cascade="all, delete-orphan", single_parent=True) # Relationship back to the tür

# ORM Model representing a row in the "Oberfläche" table
class Oberfläche(Base):
    __tablename__ = "Oberfläche" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    name = Column(String, nullable=False, unique=True)  # Adds a Main Name column that stores strings and is required
    description = Column(String, nullable=True) # Adds an optional description
    
    türen = relationship("Tür", back_populates="öberflache", cascade="all, delete-orphan", single_parent=True) # Relationship back to the tür

# OPTIONAL SPECIFICATIONS
# ORM Model representing a row in the "Schlossart" table
class Schlossart(Base):
    __tablename__ = "Schlossart" # Table name in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key marks the id column as a unique identifier while index:True creates an index for faster searches
    name = Column(String, nullable=False, unique=True)  # Adds a Main Name column that stores strings and is required
    kürzung = Column(String, nullable=False, unique=True)  # Adds a kürzung Name column that stores strings and is required
    description = Column(String, nullable=True) # Adds an optional description
    
    türen = relationship("Tür", back_populates="schlossart", cascade="all, delete-orphan", single_parent=True) # Relationship back to the tür