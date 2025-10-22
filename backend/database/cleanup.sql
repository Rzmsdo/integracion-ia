-- ===========================================
-- LIMPIEZA Y RECREACIÓN COMPLETA DEL SCHEMA
-- ===========================================
-- PASO 1: Ejecuta este SQL primero para limpiar todo
-- PASO 2: Luego ejecuta el schema.sql completo

-- Eliminar vistas (deben ir primero)
DROP VIEW IF EXISTS document_analyses_view CASCADE;
DROP VIEW IF EXISTS user_stats_view CASCADE;

-- Eliminar funciones
DROP FUNCTION IF EXISTS cleanup_old_analyses(INTEGER) CASCADE;
DROP FUNCTION IF EXISTS get_user_statistics(VARCHAR) CASCADE;
DROP FUNCTION IF EXISTS update_user_statistics() CASCADE;
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- Eliminar tablas (en orden inverso por las foreign keys)
DROP TABLE IF EXISTS analysis_statistics CASCADE;
DROP TABLE IF EXISTS analyses CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Verificar que todo se eliminó
SELECT 
    schemaname,
    tablename
FROM pg_tables
WHERE schemaname = 'public'
    AND tablename IN ('users', 'documents', 'analyses', 'analysis_statistics');

-- Si la query anterior no devuelve filas, está limpio ✓
-- Ahora ejecuta el schema.sql completo
