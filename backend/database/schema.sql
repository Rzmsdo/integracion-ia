-- ===========================================
-- SCHEMA DE BASE DE DATOS - DOCUMENT ANALYZER
-- ===========================================
-- Este archivo contiene el esquema completo para Supabase
-- Ejecuta este SQL en el SQL Editor de tu proyecto Supabase

-- ===========================================
-- TABLA: users
-- Almacena información básica de usuarios
-- ===========================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255),
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Índice para búsquedas rápidas por user_id
CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id);

-- ===========================================
-- TABLA: documents
-- Almacena información de documentos procesados
-- ===========================================
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    filename VARCHAR(500) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size INTEGER NOT NULL,
    original_text TEXT,
    text_length INTEGER,
    word_count INTEGER,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Relación con users
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Índices para búsquedas y ordenamiento
CREATE INDEX IF NOT EXISTS idx_documents_user_id ON documents(user_id);
CREATE INDEX IF NOT EXISTS idx_documents_uploaded_at ON documents(uploaded_at DESC);
CREATE INDEX IF NOT EXISTS idx_documents_file_type ON documents(file_type);

-- ===========================================
-- TABLA: analyses
-- Almacena los resultados de análisis
-- ===========================================
CREATE TABLE IF NOT EXISTS analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    analysis_type VARCHAR(50) NOT NULL,
    
    -- Resultados del análisis
    summary TEXT,
    key_points TEXT,
    sentiment TEXT,
    entities JSONB,
    questions JSONB,
    
    -- Metadata del análisis
    model_used VARCHAR(100),
    processing_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Relaciones
    CONSTRAINT fk_document FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    CONSTRAINT fk_user_analysis FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Índices para búsquedas eficientes
CREATE INDEX IF NOT EXISTS idx_analyses_document_id ON analyses(document_id);
CREATE INDEX IF NOT EXISTS idx_analyses_user_id ON analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_analyses_type ON analyses(analysis_type);
CREATE INDEX IF NOT EXISTS idx_analyses_created_at ON analyses(created_at DESC);

-- Índice GIN para búsqueda en JSONB
CREATE INDEX IF NOT EXISTS idx_analyses_entities ON analyses USING GIN (entities);
CREATE INDEX IF NOT EXISTS idx_analyses_metadata ON analyses USING GIN (metadata);

-- ===========================================
-- TABLA: analysis_statistics
-- Almacena estadísticas agregadas
-- ===========================================
CREATE TABLE IF NOT EXISTS analysis_statistics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    total_documents INTEGER DEFAULT 0,
    total_analyses INTEGER DEFAULT 0,
    total_words_analyzed BIGINT DEFAULT 0,
    last_analysis_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT fk_user_stats FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT unique_user_stats UNIQUE (user_id)
);

CREATE INDEX IF NOT EXISTS idx_stats_user_id ON analysis_statistics(user_id);

-- ===========================================
-- FUNCIONES Y TRIGGERS
-- ===========================================

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para users
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para analysis_statistics
DROP TRIGGER IF EXISTS update_stats_updated_at ON analysis_statistics;
CREATE TRIGGER update_stats_updated_at
    BEFORE UPDATE ON analysis_statistics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Función para actualizar estadísticas después de insertar análisis
CREATE OR REPLACE FUNCTION update_user_statistics()
RETURNS TRIGGER AS $$
BEGIN
    -- Actualizar o crear estadísticas del usuario
    INSERT INTO analysis_statistics (user_id, total_analyses, last_analysis_at)
    VALUES (NEW.user_id, 1, NEW.created_at)
    ON CONFLICT (user_id) 
    DO UPDATE SET
        total_analyses = analysis_statistics.total_analyses + 1,
        last_analysis_at = NEW.created_at,
        updated_at = NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar estadísticas automáticamente
DROP TRIGGER IF EXISTS update_stats_on_analysis ON analyses;
CREATE TRIGGER update_stats_on_analysis
    AFTER INSERT ON analyses
    FOR EACH ROW
    EXECUTE FUNCTION update_user_statistics();

-- ===========================================
-- ROW LEVEL SECURITY (RLS)
-- Opcional: Descomentar si quieres habilitar RLS
-- ===========================================

-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE analyses ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE analysis_statistics ENABLE ROW LEVEL SECURITY;

-- Políticas de ejemplo (ajustar según necesidades)
-- CREATE POLICY "Users can view own data" ON users
--     FOR SELECT USING (user_id = current_setting('app.current_user_id'));

