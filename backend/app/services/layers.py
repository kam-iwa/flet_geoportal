from sqlalchemy import Column, String, Enum

from backend.app.database import Base
from backend.app.models.layers import LayerGeometryType

class LayerTable(Base): 
    __tablename__ = "layer"
    __table_args__ = {"schema": "metadata"}
    
    id = Column(String, primary_key=True)
    geometry_type = Column(Enum(LayerGeometryType))
    geometry_field = Column(String)
