from pathlib import Path
import geopandas as gpd
import tempfile

from fastapi import UploadFile
from sqlalchemy import Column, String, create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base, engine

class LayerTable(Base): 
    __tablename__ = "layer"
    __table_args__ = {"schema": "metadata"}
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    geometry_field = Column(String)

class LayerService():
    async def get_layers(self, db: AsyncSession) -> list:
        layers = []

        layers_query = await db.execute(text("SELECT l.id, l.name FROM metadata.layer l;"))
        layers_rows = layers_query.fetchall()

        for row in layers_rows:
            layers.append({"id": row[0], "name": row[1]})

        return layers
    
    async def get_layer(self, db: AsyncSession) -> dict:
        return None
    
    async def add_layers(self, db: AsyncSession, token: dict | None, file: UploadFile, layer_name: str) -> tuple[dict, int]:
        if token is None:
            return {"error": f"You are not logged in."}, 401

        if not file.filename.lower().endswith(".gpkg"):
            return {"error": f"Wrong file extension."}, 400
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_path = Path(tmp_dir) / file.filename
            with open(temp_path, "wb") as f:
                f.write(await file.read())

            try:  
                gdf = gpd.read_file(
                    temp_path,
                    engine="pyogrio"
                )
                if gdf.crs.to_epsg() != 4326:
                    gdf = gdf.to_crs(epsg=4326)

                table_name = layer_name.lower().replace(" ", "_")

                async_url = db.get_bind().url
                username = async_url.username
                password = async_url.password
                host = async_url.host
                port = async_url.port
                database = async_url.database
                sync_url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
                sync_engine = create_engine(sync_url)
                
                try:
                    gdf.to_postgis(
                        name=table_name,
                        con=sync_engine,
                        schema="data",
                        if_exists="replace"
                    )
                finally:
                    sync_engine.dispose()
                
                await db.execute(text("""
                                INSERT INTO metadata.layer (id, name)
                                VALUES (:table_name, :layer_name)
                                """),
                                {"table_name": table_name, "layer_name": layer_name}
                )
                await db.commit()
                return {"data": table_name}, 200

            except Exception as e:
                return {"error": f"{e.args}"}, 400