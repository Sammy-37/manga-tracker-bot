from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# This creates a file named "manga.db" in your folder
engine = create_engine('sqlite:///manga.db', echo=False)
Base = declarative_base()

#Relationships between various tags
panel_tags = Table('panel_tags', Base.metadata,
    Column('panel_id', Integer, ForeignKey('panels.id'), primary_key=True),
    Column('tag_id',Integer, ForeignKey('tags.id'),primary_key=True)
)

class Arc(Base):
    __tablename__ = 'arcs'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    chapters = relationship("Chapter", back_populates="arc")

class Chapter(Base):
    __tablename__ = 'chapters'
    id = Column(Integer, primary_key=True)
    number = Column(String)
    arc_id = Column(Integer)

    #Links
    arc_id = Column(Integer, ForeignKey('arc.id'))
    arc = relationship("Arc", back_populates="chapters")
    panels = relationship("Panel", back_populates="chapter", cascade="all, delete-orhpans")

class Panel(Base):
   __tablename__ = 'panels'
    id = Column(Integer, primary_key=True)
    
    image_path = Column(String, unique=True)
    
    panel_order = Column(Integer)
    source_page_number = Column(Integer)     
    
    # Links
    chapter_id = Column(Integer, ForeignKey('chapters.id'))
    chapter = relationship("Chapter", back_populates="panels")
    
    tags = relationship("Tag", secondary=panel_tags, back_populates="panels")

class Tags(Base):
    __tablename__= 'tags'
    id = Column(Integer, primary_key = True)

    name = Column(String,unique = True)
    category = Column(String)

    #Link
    panels = relationship("Panel", secondary=panel_tags,back_populates="tags")

# Initialize the DB
Base.metadata.create_all(engine)
