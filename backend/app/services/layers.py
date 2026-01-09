from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Enum

from database import Base
from models.layers import LayerGeometryType

class LayerTable(Base): 
    __tablename__ = "layer"
    __table_args__ = {"schema": "metadata"}
    
    id = Column(String, primary_key=True)
    geometry_type = Column(Enum(LayerGeometryType))
    geometry_field = Column(String)
    added_at = Column(DateTime)
    added_by = Column(Integer, ForeignKey("metadata.user.id"))
