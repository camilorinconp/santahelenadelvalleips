# =============================================================================
# Security Avanzada - Growth Tier Implementation
# Sistema de auditoría, acceso granular y seguridad enterprise-ready
# =============================================================================

import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from uuid import UUID, uuid4
from enum import Enum
import ipaddress
from dataclasses import dataclass
from supabase import Client
from core.error_handling import logger

# =============================================================================
# ENUMS Y TIPOS DE DATOS DE SEGURIDAD
# =============================================================================

class AccessLevel(str, Enum):
    """Niveles de acceso granular del sistema."""
    PÚBLICO_LECTURA = "PÚBLICO_LECTURA"                    # Datos no sensibles
    BÁSICO_USUARIO = "BÁSICO_USUARIO"                      # Usuario autenticado básico
    MÉDICO_CONSULTA = "MÉDICO_CONSULTA"                    # Médico - solo consulta
    MÉDICO_ATENCIÓN = "MÉDICO_ATENCIÓN"                    # Médico - crear/modificar atenciones
    ENFERMERO_OPERATIVO = "ENFERMERO_OPERATIVO"            # Enfermero - operaciones básicas
    ADMINISTRADOR_IPS = "ADMINISTRADOR_IPS"                # Admin de la IPS
    SUPERUSUARIO = "SUPERUSUARIO"                          # Admin técnico total

class OperationType(str, Enum):
    """Tipos de operación para auditoría."""
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    BULK_OPERATION = "BULK_OPERATION"
    EXPORT = "EXPORT"
    IMPORT = "IMPORT"
    AUTHENTICATION = "AUTHENTICATION"
    AUTHORIZATION_FAILED = "AUTHORIZATION_FAILED"

class ResourceType(str, Enum):
    """Tipos de recursos del sistema."""
    PACIENTE = "PACIENTE"
    ATENCIÓN_MÉDICA = "ATENCIÓN_MÉDICA"
    HISTORIA_CLÍNICA = "HISTORIA_CLÍNICA"
    DATOS_SENSIBLES = "DATOS_SENSIBLES"
    ESTADÍSTICAS = "ESTADÍSTICAS"
    CONFIGURACIÓN_SISTEMA = "CONFIGURACIÓN_SISTEMA"
    USUARIOS = "USUARIOS"

