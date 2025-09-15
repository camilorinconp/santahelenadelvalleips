# =============================================================================
# Error Handling Centralizado - IPS Santa Helena del Valle
# Middleware para manejo unificado de errores y logging estructurado
# =============================================================================

import logging
import traceback
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError

# =============================================================================
# CONFIGURACIÓN LOGGING ESTRUCTURADO
# =============================================================================

class StructuredLogger:
    """Logger estructurado para trazabilidad completa."""
    
    def __init__(self, name: str = "ips_santa_helena"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Handler para consola con formato estructurado
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s'
            )
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
    
    def info(self, message: str, **kwargs):
        """Log de información con contexto."""
        extra_data = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
        self.logger.info(f"{message} | {extra_data}" if extra_data else message)
    
    def error(self, message: str, **kwargs):
        """Log de error con contexto."""
        extra_data = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
        self.logger.error(f"{message} | {extra_data}" if extra_data else message)
    
    def warning(self, message: str, **kwargs):
        """Log de warning con contexto."""
        extra_data = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
        self.logger.warning(f"{message} | {extra_data}" if extra_data else message)

# Logger global
logger = StructuredLogger()

# =============================================================================
# MODELOS DE RESPUESTA ERROR ESTANDARIZADOS
# =============================================================================

class ErrorResponse:
    """Respuestas de error estandarizadas."""
    
    @staticmethod
    def create_error_response(
        status_code: int,
        error_type: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Crear respuesta de error estandarizada."""
        
        return {
            "error": {
                "type": error_type,
                "message": message,
                "status_code": status_code,
                "timestamp": datetime.now().isoformat(),
                "correlation_id": correlation_id or str(uuid.uuid4())[:8],
                "details": details or {}
            },
            "success": False,
            "data": None
        }

# =============================================================================
# EXCEPTION HANDLERS PERSONALIZADOS
# =============================================================================

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handler para HTTPException estándar."""
    
    correlation_id = str(uuid.uuid4())[:8]
    
    # Log del error
    logger.error(
        f"HTTP Exception: {exc.detail}",
        status_code=exc.status_code,
        path=request.url.path,
        method=request.method,
        correlation_id=correlation_id
    )
    
    # Mapear tipos de error comunes
    error_type_mapping = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED", 
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        422: "VALIDATION_ERROR",
        500: "INTERNAL_SERVER_ERROR"
    }
    
    error_response = ErrorResponse.create_error_response(
        status_code=exc.status_code,
        error_type=error_type_mapping.get(exc.status_code, "HTTP_ERROR"),
        message=exc.detail,
        correlation_id=correlation_id
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handler para errores de validación Pydantic."""
    
    correlation_id = str(uuid.uuid4())[:8]
    
    # Procesar errores de validación
    validation_errors = []
    for error in exc.errors():
        validation_errors.append({
            "field": " -> ".join([str(loc) for loc in error["loc"]]),
            "message": error["msg"],
            "type": error["type"],
            "input": error.get("input", "N/A")
        })
    
    # Log detallado
    logger.error(
        f"Validation Error: {len(validation_errors)} field(s) failed validation",
        path=request.url.path,
        method=request.method,
        errors=validation_errors,
        correlation_id=correlation_id
    )
    
    error_response = ErrorResponse.create_error_response(
        status_code=422,
        error_type="VALIDATION_ERROR",
        message=f"Errores de validación en {len(validation_errors)} campo(s)",
        details={
            "validation_errors": validation_errors,
            "total_errors": len(validation_errors)
        },
        correlation_id=correlation_id
    )
    
    return JSONResponse(
        status_code=422,
        content=error_response
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler para excepciones generales no capturadas."""
    
    correlation_id = str(uuid.uuid4())[:8]
    
    # Log completo del error con traceback
    logger.error(
        f"Unhandled Exception: {str(exc)}",
        exception_type=type(exc).__name__,
        path=request.url.path,
        method=request.method,
        traceback=traceback.format_exc(),
        correlation_id=correlation_id
    )
    
    # En desarrollo, incluir más detalles
    import os
    is_development = os.getenv("ENVIRONMENT", "development") == "development"
    
    error_details = {}
    if is_development:
        error_details = {
            "exception_type": type(exc).__name__,
            "traceback": traceback.format_exc().split('\n')
        }
    
    error_response = ErrorResponse.create_error_response(
        status_code=500,
        error_type="INTERNAL_SERVER_ERROR",
        message="Error interno del servidor. Contacte al administrador si persiste.",
        details=error_details,
        correlation_id=correlation_id
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response
    )

# =============================================================================
# MIDDLEWARE PARA REQUEST/RESPONSE LOGGING
# =============================================================================

async def logging_middleware(request: Request, call_next):
    """Middleware para logging de requests y responses."""
    
    start_time = datetime.now()
    correlation_id = str(uuid.uuid4())[:8]
    
    # Log del request entrante
    logger.info(
        f"Request iniciado",
        method=request.method,
        path=request.url.path,
        query_params=str(request.query_params),
        correlation_id=correlation_id
    )
    
    # Procesar request
    try:
        response = await call_next(request)
        
        # Calcular tiempo de procesamiento
        process_time = (datetime.now() - start_time).total_seconds()
        
        # Log del response
        logger.info(
            f"Request completado",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time_seconds=round(process_time, 4),
            correlation_id=correlation_id
        )
        
        # Agregar correlation ID al header
        response.headers["X-Correlation-ID"] = correlation_id
        
        return response
        
    except Exception as e:
        process_time = (datetime.now() - start_time).total_seconds()
        
        logger.error(
            f"Request falló",
            method=request.method,
            path=request.url.path,
            process_time_seconds=round(process_time, 4),
            error=str(e),
            correlation_id=correlation_id
        )
        raise

# =============================================================================
# CONFIGURACIÓN PARA FastAPI
# =============================================================================

def setup_error_handling(app: FastAPI) -> None:
    """Configurar error handling centralizado en FastAPI."""
    
    # Registrar exception handlers
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    # Registrar middleware de logging
    app.middleware("http")(logging_middleware)
    
    logger.info("Error handling centralizado configurado exitosamente")

# =============================================================================
# UTILIDADES PARA BUSINESS LOGIC
# =============================================================================

class BusinessLogicError(Exception):
    """Excepción personalizada para errores de lógica de negocio."""
    
    def __init__(self, message: str, error_code: str = None, details: Dict = None):
        self.message = message
        self.error_code = error_code or "BUSINESS_LOGIC_ERROR"
        self.details = details or {}
        super().__init__(self.message)

def raise_not_found(entity: str, identifier: str):
    """Utility para errores 404 consistentes."""
    raise HTTPException(
        status_code=404,
        detail=f"{entity} con ID '{identifier}' no encontrado"
    )

def raise_bad_request(message: str, details: Dict = None):
    """Utility para errores 400 consistentes."""
    raise HTTPException(
        status_code=400,
        detail=message
    )

def raise_validation_error(field: str, message: str):
    """Utility para errores de validación específicos."""
    raise HTTPException(
        status_code=422,
        detail=f"Error de validación en campo '{field}': {message}"
    )