-- CREATE POLICY "Users can view own documents" ON documents
--     FOR SELECT USING (user_id = current_setting('app.current_user_id'));

-- CREATE POLICY "Users can view own analyses" ON analyses
--     FOR SELECT USING (user_id = current_setting('app.current_user_id'));

-- ===========================================
-- VISTAS ÚTILES
-- ===========================================

-- Vista combinada de documentos con sus análisis
CREATE OR REPLACE VIEW document_analyses_view AS
SELECT 
    d.id as document_id,
    d.user_id,
    d.filename,
    d.file_type,
    d.file_size,
    d.word_count,
    d.uploaded_at,
    a.id as analysis_id,
    a.analysis_type,
    a.summary,
    a.key_points,
    a.sentiment,
    a.model_used,
    a.created_at as analyzed_at
FROM documents d
LEFT JOIN analyses a ON a.document_id = d.id
ORDER BY d.uploaded_at DESC;

-- Vista de estadísticas por usuario
CREATE OR REPLACE VIEW user_stats_view AS
SELECT 
    u.user_id,
    u.name,
    u.email,
    COALESCE(s.total_documents, 0) as total_documents,
    COALESCE(s.total_analyses, 0) as total_analyses,
    COALESCE(s.total_words_analyzed, 0) as total_words_analyzed,
    s.last_analysis_at,
    u.created_at as user_since
FROM users u
LEFT JOIN analysis_statistics s ON u.user_id = s.user_id;

-- ===========================================
-- DATOS DE EJEMPLO (opcional)
-- ===========================================

-- Insertar usuario demo
INSERT INTO users (user_id, email, name) 
VALUES ('demo_user', 'demo@example.com', 'Demo User')
ON CONFLICT (user_id) DO NOTHING;

-- ===========================================
-- FUNCIONES DE UTILIDAD
-- ===========================================

-- Función para limpiar análisis antiguos (más de 90 días)
CREATE OR REPLACE FUNCTION cleanup_old_analyses(days_old INTEGER DEFAULT 90)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM analyses
    WHERE created_at < NOW() - (days_old || ' days')::INTERVAL;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Función para obtener estadísticas de un usuario
CREATE OR REPLACE FUNCTION get_user_statistics(p_user_id VARCHAR)
RETURNS TABLE (
    total_docs INTEGER,
    total_analyses INTEGER,
    avg_words_per_doc NUMERIC,
    most_used_analysis_type VARCHAR,
    last_activity TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(DISTINCT d.id)::INTEGER as total_docs,
        COUNT(a.id)::INTEGER as total_analyses,
        ROUND(AVG(d.word_count), 2) as avg_words_per_doc,
        (
            SELECT analysis_type 
            FROM analyses 
            WHERE user_id = p_user_id 
            GROUP BY analysis_type 
            ORDER BY COUNT(*) DESC 
            LIMIT 1
        ) as most_used_analysis_type,
        MAX(GREATEST(d.uploaded_at, a.created_at)) as last_activity
    FROM documents d
    LEFT JOIN analyses a ON a.document_id = d.id
    WHERE d.user_id = p_user_id;
END;
$$ LANGUAGE plpgsql;

-- ===========================================
-- COMENTARIOS EN TABLAS
-- ===========================================

COMMENT ON TABLE users IS 'Almacena información de usuarios del sistema';
COMMENT ON TABLE documents IS 'Documentos subidos por los usuarios';
COMMENT ON TABLE analyses IS 'Resultados de análisis de documentos con IA';
COMMENT ON TABLE analysis_statistics IS 'Estadísticas agregadas por usuario';

COMMENT ON COLUMN analyses.summary IS 'Resumen generado por IA del documento';
COMMENT ON COLUMN analyses.key_points IS 'Puntos clave extraídos del documento';
COMMENT ON COLUMN analyses.sentiment IS 'Análisis de sentimiento del texto';
COMMENT ON COLUMN analyses.entities IS 'Entidades nombradas extraídas (JSON)';
COMMENT ON COLUMN analyses.model_used IS 'Modelo de IA utilizado para el análisis';

-- ===========================================
-- FIN DEL SCHEMA
-- ===========================================

-- Verificar que todo se creó correctamente
SELECT 
    schemaname,
    tablename,
    tableowner
FROM pg_tables
WHERE schemaname = 'public'
    AND tablename IN ('users', 'documents', 'analyses', 'analysis_statistics')
ORDER BY tablename;
