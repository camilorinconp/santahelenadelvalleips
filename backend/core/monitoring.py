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
# 🚀 NUEVOS ENDPOINTS APM - GROWTH TIER
# =============================================================================

@monitoring_router.get("/apm")
async def apm_dashboard():
    """Dashboard completo APM con métricas detalladas."""
    return apm_collector.get_apm_dashboard_data()

@monitoring_router.get("/apm/alerts")
async def apm_alerts_check():
    """Verificar y obtener alertas activas."""
    alerts = apm_collector.check_alerts_and_notify()
    return {
        "timestamp": datetime.now().isoformat(),
        "alerts_found": len(alerts),
        "alerts": alerts
    }

@monitoring_router.get("/apm/endpoints")
async def apm_endpoints_detail():
    """Detalle de performance por endpoint."""
    endpoints_detail = {}
    
    for endpoint_key, metric in apm_collector.endpoints_metrics.items():
        if metric["total_requests"] > 0:
            p95_time = None
            if len(metric["p95_response_times"]) > 5:
                p95_time = sorted(metric["p95_response_times"])[int(len(metric["p95_response_times"]) * 0.95)]
            
            endpoints_detail[endpoint_key] = {
                "total_requests": metric["total_requests"],
                "success_count": metric["success_count"],
                "error_count": metric["error_count"],
                "error_rate": round((metric["error_count"] / metric["total_requests"]) * 100, 2),
                "avg_response_time": round(metric["total_response_time"] / metric["total_requests"], 4),
                "p95_response_time": round(p95_time, 3) if p95_time else None,
                "requests_last_24h": len(metric["last_24h_requests"])
            }
    
    return {
        "timestamp": datetime.now().isoformat(),
        "endpoints": endpoints_detail
    }

@monitoring_router.get("/apm/database")
async def apm_database_detail():
    """Detalle de performance de operaciones de base de datos."""
    return {
        "timestamp": datetime.now().isoformat(),
        "database_operations": apm_collector.database_metrics
    }

@monitoring_router.get("/apm/business")
async def apm_business_metrics():
    """Métricas de negocio específicas de salud."""
    return {
        "timestamp": datetime.now().isoformat(),
        "business_metrics": apm_collector.business_metrics
    }

# =============================================================================
# 🔒 ENDPOINTS DE SECURITY - GROWTH TIER
# =============================================================================

@monitoring_router.get("/security/summary")
async def security_summary(hours: int = 24):
    """Resumen de seguridad de las últimas N horas."""
    try:
        from core.security import audit_logger
        if audit_logger:
            summary = await audit_logger.get_security_summary(hours)
            return {
                "timestamp": datetime.now().isoformat(),
                "summary": summary
            }
        else:
            return {
                "timestamp": datetime.now().isoformat(),
                "error": "Sistema de auditoría no inicializado"
            }
    except Exception as e:
        logger.error(f"Error obteniendo resumen de seguridad: {str(e)}")
        return {
            "timestamp": datetime.now().isoformat(),
            "error": f"Error: {str(e)}"
        }

@monitoring_router.get("/security/access-levels")
async def security_access_levels():
    """Información sobre niveles de acceso disponibles."""
    from core.security import AccessLevel, ResourceType, OperationType, access_controller
    
    return {
        "timestamp": datetime.now().isoformat(),
        "access_levels": [level.value for level in AccessLevel],
        "resource_types": [resource.value for resource in ResourceType],
        "operation_types": [op.value for op in OperationType],
        "permissions_matrix": {
            level.value: {
                resource.value: [op.value for op in operations]
                for resource, operations in resources.items()
            }
            for level, resources in access_controller.permissions_matrix.items()
        }
    }

# =============================================================================
# MIDDLEWARE PARA CAPTURAR MÉTRICAS
# =============================================================================

