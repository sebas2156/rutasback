from fastapi import FastAPI
from controllers.historial_rutas_controller import router as historial_router
from controllers.rutas_controller import router as rutas_router
from controllers.usuarios_controller import router as usuarios_router
from controllers.trufis_controller import router as trufis_router

app = FastAPI()

app.include_router(historial_router)
app.include_router(rutas_router)
app.include_router(usuarios_router)
app.include_router(trufis_router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "API funcionando"}
