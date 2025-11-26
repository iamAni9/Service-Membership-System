from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import members, plans, subscriptions, attendance

# Creating all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Service Membership API",
    description="Backend API for managing service memberships (gym, coaching center, salon)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Adding CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Including all routers
app.include_router(members.router)
app.include_router(plans.router)
app.include_router(subscriptions.router)
app.include_router(attendance.router)


@app.get("/", tags=["root"])
def read_root():
    return {
        "message": "Service Membership API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}