async def metrics_middleware(request, call_next):
    """Middleware para capturar métricas de performance + APM."""
    start_time = time.time()
    
    try:
        response = await call_next(request)
        
        # Registrar métrica básica (compatibilidad)
        response_time = time.time() - start_time
        is_error = response.status_code >= 400
        metrics.record_request(response_time, is_error)
        
        # 🚀 NUEVO: Registrar métricas APM detalladas
        apm_collector.track_endpoint_performance(
            endpoint=request.url.path,
            method=request.method,
            status_code=response.status_code,
            response_time=response_time
        )
        
        # Agregar headers de performance
        response.headers["X-Response-Time"] = f"{round(response_time * 1000, 2)}ms"
        response.headers["X-Correlation-ID"] = getattr(request.state, 'correlation_id', 'unknown')
        
        return response
        
    except Exception as e:
        # Registrar métrica de error (básica + APM)
        response_time = time.time() - start_time
        metrics.record_request(response_time, is_error=True)
        
        apm_collector.track_endpoint_performance(
            endpoint=request.url.path,
            method=request.method,
            status_code=500,  # Exception = 500
            response_time=response_time
        )
        
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

# =============================================================================
# APM INTERMEDIO - GROWTH TIER IMPLEMENTATION
# =============================================================================

class APMMetricsCollector:
    """Collector de métricas APM para Growth tier - Balance simplicidad/visibilidad."""
    
    def __init__(self):
        self.endpoints_metrics = {}
        self.database_metrics = {}
        self.error_metrics = {}
        self.business_metrics = {}
        self.alerts_sent = {}
        
    def track_endpoint_performance(self, endpoint: str, method: str, 
                                 status_code: int, response_time: float):
        """Track performance de endpoints específicos."""
        key = f"{method}:{endpoint}"
        
        if key not in self.endpoints_metrics:
            self.endpoints_metrics[key] = {
                "total_requests": 0,
                "total_response_time": 0.0,
                "error_count": 0,
                "success_count": 0,
                "p95_response_times": [],
                "last_24h_requests": []
            }
        
        metric = self.endpoints_metrics[key]
        metric["total_requests"] += 1
        metric["total_response_time"] += response_time
        
        if status_code >= 400:
            metric["error_count"] += 1
        else:
            metric["success_count"] += 1
            
        # Track para P95 (mantener solo últimos 100 requests)
        metric["p95_response_times"].append(response_time)
        if len(metric["p95_response_times"]) > 100:
            metric["p95_response_times"] = metric["p95_response_times"][-100:]
        
        # Track requests por hora para alertas
        current_hour = datetime.now().hour
        metric["last_24h_requests"].append({
            "timestamp": datetime.now(),
            "hour": current_hour,
            "status_code": status_code,
            "response_time": response_time
        })
        
        # Mantener solo últimas 24 horas
        cutoff = datetime.now() - timedelta(hours=24)
        metric["last_24h_requests"] = [
            r for r in metric["last_24h_requests"] 
            if r["timestamp"] > cutoff
        ]
    
    def track_database_operation(self, table: str, operation: str, 
                                response_time: float, record_count: int = 1):
        """Track operaciones específicas de base de datos."""
        key = f"{table}:{operation}"
        
        if key not in self.database_metrics:
            self.database_metrics[key] = {
                "total_operations": 0,
                "total_response_time": 0.0,
                "total_records_processed": 0,
                "slow_queries": [],
                "error_count": 0
            }
        
        metric = self.database_metrics[key]
        metric["total_operations"] += 1
        metric["total_response_time"] += response_time
        metric["total_records_processed"] += record_count
        
        # Track slow queries (>1s)
        if response_time > 1.0:
            metric["slow_queries"].append({
                "timestamp": datetime.now(),
                "response_time": response_time,
                "record_count": record_count
            })
            
            # Mantener solo últimos 50 slow queries
            if len(metric["slow_queries"]) > 50:
                metric["slow_queries"] = metric["slow_queries"][-50:]
    
    def track_business_metric(self, metric_name: str, value: float, 
                            tags: Dict[str, str] = None):
        """Track métricas de negocio específicas de salud."""
        if metric_name not in self.business_metrics:
            self.business_metrics[metric_name] = {
                "total_events": 0,
                "sum_value": 0.0,
                "max_value": 0.0,
                "min_value": float('inf'),
                "recent_values": [],
                "tags_breakdown": {}
            }
        
        metric = self.business_metrics[metric_name]
        metric["total_events"] += 1
        metric["sum_value"] += value
        metric["max_value"] = max(metric["max_value"], value)
        metric["min_value"] = min(metric["min_value"], value)
        
        # Recent values para trending
        metric["recent_values"].append({
            "timestamp": datetime.now(),
            "value": value,
            "tags": tags or {}
        })
        
        # Mantener solo últimos 200 valores
        if len(metric["recent_values"]) > 200:
            metric["recent_values"] = metric["recent_values"][-200:]
        
        # Tags breakdown
        if tags:
            for tag_key, tag_value in tags.items():
                tag_breakdown_key = f"{tag_key}:{tag_value}"
                if tag_breakdown_key not in metric["tags_breakdown"]:
                    metric["tags_breakdown"][tag_breakdown_key] = {
                        "count": 0, "sum_value": 0.0
                    }
                metric["tags_breakdown"][tag_breakdown_key]["count"] += 1
                metric["tags_breakdown"][tag_breakdown_key]["sum_value"] += value
    
    def check_alerts_and_notify(self):
        """Verificar condiciones de alerta y enviar notificaciones."""
        alerts = []
        current_time = datetime.now()
        
        # Alert 1: Error rate alto en endpoints
        for endpoint_key, metric in self.endpoints_metrics.items():
            if metric["total_requests"] > 10:  # Solo si tiene traffic
                error_rate = (metric["error_count"] / metric["total_requests"]) * 100
                if error_rate > 15:  # >15% error rate
                    alerts.append({
                        "type": "HIGH_ERROR_RATE",
                        "severity": "HIGH",
                        "endpoint": endpoint_key,
                        "error_rate": round(error_rate, 2),
                        "message": f"Alto error rate en {endpoint_key}: {error_rate:.1f}%"
                    })
        
        # Alert 2: Response time alto
        for endpoint_key, metric in self.endpoints_metrics.items():
            if len(metric["p95_response_times"]) > 10:
                p95_time = sorted(metric["p95_response_times"])[int(len(metric["p95_response_times"]) * 0.95)]
                if p95_time > 2.0:  # P95 > 2 seconds
                    alerts.append({
                        "type": "SLOW_RESPONSE_TIME",
                        "severity": "MEDIUM",
                        "endpoint": endpoint_key,
                        "p95_response_time": round(p95_time, 3),
                        "message": f"Response time lento en {endpoint_key}: P95 {p95_time:.2f}s"
                    })
        
        # Alert 3: Slow queries recurrentes
        for db_key, metric in self.database_metrics.items():
            recent_slow_queries = [
                q for q in metric["slow_queries"]
                if q["timestamp"] > current_time - timedelta(minutes=30)
            ]
            if len(recent_slow_queries) > 5:  # >5 slow queries en 30min
                alerts.append({
                    "type": "SLOW_DATABASE_QUERIES",
                    "severity": "MEDIUM", 
                    "table_operation": db_key,
                    "slow_queries_count": len(recent_slow_queries),
                    "message": f"Múltiples queries lentas en {db_key}: {len(recent_slow_queries)} en 30min"
                })
        
        # Procesar y enviar alertas (evitar spam)
        for alert in alerts:
            alert_key = f"{alert['type']}:{alert.get('endpoint', alert.get('table_operation', 'general'))}"
            
            # Throttling: solo enviar cada 30 minutos
            if (alert_key not in self.alerts_sent or 
                current_time - self.alerts_sent[alert_key] > timedelta(minutes=30)):
                
                self._send_alert(alert)
                self.alerts_sent[alert_key] = current_time
        
        return alerts
    
    def _send_alert(self, alert: Dict[str, Any]):
        """Enviar alerta (implementar según necesidad: email, Slack, webhook)."""
        
        # Por ahora: log structured + print para visibility
        logger.warning(
            "APM Alert triggered",
            alert_type=alert["type"],
            severity=alert["severity"],
            message=alert["message"],
            details=alert
        )
        
        print(f"🚨 APM ALERT [{alert['severity']}]: {alert['message']}")
        
        # TODO: Implementar envío real de alertas
        # - Email notification
        # - Slack webhook  
        # - Discord webhook
        # - Custom webhook endpoint
    
    def get_apm_dashboard_data(self) -> Dict[str, Any]:
        """Generar datos para dashboard APM."""
        
        # Top endpoints por traffic
        top_endpoints = sorted(
            [(k, v) for k, v in self.endpoints_metrics.items()],
            key=lambda x: x[1]["total_requests"],
            reverse=True
        )[:10]
        
        # Top slow endpoints
        slow_endpoints = []
        for endpoint_key, metric in self.endpoints_metrics.items():
            if len(metric["p95_response_times"]) > 5:
                p95_time = sorted(metric["p95_response_times"])[int(len(metric["p95_response_times"]) * 0.95)]
                slow_endpoints.append((endpoint_key, p95_time))
        
        slow_endpoints = sorted(slow_endpoints, key=lambda x: x[1], reverse=True)[:5]
        
        # Database operations summary
        db_summary = {}
        for db_key, metric in self.database_metrics.items():
            avg_response_time = metric["total_response_time"] / max(metric["total_operations"], 1)
            db_summary[db_key] = {
                "total_operations": metric["total_operations"],
                "avg_response_time": round(avg_response_time, 4),
                "slow_queries_count": len(metric["slow_queries"]),
                "records_per_operation": metric["total_records_processed"] / max(metric["total_operations"], 1)
            }
        
        # Business metrics summary  
        business_summary = {}
        for metric_name, metric in self.business_metrics.items():
            business_summary[metric_name] = {
                "total_events": metric["total_events"],
                "avg_value": metric["sum_value"] / max(metric["total_events"], 1),
                "max_value": metric["max_value"],
                "min_value": metric["min_value"] if metric["min_value"] != float('inf') else 0
            }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_endpoints_tracked": len(self.endpoints_metrics),
                "total_db_operations_tracked": len(self.database_metrics),
                "total_business_metrics": len(self.business_metrics),
                "alerts_sent_last_hour": len([
                    alert_time for alert_time in self.alerts_sent.values()
                    if datetime.now() - alert_time < timedelta(hours=1)
                ])
            },
            "top_endpoints": [
                {
                    "endpoint": endpoint,
                    "total_requests": data["total_requests"],
                    "error_rate": round((data["error_count"] / max(data["total_requests"], 1)) * 100, 2),
                    "avg_response_time": round(data["total_response_time"] / max(data["total_requests"], 1), 4)
                }
                for endpoint, data in top_endpoints
            ],
            "slow_endpoints": [
                {
                    "endpoint": endpoint,
                    "p95_response_time": round(p95_time, 3)
                }
                for endpoint, p95_time in slow_endpoints
            ],
            "database_operations": db_summary,
            "business_metrics": business_summary
        }

