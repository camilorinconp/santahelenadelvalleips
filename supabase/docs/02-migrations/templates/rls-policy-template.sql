-- =============================================
-- TEMPLATE: ROW LEVEL SECURITY (RLS) POLICIES
-- =============================================
-- Descripción: Template reutilizable para configurar RLS siguiendo
--              convenciones de seguridad IPS Santa Helena del Valle
-- Fecha: [DD mes AAAA]
-- Autor: [Tu nombre]
-- Contexto: [Explicar modelo de seguridad requerido]
-- Impacto: [Describir qué acceso se permite/bloquea]
-- =============================================

BEGIN;

-- =============================================
-- 1. VERIFICACIONES PRE-EJECUCIÓN
-- =============================================
DO $pre_check$
DECLARE
    table_exists BOOLEAN;
    rls_enabled BOOLEAN;
    existing_policies INTEGER;
BEGIN
    -- Verificar que la tabla existe
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = '[NOMBRE_TABLA]'
    ) INTO table_exists;
    
    IF NOT table_exists THEN
        RAISE EXCEPTION 'Tabla [NOMBRE_TABLA] no existe. Crear tabla primero.';
    END IF;
    
    -- Verificar estado RLS actual
    SELECT EXISTS (
        SELECT FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'public'
        AND c.relname = '[NOMBRE_TABLA]'
        AND c.relrowsecurity = true
    ) INTO rls_enabled;
    
    -- Contar políticas existentes
    SELECT COUNT(*) INTO existing_policies
    FROM pg_policies 
    WHERE tablename = '[NOMBRE_TABLA]' 
    AND schemaname = 'public';
    
    RAISE NOTICE '🔒 Configurando RLS para tabla: [NOMBRE_TABLA]';
    RAISE NOTICE 'RLS actualmente habilitado: %', rls_enabled;
    RAISE NOTICE 'Políticas existentes: %', existing_policies;
END;
$pre_check$;

-- =============================================
-- 2. HABILITAR RLS EN LA TABLA
-- =============================================

-- Habilitar Row Level Security
ALTER TABLE [NOMBRE_TABLA] ENABLE ROW LEVEL SECURITY;

-- =============================================
-- 3. POLÍTICA PRINCIPAL: SERVICE_ROLE (BACKEND)
-- =============================================
-- CRÍTICO: Backend FastAPI debe tener acceso completo

-- Eliminar policy existente si existe
DROP POLICY IF EXISTS "service_role_full_access_[NOMBRE_TABLA]" ON [NOMBRE_TABLA];

-- Crear policy completa para service_role
CREATE POLICY "service_role_full_access_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
FOR ALL 
TO service_role
USING (true)           -- Puede leer cualquier registro
WITH CHECK (true);     -- Puede insertar/actualizar cualquier registro

-- =============================================
-- 4. POLÍTICAS PARA AUTHENTICATED USERS
-- =============================================

-- OPCIÓN A: Acceso completo de lectura
-- Usar para catálogos, lookups, datos públicos
DROP POLICY IF EXISTS "authenticated_read_all_[NOMBRE_TABLA]" ON [NOMBRE_TABLA];

CREATE POLICY "authenticated_read_all_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
FOR SELECT 
TO authenticated
USING (true);  -- Todos los registros visibles

-- OPCIÓN B: Acceso filtrado por condición business
-- Usar para datos sensibles con reglas específicas
-- DROP POLICY IF EXISTS "authenticated_read_filtered_[NOMBRE_TABLA]" ON [NOMBRE_TABLA];

-- CREATE POLICY "authenticated_read_filtered_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
-- FOR SELECT 
-- TO authenticated
-- USING (
--     -- Solo registros activos
--     estado_activo = true 
--     -- O solo registros del usuario actual
--     -- OR creado_por = auth.uid()
--     -- O solo registros públicos
--     -- OR visibilidad = 'publico'
-- );

-- OPCIÓN C: Acceso basado en roles de usuario
-- Requiere tabla usuarios con roles
-- DROP POLICY IF EXISTS "authenticated_role_based_[NOMBRE_TABLA]" ON [NOMBRE_TABLA];

-- CREATE POLICY "authenticated_role_based_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
-- FOR SELECT 
-- TO authenticated
-- USING (
--     EXISTS (
--         SELECT 1 FROM usuarios u
--         WHERE u.id = auth.uid()
--         AND u.rol IN ('admin', 'medico', 'enfermero')
--     )
--     -- Además de condiciones específicas del registro
--     AND estado_activo = true
-- );

-- =============================================
-- 5. POLÍTICAS PARA INSERCIÓN (AUTHENTICATED)
-- =============================================

