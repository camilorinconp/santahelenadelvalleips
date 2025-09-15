-- =============================================================================
-- TABLA DE AUDITORÍA DE SEGURIDAD
-- Sistema de logging de accesos y eventos de seguridad
-- =============================================================================

-- Crear tabla de auditoría de seguridad
CREATE TABLE IF NOT EXISTS security_audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id VARCHAR(255) NOT NULL UNIQUE,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Contexto de usuario
    user_id VARCHAR(255) NOT NULL,
    access_level VARCHAR(50) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(255),
    
    -- Información del recurso y operación
    resource_type VARCHAR(50) NOT NULL,
    operation VARCHAR(50) NOT NULL,
    resource_id VARCHAR(255),
    
    -- Resultado y análisis
    result VARCHAR(20) NOT NULL CHECK (result IN ('GRANTED', 'DENIED', 'ERROR')),
    risk_level VARCHAR(20) NOT NULL CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    
    -- Metadata adicional
    additional_metadata JSONB,
    data_fingerprint VARCHAR(20),
    
    -- Auditoría interna
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para optimización de queries
CREATE INDEX IF NOT EXISTS idx_security_audit_timestamp ON security_audit_log(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_security_audit_user_id ON security_audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_security_audit_result ON security_audit_log(result);
CREATE INDEX IF NOT EXISTS idx_security_audit_risk_level ON security_audit_log(risk_level);
CREATE INDEX IF NOT EXISTS idx_security_audit_resource_type ON security_audit_log(resource_type);
CREATE INDEX IF NOT EXISTS idx_security_audit_fingerprint ON security_audit_log(data_fingerprint);

-- Índice compuesto para queries comunes
CREATE INDEX IF NOT EXISTS idx_security_audit_user_timestamp ON security_audit_log(user_id, timestamp DESC);

-- RLS Policy para acceso restringido
ALTER TABLE security_audit_log ENABLE ROW LEVEL SECURITY;

-- Policy: Solo administradores y superusuarios pueden leer logs de auditoría
CREATE POLICY "Audit log read access" ON security_audit_log
    FOR SELECT
    USING (
        -- Por ahora permitir lectura para testing
        -- En producción: verificar nivel de acceso del usuario
        true
    );

-- Policy: Solo el sistema puede insertar logs (service_role)
CREATE POLICY "Audit log insert access" ON security_audit_log
    FOR INSERT
    WITH CHECK (
        -- Solo service_role puede insertar
        auth.role() = 'service_role'
    );

-- Comentarios para documentación
COMMENT ON TABLE security_audit_log IS 'Tabla de auditoría de seguridad para tracking de accesos y eventos críticos';
COMMENT ON COLUMN security_audit_log.event_id IS 'ID único del evento de seguridad';
COMMENT ON COLUMN security_audit_log.user_id IS 'ID del usuario que realizó la acción';
COMMENT ON COLUMN security_audit_log.access_level IS 'Nivel de acceso del usuario (BÁSICO_USUARIO, MÉDICO_CONSULTA, etc.)';
COMMENT ON COLUMN security_audit_log.resource_type IS 'Tipo de recurso accedido (PACIENTE, ATENCIÓN_MÉDICA, etc.)';
COMMENT ON COLUMN security_audit_log.operation IS 'Operación realizada (CREATE, READ, UPDATE, DELETE, etc.)';
COMMENT ON COLUMN security_audit_log.result IS 'Resultado del acceso (GRANTED, DENIED, ERROR)';
COMMENT ON COLUMN security_audit_log.risk_level IS 'Nivel de riesgo evaluado (LOW, MEDIUM, HIGH, CRITICAL)';
COMMENT ON COLUMN security_audit_log.data_fingerprint IS 'Hash para detección de patrones sospechosos';

-- =============================================================================
-- TABLA DE CONFIGURACIÓN DE SECURITY
-- =============================================================================

-- Tabla para configurar reglas de seguridad dinámicas
CREATE TABLE IF NOT EXISTS security_configuration (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    config_key VARCHAR(100) NOT NULL UNIQUE,
    config_value JSONB NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insertar configuraciones por defecto
INSERT INTO security_configuration (config_key, config_value, description) VALUES
('blocked_ips', '[]', 'Lista de IPs bloqueadas'),
('suspicious_ips', '[]', 'Lista de IPs bajo sospecha'),
('rate_limits', '{"default": 100, "sensitive_operations": 10}', 'Límites de rate limiting por tipo de operación'),
('alert_thresholds', '{"failed_attempts": 5, "bulk_operations": 3}', 'Umbrales para generar alertas'),
('working_hours', '{"start": 6, "end": 22}', 'Horario laboral para análisis de riesgo')
ON CONFLICT (config_key) DO NOTHING;

-- RLS para tabla de configuración
ALTER TABLE security_configuration ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Security config read access" ON security_configuration
    FOR SELECT
    USING (true);  -- Lectura para todos, modificación solo para admins

-- =============================================================================
-- VISTAS PARA ANÁLISIS DE SEGURIDAD
-- =============================================================================

-- Vista de eventos de alto riesgo
CREATE OR REPLACE VIEW high_risk_security_events AS
SELECT 
    event_id,
    timestamp,
    user_id,
    resource_type,
    operation,
    result,
    risk_level,
    ip_address,
    additional_metadata->>'reason' as reason
FROM security_audit_log
WHERE risk_level IN ('HIGH', 'CRITICAL')
ORDER BY timestamp DESC;

-- Vista de accesos denegados
CREATE OR REPLACE VIEW denied_access_events AS
SELECT 
    event_id,
    timestamp,
    user_id,
    resource_type,
    operation,
    ip_address,
    additional_metadata->>'reason' as denial_reason
FROM security_audit_log
WHERE result = 'DENIED'
ORDER BY timestamp DESC;

-- Vista de estadísticas de seguridad por día
CREATE OR REPLACE VIEW daily_security_stats AS
SELECT 
    DATE(timestamp) as date,
    COUNT(*) as total_events,
    COUNT(*) FILTER (WHERE result = 'DENIED') as denied_events,
    COUNT(*) FILTER (WHERE risk_level IN ('HIGH', 'CRITICAL')) as high_risk_events,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(DISTINCT ip_address) as unique_ips
FROM security_audit_log
GROUP BY DATE(timestamp)
ORDER BY date DESC;

-- Trigger para actualizar updated_at en security_configuration
CREATE OR REPLACE FUNCTION update_security_config_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_security_config_updated_at
    BEFORE UPDATE ON security_configuration
    FOR EACH ROW
    EXECUTE FUNCTION update_security_config_updated_at();