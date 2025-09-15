# =============================================================================
# Performance Monitoring & Health Checks - IPS Santa Helena del Valle
# Sistema de monitoreo básico para APIs y base de datos
# =============================================================================

import time
import psutil
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from database import get_supabase_client
from core.error_handling import logger

# =============================================================================
# MÉTRICAS DE PERFORMANCE
# =============================================================================

class PerformanceMetrics:
    """Collector de métricas básicas de performance."""
    
    def __init__(self):
        self.request_count = 0
        self.total_response_time = 0.0
        self.error_count = 0
        self.start_time = datetime.now()
    
    def record_request(self, response_time: float, is_error: bool = False):
        """Registrar métrica de request."""
        self.request_count += 1
        self.total_response_time += response_time
        if is_error:
            self.error_count += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas actuales."""
        uptime = datetime.now() - self.start_time
        
        return {
            "requests_total": self.request_count,
            "errors_total": self.error_count,
            "uptime_seconds": int(uptime.total_seconds()),
            "average_response_time": round(
                self.total_response_time / max(self.request_count, 1), 4
            ),
            "error_rate_percentage": round(
                (self.error_count / max(self.request_count, 1)) * 100, 2
            )
        }

# Instancia global de métricas
metrics = PerformanceMetrics()

# =============================================================================
# HEALTH CHECKS
# =============================================================================

class HealthChecker:
    """Verificaciones de salud del sistema."""
    
    @staticmethod
    async def check_database(db: Client) -> Dict[str, Any]:
        """Verificar conectividad y performance de base de datos."""
        start_time = time.time()
        
        try:
            # Test básico de conectividad
            response = db.table("pacientes").select("id").limit(1).execute()
            db_time = round((time.time() - start_time) * 1000, 2)  # ms
            
            return {
                "status": "healthy",
                "response_time_ms": db_time,
                "details": {
                    "connection": "ok",
                    "query_test": "passed",
                    "records_found": len(response.data) if response.data else 0
                }
            }
            
        except Exception as e:
            db_time = round((time.time() - start_time) * 1000, 2)
            logger.error(f"Database health check failed: {str(e)}")
            
            return {
                "status": "unhealthy",
                "response_time_ms": db_time,
                "details": {
                    "connection": "failed",
                    "error": str(e)
                }
            }
    
    @staticmethod
    def check_system_resources() -> Dict[str, Any]:
        """Verificar recursos del sistema."""
        try:
            # Métricas de CPU y memoria
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Determinar estado basado en thresholds
            cpu_status = "healthy" if cpu_percent < 80 else "warning" if cpu_percent < 95 else "unhealthy"
            memory_status = "healthy" if memory.percent < 80 else "warning" if memory.percent < 95 else "unhealthy"
            disk_status = "healthy" if disk.percent < 80 else "warning" if disk.percent < 95 else "unhealthy"
            
            # Estado general
            overall_status = "unhealthy" if "unhealthy" in [cpu_status, memory_status, disk_status] else \
                           "warning" if "warning" in [cpu_status, memory_status, disk_status] else "healthy"
            
            return {
                "status": overall_status,
                "details": {
                    "cpu": {
                        "usage_percent": round(cpu_percent, 1),
                        "status": cpu_status
                    },
                    "memory": {
                        "usage_percent": round(memory.percent, 1),
                        "available_gb": round(memory.available / (1024**3), 2),
                        "status": memory_status
                    },
                    "disk": {
                        "usage_percent": round(disk.percent, 1),
                        "free_gb": round(disk.free / (1024**3), 2),
                        "status": disk_status
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"System resources check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "details": {
                    "error": str(e)
                }
            }
    
    @staticmethod
    async def check_critical_endpoints(db: Client) -> Dict[str, Any]:
        """Verificar endpoints críticos del sistema."""
        start_time = time.time()
        
        try:
            # Test endpoints críticos
            tests = []
            
            # Test 1: Listar pacientes
            try:
                patients_response = db.table("pacientes").select("id").limit(5).execute()
                tests.append({
                    "endpoint": "GET /pacientes",
                    "status": "ok",
                    "records": len(patients_response.data) if patients_response.data else 0
                })
            except Exception as e:
                tests.append({
                    "endpoint": "GET /pacientes", 
                    "status": "error",
                    "error": str(e)
                })
            
            # Test 2: Primera Infancia
            try:
                pi_response = db.table("atencion_primera_infancia").select("id").limit(3).execute()
                tests.append({
                    "endpoint": "GET /atenciones-primera-infancia",
                    "status": "ok",
                    "records": len(pi_response.data) if pi_response.data else 0
                })
            except Exception as e:
                tests.append({
                    "endpoint": "GET /atenciones-primera-infancia",
                    "status": "error", 
                    "error": str(e)
                })
            
            # Test 3: Catálogos
            try:
                ocupaciones_response = db.table("catalogo_ocupaciones_dane").select("id").limit(3).execute()
                tests.append({
                    "endpoint": "GET /ocupaciones",
                    "status": "ok",
                    "records": len(ocupaciones_response.data) if ocupaciones_response.data else 0
                })
            except Exception as e:
                tests.append({
                    "endpoint": "GET /ocupaciones",
                    "status": "error",
                    "error": str(e)
                })
            
            # Evaluar estado general
            failed_tests = [t for t in tests if t["status"] == "error"]
            overall_status = "unhealthy" if failed_tests else "healthy"
            
            total_time = round((time.time() - start_time) * 1000, 2)
            
            return {
                "status": overall_status,
                "response_time_ms": total_time,
                "details": {
                    "tests_run": len(tests),
                    "tests_passed": len(tests) - len(failed_tests),
                    "tests_failed": len(failed_tests),
                    "test_results": tests
                }
            }
            
        except Exception as e:
            total_time = round((time.time() - start_time) * 1000, 2)
            logger.error(f"Critical endpoints check failed: {str(e)}")
            
            return {
                "status": "unhealthy",
                "response_time_ms": total_time,
                "details": {
                    "error": str(e)
                }
            }

# =============================================================================
# ROUTER PARA ENDPOINTS DE MONITORING
# =============================================================================

monitoring_router = APIRouter(prefix="/health", tags=["Monitoring & Health"])

@monitoring_router.get("/")
async def health_check_comprehensive(db: Client = Depends(get_supabase_client)):
    """Health check comprehensivo del sistema."""
    
    start_time = time.time()
    
    # Ejecutar todas las verificaciones
    database_health = await HealthChecker.check_database(db)
    system_health = HealthChecker.check_system_resources()
    endpoints_health = await HealthChecker.check_critical_endpoints(db)
    
    # Estado general del sistema
    health_statuses = [
        database_health["status"],
        system_health["status"], 
        endpoints_health["status"]
    ]
    
    overall_status = "unhealthy" if "unhealthy" in health_statuses else \
                    "warning" if "warning" in health_statuses else "healthy"
    
    total_time = round((time.time() - start_time) * 1000, 2)
    
    health_report = {
        "status": overall_status,
        "timestamp": datetime.now().isoformat(),
        "response_time_ms": total_time,
        "version": "1.0.0",
        "environment": "development",  # TODO: Leer de environment
        "checks": {
            "database": database_health,
            "system": system_health,
            "endpoints": endpoints_health
        },
        "metrics": metrics.get_stats()
    }
    
    # Log del health check
    logger.info(
        f"Health check completado",
        overall_status=overall_status,
        response_time_ms=total_time,
        database_status=database_health["status"],
        system_status=system_health["status"],
        endpoints_status=endpoints_health["status"]
    )
    
    return health_report

@monitoring_router.get("/quick")
async def health_check_quick():
    """Health check rápido básico."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": int((datetime.now() - metrics.start_time).total_seconds()),
        "version": "1.0.0"
    }

