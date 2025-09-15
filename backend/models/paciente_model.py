from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from uuid import UUID # Importar UUID

class Paciente(BaseModel):
    id: Optional[UUID] = None # Usar UUID
    tipo_documento: str
    numero_documento: str
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    fecha_nacimiento: date
    genero: str
    
    # ===================================================================
    # INTEGRACIÓN CON CATÁLOGO OCUPACIONES DANE
    # ===================================================================
    ocupacion_id: Optional[UUID] = Field(
        None,
        description="UUID de la ocupación del catálogo DANE"
    )
    ocupacion_otra_descripcion: Optional[str] = Field(
        None,
        description="Descripción manual si ocupación no está en catálogo DANE"
    )
    
    # Campos de auditoría
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None

class PacienteResponse(Paciente):
    """Modelo de respuesta que incluye datos de ocupación expandidos"""
    
    # Datos de ocupación expandidos (populated por query join)
    ocupacion_codigo_dane: Optional[str] = Field(
        None,
        description="Código DANE de la ocupación (populated)"
    )
    ocupacion_nombre_normalizado: Optional[str] = Field(
        None,
        description="Nombre normalizado de la ocupación (populated)"
    )
    ocupacion_categoria_nivel_1: Optional[str] = Field(
        None,
        description="Categoría nivel 1 de la ocupación (populated)"
    )
    
    model_config = ConfigDict(from_attributes=True)

class PacienteCreate(BaseModel):
    """Modelo para creación de paciente"""
    tipo_documento: str
    numero_documento: str
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    fecha_nacimiento: date
    genero: str
    ocupacion_id: Optional[UUID] = None
    ocupacion_otra_descripcion: Optional[str] = None

class PacienteUpdate(BaseModel):
    """Modelo para actualización de paciente"""
    tipo_documento: Optional[str] = None
    numero_documento: Optional[str] = None
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    genero: Optional[str] = None
    ocupacion_id: Optional[UUID] = None
    ocupacion_otra_descripcion: Optional[str] = None