-- OPCIÓN A: Inserción libre (para catálogos, logs)
-- DROP POLICY IF EXISTS "authenticated_insert_[NOMBRE_TABLA]" ON [NOMBRE_TABLA];

-- CREATE POLICY "authenticated_insert_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
-- FOR INSERT 
-- TO authenticated
-- WITH CHECK (true);

-- OPCIÓN B: Inserción con validaciones business
DROP POLICY IF EXISTS "authenticated_insert_validated_[NOMBRE_TABLA]" ON [NOMBRE_TABLA];

CREATE POLICY "authenticated_insert_validated_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
FOR INSERT 
TO authenticated
WITH CHECK (
    -- Solo puede insertar si es usuario válido
    auth.uid() IS NOT NULL
    -- Y cumple condiciones específicas
    -- AND campo_requerido IS NOT NULL
    -- AND campo_requerido != ''
);

-- =============================================
-- 6. POLÍTICAS PARA ACTUALIZACIÓN (AUTHENTICATED)
-- =============================================

-- OPCIÓN A: Actualización propia (usuario solo sus registros)
-- DROP POLICY IF EXISTS "authenticated_update_own_[NOMBRE_TABLA]" ON [NOMBRE_TABLA];

-- CREATE POLICY "authenticated_update_own_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
-- FOR UPDATE 
-- TO authenticated
-- USING (creado_por = auth.uid())           -- Solo los que creó
-- WITH CHECK (actualizado_por = auth.uid()); -- Solo puede poner su ID

-- OPCIÓN B: Actualización con validaciones business
DROP POLICY IF EXISTS "authenticated_update_validated_[NOMBRE_TABLA]" ON [NOMBRE_TABLA];

CREATE POLICY "authenticated_update_validated_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
FOR UPDATE 
TO authenticated
USING (
    -- Puede actualizar registros activos
    estado_activo = true
    -- Y que no estén bloqueados
    -- AND bloqueado_para_edicion = false
    -- O que sean suyos
    -- OR creado_por = auth.uid()
)
WITH CHECK (
    -- Las actualizaciones deben mantener integridad
    auth.uid() IS NOT NULL
    -- Y no pueden cambiar campos críticos (ejemplo)
    -- AND codigo_inmutable = codigo_inmutable  -- Evita cambio
);

-- =============================================
-- 7. POLÍTICAS PARA ELIMINACIÓN (AUTHENTICATED)
-- =============================================

-- OPCIÓN A: Solo soft delete (recomendado para datos críticos)
DROP POLICY IF EXISTS "authenticated_soft_delete_[NOMBRE_TABLA]" ON [NOMBRE_TABLA];

CREATE POLICY "authenticated_soft_delete_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
FOR UPDATE 
TO authenticated
USING (
    -- Solo puede "eliminar" (marcar inactivo) registros activos
    estado_activo = true
    AND creado_por = auth.uid()
)
WITH CHECK (
    -- La "eliminación" es cambiar estado
    estado_activo = false
    AND actualizado_por = auth.uid()
);

-- OPCIÓN B: Eliminación física (CUIDADO - solo para datos no críticos)
-- DROP POLICY IF EXISTS "authenticated_delete_[NOMBRE_TABLA]" ON [NOMBRE_TABLA];

-- CREATE POLICY "authenticated_delete_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
-- FOR DELETE 
-- TO authenticated
-- USING (
--     -- Solo puede eliminar registros propios
--     creado_por = auth.uid()
--     -- Y que no estén referenciados
--     AND NOT EXISTS (SELECT 1 FROM tabla_dependiente WHERE fk_id = id)
-- );

-- =============================================
-- 8. POLÍTICAS PARA ANONYMOUS USERS
-- =============================================

-- OPCIÓN A: Sin acceso (más seguro - recomendado para datos sensibles)
-- No crear políticas para anon = sin acceso

-- OPCIÓN B: Solo lectura muy limitada (para datos públicos)
-- DROP POLICY IF EXISTS "anon_read_public_[NOMBRE_TABLA]" ON [NOMBRE_TABLA];

-- CREATE POLICY "anon_read_public_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
-- FOR SELECT 
-- TO anon
-- USING (
--     -- Solo registros marcados como públicos
--     visibilidad_publica = true
--     AND estado_activo = true
--     -- Con datos no sensibles únicamente
-- );

-- =============================================
-- 9. GRANTS EXPLÍCITOS (COMPLEMENTA RLS)
-- =============================================