@monitoring_router.get("/metrics")
async def get_metrics():
    """Métricas básicas de performance."""
    system_metrics = HealthChecker.check_system_resources()
    app_metrics = metrics.get_stats()
    
    return {
        "timestamp": datetime.now().isoformat(),
        "application": app_metrics,
        "system": system_metrics["details"] if system_metrics["status"] != "unhealthy" else {"error": "Unable to get system metrics"}
    }

@monitoring_router.get("/database")
async def health_check_database(db: Client = Depends(get_supabase_client)):
    """Health check específico de base de datos."""
    return await HealthChecker.check_database(db)

# =============================================================================
# MIDDLEWARE PARA CAPTURAR MÉTRICAS
# =============================================================================

async def metrics_middleware(request, call_next):
    """Middleware para capturar métricas de performance."""
    start_time = time.time()
    
    try:
        response = await call_next(request)
        
        # Registrar métrica exitosa
        response_time = time.time() - start_time
        is_error = response.status_code >= 400
        metrics.record_request(response_time, is_error)
        
        # Agregar headers de performance
        response.headers["X-Response-Time"] = f"{round(response_time * 1000, 2)}ms"
        
        return response
        
    except Exception as e:
        # Registrar métrica de error
        response_time = time.time() - start_time
        metrics.record_request(response_time, is_error=True)
        raise

def setup_monitoring(app):
    """Configurar monitoring en FastAPI."""
    
    # Registrar router de health checks
    app.include_router(monitoring_router)
    
    # Registrar middleware de métricas
    app.middleware("http")(metrics_middleware)
    
    logger.info("Performance monitoring configurado exitosamente")

# =============================================================================
# UTILIDADES DE PERFORMANCE
# =============================================================================

class PerformanceTimer:
    """Context manager para medir tiempo de ejecución."""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        execution_time = time.time() - self.start_time
        
        if exc_type:
            logger.error(
                f"Operation '{self.operation_name}' failed",
                execution_time_seconds=round(execution_time, 4),
                error=str(exc_val)
            )
        else:
            logger.info(
                f"Operation '{self.operation_name}' completed",
                execution_time_seconds=round(execution_time, 4)
            )

# Ejemplo de uso:
# async def some_operation():
#     with PerformanceTimer("Database query - get patients"):
#         return await db.table("pacientes").select("*").execute()