class RiskLevel(str, Enum):
    """Niveles de riesgo para análisis de acceso."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

# =============================================================================
# DATA CLASSES PARA SECURITY
# =============================================================================

@dataclass
class UserContext:
    """Contexto de usuario para decisiones de seguridad."""
    user_id: str
    access_level: AccessLevel
    department: Optional[str] = None
    specialization: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    roles: List[str] = None
    
    def __post_init__(self):
        if self.roles is None:
            self.roles = []

@dataclass
class AccessRequest:
    """Request de acceso para evaluación de seguridad."""
    resource_type: ResourceType
    operation: OperationType
    resource_id: Optional[str] = None
    additional_context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.additional_context is None:
            self.additional_context = {}

@dataclass
class SecurityEvent:
    """Evento de seguridad para auditoría."""
    event_id: str
    timestamp: datetime
    user_context: UserContext
    access_request: AccessRequest
    result: str  # GRANTED, DENIED, ERROR
    risk_level: RiskLevel
    additional_metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.additional_metadata is None:
            self.additional_metadata = {}

# =============================================================================
# SISTEMA DE AUTORIZACION GRANULAR
# =============================================================================

class GranularAccessController:
    """Controlador de acceso granular para recursos de salud."""
    
    def __init__(self):
        # Matriz de permisos: access_level -> resource_type -> operations
        self.permissions_matrix = {
            AccessLevel.PÚBLICO_LECTURA: {
                ResourceType.ESTADÍSTICAS: [OperationType.READ]
            },
            AccessLevel.BÁSICO_USUARIO: {
                ResourceType.ESTADÍSTICAS: [OperationType.READ],
                ResourceType.CONFIGURACIÓN_SISTEMA: [OperationType.READ]
            },
            AccessLevel.MÉDICO_CONSULTA: {
                ResourceType.PACIENTE: [OperationType.READ],
                ResourceType.ATENCIÓN_MÉDICA: [OperationType.READ],
                ResourceType.HISTORIA_CLÍNICA: [OperationType.READ],
                ResourceType.ESTADÍSTICAS: [OperationType.READ]
            },
            AccessLevel.MÉDICO_ATENCIÓN: {
                ResourceType.PACIENTE: [OperationType.READ, OperationType.CREATE, OperationType.UPDATE],
                ResourceType.ATENCIÓN_MÉDICA: [OperationType.READ, OperationType.CREATE, OperationType.UPDATE],
                ResourceType.HISTORIA_CLÍNICA: [OperationType.READ, OperationType.CREATE, OperationType.UPDATE],
                ResourceType.ESTADÍSTICAS: [OperationType.READ],
                ResourceType.DATOS_SENSIBLES: [OperationType.READ, OperationType.CREATE, OperationType.UPDATE]
            },
            AccessLevel.ENFERMERO_OPERATIVO: {
                ResourceType.PACIENTE: [OperationType.READ, OperationType.UPDATE],
                ResourceType.ATENCIÓN_MÉDICA: [OperationType.READ, OperationType.UPDATE],
                ResourceType.ESTADÍSTICAS: [OperationType.READ]
            },
            AccessLevel.ADMINISTRADOR_IPS: {
                ResourceType.PACIENTE: [OperationType.READ, OperationType.CREATE, OperationType.UPDATE, OperationType.EXPORT],
                ResourceType.ATENCIÓN_MÉDICA: [OperationType.READ, OperationType.CREATE, OperationType.UPDATE, OperationType.EXPORT],
                ResourceType.HISTORIA_CLÍNICA: [OperationType.READ, OperationType.EXPORT],
                ResourceType.ESTADÍSTICAS: [OperationType.READ, OperationType.EXPORT],
                ResourceType.USUARIOS: [OperationType.READ, OperationType.CREATE, OperationType.UPDATE],
                ResourceType.CONFIGURACIÓN_SISTEMA: [OperationType.READ, OperationType.UPDATE],
                ResourceType.DATOS_SENSIBLES: [OperationType.READ, OperationType.EXPORT]
            },
            AccessLevel.SUPERUSUARIO: {
                # Full access to everything
                ResourceType.PACIENTE: list(OperationType),
                ResourceType.ATENCIÓN_MÉDICA: list(OperationType),
                ResourceType.HISTORIA_CLÍNICA: list(OperationType),
                ResourceType.ESTADÍSTICAS: list(OperationType),
                ResourceType.USUARIOS: list(OperationType),
                ResourceType.CONFIGURACIÓN_SISTEMA: list(OperationType),
                ResourceType.DATOS_SENSIBLES: list(OperationType)
            }
        }
        
        # Recursos que requieren logging especial
        self.sensitive_resources = {
            ResourceType.DATOS_SENSIBLES,
            ResourceType.HISTORIA_CLÍNICA,
            ResourceType.USUARIOS
        }
        
        # IPs sospechosas o bloqueadas
        self.blocked_ips = set()
        self.suspicious_ips = set()
    
    def check_access(self, user_context: UserContext, access_request: AccessRequest) -> tuple[bool, RiskLevel, str]:
        """
        Verificar si el usuario tiene acceso al recurso solicitado.
        
        Returns:
            (permitted: bool, risk_level: RiskLevel, reason: str)
        """
        
        # Check 1: IP bloqueada
        if user_context.ip_address and self._is_ip_blocked(user_context.ip_address):
            return False, RiskLevel.CRITICAL, f"IP {user_context.ip_address} está bloqueada"
        
        # Check 2: Permisos básicos por matriz
        if not self._check_basic_permissions(user_context.access_level, access_request):
            return False, RiskLevel.MEDIUM, f"Sin permisos para {access_request.operation} en {access_request.resource_type}"
        
        # Check 3: Análisis de riesgo contextual
        risk_level = self._assess_risk_level(user_context, access_request)
        
        # Check 4: Verificaciones adicionales de alto riesgo
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            additional_checks_passed, reason = self._perform_additional_security_checks(user_context, access_request)
            if not additional_checks_passed:
                return False, risk_level, reason
        
        # Check 5: Rate limiting básico
        if self._is_rate_limited(user_context, access_request):
            return False, RiskLevel.MEDIUM, "Rate limit excedido"
        
        return True, risk_level, "Acceso autorizado"
    
    def _check_basic_permissions(self, access_level: AccessLevel, access_request: AccessRequest) -> bool:
        """Verificar permisos básicos según matriz."""
        permitted_resources = self.permissions_matrix.get(access_level, {})
        permitted_operations = permitted_resources.get(access_request.resource_type, [])
        return access_request.operation in permitted_operations
    
    def _assess_risk_level(self, user_context: UserContext, access_request: AccessRequest) -> RiskLevel:
        """Evaluar nivel de riesgo del acceso."""
        risk_score = 0
        
        # Factor 1: Tipo de recurso
        if access_request.resource_type in self.sensitive_resources:
            risk_score += 2
        
        # Factor 2: Tipo de operación
        if access_request.operation in [OperationType.DELETE, OperationType.BULK_OPERATION]:
            risk_score += 3
        elif access_request.operation in [OperationType.EXPORT, OperationType.UPDATE]:
            risk_score += 1
        
        # Factor 3: IP sospechosa
        if user_context.ip_address and user_context.ip_address in self.suspicious_ips:
            risk_score += 2
        
        # Factor 4: Acceso fuera de horario (simplificado)
        current_hour = datetime.now().hour
        if current_hour < 6 or current_hour > 22:  # 6 AM - 10 PM
            risk_score += 1
        
        # Factor 5: Nivel de acceso vs operación
        if (user_context.access_level == AccessLevel.BÁSICO_USUARIO and 
            access_request.operation in [OperationType.CREATE, OperationType.UPDATE, OperationType.DELETE]):
            risk_score += 2
        
        # Mapear score a risk level
        if risk_score <= 1:
            return RiskLevel.LOW
        elif risk_score <= 3:
            return RiskLevel.MEDIUM
        elif risk_score <= 5:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
    
    def _perform_additional_security_checks(self, user_context: UserContext, access_request: AccessRequest) -> tuple[bool, str]:
        """Verificaciones adicionales para accesos de alto riesgo."""
        
        # Check 1: Usuarios de alto privilegio requieren sesión reciente
        if (user_context.access_level in [AccessLevel.ADMINISTRADOR_IPS, AccessLevel.SUPERUSUARIO] and
            not self._is_session_recent(user_context.session_id)):
            return False, "Sesión expirada para usuario de alto privilegio"
        
        # Check 2: Operaciones DELETE requieren justificación
        if (access_request.operation == OperationType.DELETE and 
            not access_request.additional_context.get("justification")):
            return False, "Operación DELETE requiere justificación"
        
        # Check 3: Bulk operations requieren aprobación adicional
        if (access_request.operation == OperationType.BULK_OPERATION and
            not access_request.additional_context.get("approved_by_supervisor")):
            return False, "Operación masiva requiere aprobación de supervisor"
        
        return True, "Verificaciones adicionales pasadas"
    
    def _is_ip_blocked(self, ip_address: str) -> bool:
        """Verificar si IP está bloqueada."""
        try:
            ip = ipaddress.ip_address(ip_address)
            # Bloquear IPs privadas sospechosas
            if ip.is_private and ip_address in self.blocked_ips:
                return True
            return ip_address in self.blocked_ips
        except:
            return True  # IP inválida = bloqueada
    
    def _is_rate_limited(self, user_context: UserContext, access_request: AccessRequest) -> bool:
        """Rate limiting básico (implementación simplificada)."""
        # TODO: Implementar rate limiting real con Redis o similar
        # Por ahora: false (sin limiting)
        return False
    
    def _is_session_recent(self, session_id: Optional[str]) -> bool:
        """Verificar si la sesión es reciente (implementación simplificada)."""
        # TODO: Implementar verificación real de sesión
        # Por ahora: true (sesión válida)
        return session_id is not None

# =============================================================================
# SISTEMA DE AUDITORIA DE ACCESO
# =============================================================================

class AccessAuditLogger:
    """Sistema de auditoría de acceso automática."""
    
    def __init__(self, db: Client):
        self.db = db
        self.access_controller = GranularAccessController()
        
        # Configuración de auditoría
        self.always_log_resources = {
            ResourceType.DATOS_SENSIBLES,
            ResourceType.HISTORIA_CLÍNICA,
            ResourceType.USUARIOS,
            ResourceType.CONFIGURACIÓN_SISTEMA
        }
        
        self.always_log_operations = {
            OperationType.DELETE,
            OperationType.BULK_OPERATION,
            OperationType.EXPORT,
            OperationType.AUTHENTICATION,
            OperationType.AUTHORIZATION_FAILED
        }
    
    async def log_access_attempt(self, user_context: UserContext, access_request: AccessRequest) -> SecurityEvent:
        """Log intento de acceso con evaluación de seguridad."""
        
        # Evaluar acceso
        permitted, risk_level, reason = self.access_controller.check_access(user_context, access_request)
        result = "GRANTED" if permitted else "DENIED"
        
        # Crear evento de seguridad
        security_event = SecurityEvent(
            event_id=str(uuid4()),
            timestamp=datetime.now(),
            user_context=user_context,
            access_request=access_request,
            result=result,
            risk_level=risk_level,
            additional_metadata={
                "reason": reason,
                "user_agent": user_context.user_agent,
                "session_id": user_context.session_id
            }
        )
        
        # Determinar si debe loggearse
        should_log = self._should_log_event(security_event)
        
        if should_log:
            await self._persist_security_event(security_event)
        
        # Log en sistema general siempre
        log_level = "warning" if result == "DENIED" else "info"
        getattr(logger, log_level)(
            f"Access {result}: {user_context.user_id} -> {access_request.operation} {access_request.resource_type}",
            event_id=security_event.event_id,
            user_id=user_context.user_id,
            resource_type=access_request.resource_type,
            operation=access_request.operation,
            risk_level=risk_level,
            ip_address=user_context.ip_address,
            result=result,
            reason=reason
        )
        
        return security_event
    
    def _should_log_event(self, event: SecurityEvent) -> bool:
        """Determinar si el evento debe persistirse en auditoría."""
        
        # Siempre loggear denegaciones
        if event.result == "DENIED":
            return True
        
        # Siempre loggear recursos sensibles
        if event.access_request.resource_type in self.always_log_resources:
            return True
        
        # Siempre loggear operaciones críticas
        if event.access_request.operation in self.always_log_operations:
            return True
        
        # Siempre loggear riesgo alto
        if event.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            return True
        
        # Loggear administradores
        if event.user_context.access_level in [AccessLevel.ADMINISTRADOR_IPS, AccessLevel.SUPERUSUARIO]:
            return True
        
        return False
    
    async def _persist_security_event(self, event: SecurityEvent):
        """Persistir evento de seguridad en base de datos."""
        
        try:
            # Preparar datos para inserción
            audit_record = {
                "event_id": event.event_id,
                "timestamp": event.timestamp.isoformat(),
                "user_id": event.user_context.user_id,
                "access_level": event.user_context.access_level,
                "ip_address": event.user_context.ip_address,
                "user_agent": event.user_context.user_agent,
                "session_id": event.user_context.session_id,
                "resource_type": event.access_request.resource_type,
                "operation": event.access_request.operation,
                "resource_id": event.access_request.resource_id,
                "result": event.result,
                "risk_level": event.risk_level,
                "additional_metadata": json.dumps(event.additional_metadata),
                "data_fingerprint": self._create_data_fingerprint(event)
            }
            
            # Insertar en tabla de auditoría
            await self.db.table("security_audit_log").insert(audit_record).execute()
            
        except Exception as e:
            logger.error(
                f"Error persistiendo evento de auditoría: {str(e)}",
                event_id=event.event_id,
                user_id=event.user_context.user_id
            )
    
    def _create_data_fingerprint(self, event: SecurityEvent) -> str:
        """Crear fingerprint para detección de patrones."""
        fingerprint_data = {
            "user_id": event.user_context.user_id,
            "resource_type": event.access_request.resource_type,
            "operation": event.access_request.operation,
            "hour": event.timestamp.hour,
            "day_of_week": event.timestamp.weekday()
        }
        
        fingerprint_str = json.dumps(fingerprint_data, sort_keys=True)
        return hashlib.md5(fingerprint_str.encode()).hexdigest()[:12]
    
    async def get_security_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Obtener resumen de seguridad de las últimas N horas."""
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        try:
            # Query audit log
            response = await self.db.table("security_audit_log")\
                .select("*")\
                .gte("timestamp", cutoff_time.isoformat())\
                .execute()
            
            events = response.data if response.data else []
            
            # Analizar eventos
            summary = {
                "period_hours": hours,
                "total_events": len(events),
                "denied_access_count": len([e for e in events if e["result"] == "DENIED"]),
                "high_risk_events": len([e for e in events if e["risk_level"] in ["HIGH", "CRITICAL"]]),
                "unique_users": len(set(e["user_id"] for e in events)),
                "unique_ips": len(set(e["ip_address"] for e in events if e["ip_address"])),
                "operations_breakdown": {},
                "risk_level_breakdown": {},
                "suspicious_patterns": []
            }
            
            # Breakdown por operación
            for event in events:
                operation = event["operation"]
                summary["operations_breakdown"][operation] = summary["operations_breakdown"].get(operation, 0) + 1
            
            # Breakdown por risk level
            for event in events:
                risk_level = event["risk_level"]
                summary["risk_level_breakdown"][risk_level] = summary["risk_level_breakdown"].get(risk_level, 0) + 1
            
            # Detectar patrones sospechosos (simplificado)
            summary["suspicious_patterns"] = self._detect_suspicious_patterns(events)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generando resumen de seguridad: {str(e)}")
            return {"error": "No se pudo generar resumen de seguridad"}
    
    def _detect_suspicious_patterns(self, events: List[Dict]) -> List[Dict[str, Any]]:
        """Detectar patrones sospechosos en eventos de auditoría."""
        patterns = []
        
        # Patrón 1: Múltiples accesos denegados del mismo usuario
        denied_by_user = {}
        for event in events:
            if event["result"] == "DENIED":
                user_id = event["user_id"]
                denied_by_user[user_id] = denied_by_user.get(user_id, 0) + 1
        
        for user_id, count in denied_by_user.items():
            if count >= 5:  # 5+ accesos denegados
                patterns.append({
                    "type": "MULTIPLE_DENIED_ACCESS",
                    "severity": "HIGH",
                    "user_id": user_id,
                    "count": count,
                    "description": f"Usuario {user_id} con {count} accesos denegados"
                })
        
        # Patrón 2: Acceso desde múltiples IPs del mismo usuario
        ips_by_user = {}
        for event in events:
            if event["ip_address"]:
                user_id = event["user_id"]
                if user_id not in ips_by_user:
                    ips_by_user[user_id] = set()
                ips_by_user[user_id].add(event["ip_address"])
        
        for user_id, ips in ips_by_user.items():
            if len(ips) >= 3:  # 3+ IPs diferentes
                patterns.append({
                    "type": "MULTIPLE_IP_ACCESS",
                    "severity": "MEDIUM",
                    "user_id": user_id,
                    "ip_count": len(ips),
                    "ips": list(ips),
                    "description": f"Usuario {user_id} accedió desde {len(ips)} IPs diferentes"
                })
        
        return patterns

