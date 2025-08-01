from fastapi import FastAPI
from routes.brand_routes import router as brand_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

#middleware 
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React app will run on port 3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount your brand-related routes
app.include_router(brand_router)

#uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