-- Service role necesita grants explícitos además de policies
GRANT ALL ON [NOMBRE_TABLA] TO service_role;
GRANT ALL ON [NOMBRE_TABLA] TO postgres;

-- Authenticated users - grants según necesidad
GRANT SELECT ON [NOMBRE_TABLA] TO authenticated;
GRANT INSERT ON [NOMBRE_TABLA] TO authenticated;
GRANT UPDATE ON [NOMBRE_TABLA] TO authenticated;
-- GRANT DELETE ON [NOMBRE_TABLA] TO authenticated; -- Solo si permite eliminación física

-- Anonymous - grants mínimos (solo si hay policy anon)
-- GRANT SELECT ON [NOMBRE_TABLA] TO anon;

-- =============================================
-- 10. POLÍTICAS ESPECIALES POR CONTEXTO
-- =============================================

-- CONTEXTO MÉDICO: Acceso basado en especialidad
-- CREATE POLICY "medico_specialty_access_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
-- FOR SELECT 
-- TO authenticated
-- USING (
--     EXISTS (
--         SELECT 1 FROM medicos m
--         WHERE m.usuario_id = auth.uid()
--         AND (
--             m.especialidad = 'general'  -- Médico general ve todo
--             OR m.especialidad = especialidad_requerida  -- Especialista ve su área
--         )
--     )
-- );

-- CONTEXTO COMPLIANCE: Acceso solo a datos propios centro médico
-- CREATE POLICY "center_based_access_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
-- FOR ALL
-- TO authenticated
-- USING (
--     centro_medico_id IN (
--         SELECT centro_id FROM usuarios_centros 
--         WHERE usuario_id = auth.uid()
--     )
-- )
-- WITH CHECK (
--     centro_medico_id IN (
--         SELECT centro_id FROM usuarios_centros 
--         WHERE usuario_id = auth.uid()
--     )
-- );

-- CONTEXTO PACIENTES: Solo acceso a sus propios datos
-- CREATE POLICY "patient_own_data_[NOMBRE_TABLA]" ON [NOMBRE_TABLA]
-- FOR SELECT
-- TO authenticated
-- USING (
--     -- Paciente ve solo sus datos
--     paciente_id = (
--         SELECT p.id FROM pacientes p 
--         WHERE p.usuario_id = auth.uid()
--     )
--     -- O médico ve pacientes asignados
--     OR EXISTS (
--         SELECT 1 FROM medico_paciente_asignacion mpa
--         WHERE mpa.paciente_id = paciente_id
--         AND mpa.medico_id = (
--             SELECT m.id FROM medicos m 
--             WHERE m.usuario_id = auth.uid()
--         )
--     )
-- );

-- =============================================
-- 11. VERIFICACIONES POST-EJECUCIÓN
-- =============================================

DO $verification$
DECLARE
    rls_enabled BOOLEAN;
    policy_count INTEGER;
    service_role_policies INTEGER;
    authenticated_policies INTEGER;
    anon_policies INTEGER;
BEGIN
    -- Verificar RLS habilitado
    SELECT EXISTS (
        SELECT FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'public'
        AND c.relname = '[NOMBRE_TABLA]'
        AND c.relrowsecurity = true
    ) INTO rls_enabled;
    
    -- Contar políticas por rol
    SELECT COUNT(*) INTO policy_count
    FROM pg_policies 
    WHERE tablename = '[NOMBRE_TABLA]' AND schemaname = 'public';
    
    SELECT COUNT(*) INTO service_role_policies
    FROM pg_policies 
    WHERE tablename = '[NOMBRE_TABLA]' AND schemaname = 'public'
    AND 'service_role' = ANY(roles);
    
    SELECT COUNT(*) INTO authenticated_policies
    FROM pg_policies 
    WHERE tablename = '[NOMBRE_TABLA]' AND schemaname = 'public'
    AND 'authenticated' = ANY(roles);
    
    SELECT COUNT(*) INTO anon_policies
    FROM pg_policies 
    WHERE tablename = '[NOMBRE_TABLA]' AND schemaname = 'public'
    AND 'anon' = ANY(roles);
    
    -- Log resultados verificación
    RAISE NOTICE '=== VERIFICACIÓN RLS [NOMBRE_TABLA] ===';
    RAISE NOTICE 'RLS habilitado: %', rls_enabled;
    RAISE NOTICE 'Total políticas: %', policy_count;
    RAISE NOTICE 'Políticas service_role: % (esperado: ≥1)', service_role_policies;
    RAISE NOTICE 'Políticas authenticated: %', authenticated_policies;
    RAISE NOTICE 'Políticas anonymous: %', anon_policies;
    
    -- Test básico de acceso (simulado)
    RAISE NOTICE '🧪 Testing policy access...';
    
    -- Validación final
    IF rls_enabled AND service_role_policies >= 1 THEN
        RAISE NOTICE '✅ SUCCESS: RLS configurado correctamente';
        RAISE NOTICE 'Backend access: GARANTIZADO (service_role)';
        
        IF authenticated_policies > 0 THEN
            RAISE NOTICE 'User access: CONFIGURADO (authenticated)';
        ELSE
            RAISE NOTICE 'User access: BLOQUEADO (sin policies authenticated)';
        END IF;
        
        IF anon_policies > 0 THEN
            RAISE NOTICE 'Anonymous access: PERMITIDO (⚠️  verificar si es intencional)';
        ELSE
            RAISE NOTICE 'Anonymous access: BLOQUEADO (recomendado)';
        END IF;
    ELSE
        RAISE EXCEPTION '❌ ERROR: RLS configuración incompleta';
    END IF;
    
    RAISE NOTICE '==========================================';
