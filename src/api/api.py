from ninja import NinjaAPI

from src.api.readings.router import router as readings_router

api = NinjaAPI(title="Utility Book API", version="1.0.0")

api.add_router("/readings", readings_router)
