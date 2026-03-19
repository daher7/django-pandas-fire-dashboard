from fastapi import FastAPI
from api_fast.routes import router

app = FastAPI(
    title="Wildfire Data API",
    description="API para Análisis de Incendios Forestales en España con consultas SQL dinámicas",
    version="1.0"
)

# Incluimos el router que definimos en el otro fichero
app.include_router(router)