END;
$verification$;

COMMIT;

-- =============================================
-- NOTAS DE USO DEL TEMPLATE
-- =============================================
/*
INSTRUCCIONES DE USO:

1. REEMPLAZAR PLACEHOLDERS:
   - [NOMBRE_TABLA]: Tabla donde aplicar RLS
   - [DD mes AAAA]: Fecha actual
   - [Tu nombre]: Tu nombre o equipo

2. SELECCIONAR OPCIONES SEGÚN CONTEXTO:
   - Uncomment las políticas que apliquen a tu caso
   - Personalizar condiciones USING y WITH CHECK
   - Ajustar roles según modelo de seguridad

3. MODELOS DE SEGURIDAD TÍPICOS:

   PÚBLICO (CATÁLOGOS):
   - Service role: acceso completo
   - Authenticated: lectura completa
   - Anonymous: lectura limitada o bloqueado

   SENSIBLE (PACIENTES):
   - Service role: acceso completo
   - Authenticated: solo datos propios o asignados
   - Anonymous: bloqueado completo

   OPERACIONAL (LOGS, AUDITORÍA):
   - Service role: acceso completo
   - Authenticated: solo inserción/lectura propia
   - Anonymous: bloqueado completo

4. TESTING DE POLÍTICAS:
   -- En psql:
   SET ROLE service_role;
   SELECT COUNT(*) FROM [NOMBRE_TABLA];  -- Debe funcionar

   SET ROLE authenticated;  
   SELECT COUNT(*) FROM [NOMBRE_TABLA];  -- Según policy

   SET ROLE anon;
   SELECT COUNT(*) FROM [NOMBRE_TABLA];  -- Según policy

5. CONSIDERACIONES PERFORMANCE:
   - Políticas complejas pueden impactar performance
   - Usar índices en columnas referenciadas en policies
   - Evitar subconsultas costosas en USING/WITH CHECK
   - Test performance con datos reales

6. DEBUGGING POLÍTICAS:
   -- Ver políticas aplicadas:
   SELECT schemaname, tablename, policyname, cmd, roles, qual, with_check
   FROM pg_policies 
   WHERE tablename = '[NOMBRE_TABLA]';

   -- Test específico de policy:
   EXPLAIN (ANALYZE, BUFFERS) 
   SELECT * FROM [NOMBRE_TABLA] LIMIT 10;

7. PATRONES COMUNES:

   OWNERSHIP (creado_por):
   USING (creado_por = auth.uid())

   ROLE-BASED:
   USING (EXISTS (SELECT 1 FROM usuarios WHERE id = auth.uid() AND rol = 'admin'))

   CENTER/ORGANIZATION:
   USING (centro_id IN (SELECT centro_id FROM user_centers WHERE user_id = auth.uid()))

   TIME-BASED:
   USING (fecha_vigencia >= NOW() AND fecha_vencimiento <= NOW())

   STATUS-BASED:
   USING (activo = true AND aprobado = true)

   HIERARCHICAL:
   USING (nivel_acceso <= (SELECT nivel FROM usuarios WHERE id = auth.uid()))

8. ERRORES COMUNES A EVITAR:
   - Olvidar policy para service_role (backend falla)
   - Policies muy restrictivas (usuarios no pueden trabajar)
   - Policies muy permisivas (riesgo seguridad)
   - No considerar performance de subconsultas
   - Inconsistencia entre USING y WITH CHECK

9. BACKUP ANTES DE APLICAR:
   -- Backup políticas existentes:
   pg_dump --schema-only --table=[NOMBRE_TABLA] database > rls_backup.sql
*/