# =============================================================================
# MIDDLEWARE DE SECURITY
# =============================================================================

def create_security_middleware(audit_logger: AccessAuditLogger):
    """Crear middleware de seguridad para FastAPI."""
    
    async def security_middleware(request, call_next):
        """Middleware que evalúa y audita accesos automáticamente."""
        
        # Extraer contexto de usuario (simplificado)
        user_context = UserContext(
            user_id=request.headers.get("X-User-ID", "anonymous"),
            access_level=AccessLevel(request.headers.get("X-Access-Level", AccessLevel.BÁSICO_USUARIO)),
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("User-Agent"),
            session_id=request.headers.get("X-Session-ID")
        )
        
        # Determinar tipo de recurso y operación basado en la ruta
        resource_type, operation = _infer_resource_and_operation(request)
        
        access_request = AccessRequest(
            resource_type=resource_type,
            operation=operation,
            additional_context={"path": request.url.path, "method": request.method}
        )
        
        # Auditar intento de acceso
        security_event = await audit_logger.log_access_attempt(user_context, access_request)
        
        # Si acceso denegado, retornar error
        if security_event.result == "DENIED":
            from fastapi import HTTPException
            raise HTTPException(
                status_code=403,
                detail=f"Acceso denegado: {security_event.additional_metadata['reason']}"
            )
        
        # Continuar con request
        response = await call_next(request)
        
        # Agregar headers de seguridad
        response.headers["X-Security-Event-ID"] = security_event.event_id
        response.headers["X-Risk-Level"] = security_event.risk_level
        
        return response
    
    return security_middleware

