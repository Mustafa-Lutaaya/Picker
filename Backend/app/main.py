from fastapi import FastAPI  # Imports FastAPI class to create the main app instance
from fastapi.templating import Jinja2Templates  # Imports Jinja2 template support
from fastapi.staticfiles import StaticFiles # Serves Static Files Like CSS, JS & Images
from pathlib import Path # Provides object-oriented file system paths
from routes.setup_routes import router as setup_router # Imports Setup router instance from the setup_routes module and renames it as setup_router
from database.database import engine, Base

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Picker", version="1.0.0") # Creates a FastAPI app instance

app.mount("/static", StaticFiles(directory="static"), name="static") # Serves static files under /static
templates = Jinja2Templates(directory=Path(__file__).parent.parent/"templates") # Setsup templates directory for Jinja2

# Registers routers for different features
app.include_router(setup_router, prefix="/api", tags=["Setup"]) # Adds the Setup router to the main app, prefixing all its routes with "/api" meaning every path inside the api_router will be available under "/api". The tags parameter groups the routes under a Backend tag in Swagger UI