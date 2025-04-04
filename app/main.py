from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes.categorias import router as categorias_router
from app.api.routes.eventos import router as eventos_router
from app.api.routes.notificaciones import router as notificaciones_router

from app.core.database import init_db

app = FastAPI(
    title= settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Eventos y Calendario"}

app.include_router(categorias_router)
app.include_router(eventos_router)
app.include_router(notificaciones_router)

@app.on_event("startup")
async def startup_event():
    init_db()
    print("Base de datos inicializada correctamente.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