# Instancia global de APM collector
apm_collector = APMMetricsCollector()

# =============================================================================
# BUSINESS METRICS HELPERS - ESPECÍFICOS PARA SALUD
# =============================================================================

class HealthcareBusinessMetrics:
    """Métricas de negocio específicas para sistema de salud."""
    
    @staticmethod
    def track_patient_creation(patient_data: Dict[str, Any]):
        """Track creación de pacientes con metadata."""
        apm_collector.track_business_metric(
            "patients_created",
            1,
            {
                "department": patient_data.get("departamento", "unknown"),
                "gender": patient_data.get("genero", "unknown"),
                "document_type": patient_data.get("tipo_documento", "unknown")
            }
        )
    
    @staticmethod
    def track_medical_attention(attention_type: str, duration_minutes: float, 
                              ead3_applied: bool = False, asq3_applied: bool = False):
        """Track atenciones médicas con detalles específicos."""
        apm_collector.track_business_metric(
            f"medical_attention_{attention_type}",
            duration_minutes,
            {
                "attention_type": attention_type,
                "ead3_applied": str(ead3_applied),
                "asq3_applied": str(asq3_applied)
            }
        )
        
        # Track evaluaciones especializadas
        if ead3_applied:
            apm_collector.track_business_metric("ead3_evaluations", 1)
        if asq3_applied:
            apm_collector.track_business_metric("asq3_evaluations", 1)
    
    @staticmethod
    def track_search_performance(search_type: str, query_length: int, 
                               results_count: int, response_time: float):
        """Track performance de búsquedas (ocupaciones, pacientes, etc.)."""
        apm_collector.track_business_metric(
            f"search_{search_type}_results",
            results_count,
            {
                "query_length": str(query_length),
                "response_time_bucket": "fast" if response_time < 0.5 else "slow"
            }
        )

# Healthcare metrics helper global
health_metrics = HealthcareBusinessMetrics()

# Ejemplo de uso:
# async def some_operation():
#     with PerformanceTimer("Database query - get patients"):
#         return await db.table("pacientes").select("*").execute()