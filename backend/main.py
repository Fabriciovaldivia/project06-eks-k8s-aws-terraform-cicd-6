from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from config import settings
from database import engine, get_db, Base
from models import User, Product
from schemas import (
    UserCreate, User as UserSchema,
    ProductCreate, Product as ProductSchema,
    DataResponse
)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# ============= HEALTH CHECK =============
@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint para verificar que el servidor está en línea"""
    return {
        "status": "healthy",
        "service": "Proyecto06 Backend",
        "timestamp": datetime.utcnow().isoformat()
    }

# ============= DATA ENDPOINT =============
@app.get("/api/data", response_model=DataResponse, tags=["Data"])
async def get_data():
    """Obtener datos generales del API"""
    return {
        "message": "Proyecto06 - Backend API con 3 capas",
        "version": settings.API_VERSION,
        "status": "running",
        "timestamp": datetime.utcnow()
    }

# ============= USERS ENDPOINTS =============
@app.post("/api/users", response_model=UserSchema, tags=["Users"])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario"""
    # Verificar si el usuario ya existe
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario o email ya existe"
        )
    
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"Usuario creado: {user.username}")
    return db_user

@app.get("/api/users", response_model=list[UserSchema], tags=["Users"])
async def get_users(db: Session = Depends(get_db)):
    """Obtener todos los usuarios"""
    users = db.query(User).all()
    return users

@app.get("/api/users/{user_id}", response_model=UserSchema, tags=["Users"])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Obtener un usuario por ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# ============= PRODUCTS ENDPOINTS =============
@app.post("/api/products", response_model=ProductSchema, tags=["Products"])
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Crear un nuevo producto"""
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    logger.info(f"Producto creado: {product.name}")
    return db_product

@app.get("/api/products", response_model=list[ProductSchema], tags=["Products"])
async def get_products(db: Session = Depends(get_db)):
    """Obtener todos los productos"""
    products = db.query(Product).filter(Product.is_available == True).all()
    return products

@app.get("/api/products/{product_id}", response_model=ProductSchema, tags=["Products"])
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Obtener un producto por ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@app.put("/api/products/{product_id}", response_model=ProductSchema, tags=["Products"])
async def update_product(
    product_id: int,
    product_update: ProductCreate,
    db: Session = Depends(get_db)
):
    """Actualizar un producto"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    for key, value in product_update.dict().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    logger.info(f"Producto actualizado: {product_id}")
    return db_product

@app.delete("/api/products/{product_id}", tags=["Products"])
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Eliminar un producto (soft delete)"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db_product.is_available = False
    db.commit()
    logger.info(f"Producto eliminado: {product_id}")
    return {"message": "Producto eliminado correctamente"}

# ============= ROOT =============
@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "proyecto": "Proyecto06",
        "arquitectura": "3 capas (Frontend, Backend, Database)",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