def _infer_resource_and_operation(request) -> tuple[ResourceType, OperationType]:
    """Inferir tipo de recurso y operación de la request."""
    
    path = request.url.path.lower()
    method = request.method.upper()
    
    # Mapear rutas a tipos de recurso
    if "/pacientes" in path:
        resource_type = ResourceType.PACIENTE
    elif "/atenciones" in path or "/primera-infancia" in path:
        resource_type = ResourceType.ATENCIÓN_MÉDICA
    elif "/health" in path or "/metrics" in path:
        resource_type = ResourceType.ESTADÍSTICAS
    elif "/users" in path or "/admin" in path:
        resource_type = ResourceType.USUARIOS
    else:
        resource_type = ResourceType.ESTADÍSTICAS  # Default
    
    # Mapear métodos HTTP a operaciones
    operation_mapping = {
        "GET": OperationType.READ,
        "POST": OperationType.CREATE,
        "PUT": OperationType.UPDATE,
        "PATCH": OperationType.UPDATE,
        "DELETE": OperationType.DELETE
    }
    
    operation = operation_mapping.get(method, OperationType.READ)
    
    return resource_type, operation

# =============================================================================
# INSTANCIAS GLOBALES
# =============================================================================

# Será inicializado en setup
access_controller = GranularAccessController()
audit_logger = None  # Se inicializa con DB connection

def setup_security(app, db: Client):
    """Configurar sistema de seguridad en FastAPI."""
    
    global audit_logger
    audit_logger = AccessAuditLogger(db)
    
    # Solo agregar middleware de seguridad en producción
    # En testing y desarrollo, usar service_role sin middleware adicional
    import os
    environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "production":
        security_middleware = create_security_middleware(audit_logger)
        app.middleware("http")(security_middleware)
        logger.info("Sistema de seguridad avanzada configurado para producción")
    else:
        logger.info("Sistema de seguridad configurado para desarrollo (middleware deshabilitado)")