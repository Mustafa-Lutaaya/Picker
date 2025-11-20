from fastapi import FastAPI  # Imports FastAPI class to create the main app instance
from fastapi.templating import Jinja2Templates  # Imports Jinja2 template support
from fastapi.staticfiles import StaticFiles # Serves Static Files Like CSS, JS & Images
from pathlib import Path # Provides object-oriented file system paths

app = FastAPI(title="Picker", version="1.0.0") # Creates a FastAPI app instance

app.mount("/static", StaticFiles(directory="static"), name="static") # Serves static files under /static
templates = Jinja2Templates(directory=Path(__file__).parent.parent/"templates") # Setsup templates directory for Jinja2