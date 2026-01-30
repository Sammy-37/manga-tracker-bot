from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# This creates a file named "manga.db" in your folder
engine = create_engine('sqlite:///manga.db', echo=False)
Base = declarative_base()

class Arc(Base):
    __tablename__ = 'arcs'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    chapters = relationship("Chapter", back_populates="arc")

class Chapter(Base):
    __tablename__ = 'chapters'
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    arc_id = Column(Integer, ForeignKey('arcs.id'))
    arc = relationship("Arc", back_populates="chapters")
    panels = relationship("Panel", back_populates="chapter")

class Panel(Base):
    __tablename__ = 'panels'
    id = Column(Integer, primary_key=True)
    chapter_id = Column(Integer, ForeignKey('chapters.id'))
    image_path = Column(String) 
    characters = Column(String) 
    scene_type = Column(String) 
    chapter = relationship("Chapter", back_populates="panels")

# Create the tables
Base.metadata.create_all(engine)
