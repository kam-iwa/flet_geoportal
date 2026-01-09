from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class LayerGeometryType(Enum):
    POINT = "Point"
    LINESTRING = "LineString"
    POLYGON = "Polygon"

class LayerSchema(BaseModel):
    id: str
    geometry_type: LayerGeometryType
    geometry_field: str
    added_at: datetime
    added_by: int