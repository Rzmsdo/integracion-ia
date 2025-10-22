/**
 * API Client para conectar con el backend FastAPI
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface AnalysisResult {
  success: boolean;
  message?: string;
  filename?: string;
  file_size?: number;
  file_type?: string;
  analysis?: {
    type: string;
    summary?: string;
    key_points?: string;
    sentiment?: string;
    entities?: any;
    questions?: any;
    metadata?: {
      text_length?: number;
      word_count?: number;
      char_count?: number;
      model_used?: string;
      analyzed_at?: string;
    };
  };
  analysis_id?: string;
  statistics?: {
    character_count: number;
    word_count: number;
    sentence_count: number;
    paragraph_count: number;
    average_word_length: number;
    average_sentence_length: number;
  };
  error?: string;
  detail?: string;
}

export interface SavedAnalysis {
  id: string;
  user_id: string;
  document_name: string;
  analysis_type: string;
  created_at: string;
  metadata: {
    model_used?: string;
    file_size?: number;
    file_type?: string;
    word_count?: number;
  };
}

export interface AnalysisListResponse {
  success: boolean;
  total: number;
  analyses: SavedAnalysis[];
}

export interface HealthResponse {
  status: string;
  ollama_available: boolean;
  supabase_connected: boolean;
  timestamp: string;
}

/**
 * Analizar un documento
 */
export async function analyzeDocument(
  file: File,
  analysisType: string = 'comprehensive',
  userId: string = 'demo_user'
): Promise<AnalysisResult> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('analysis_type', analysisType);
  formData.append('user_id', userId);

  const response = await fetch(`${API_BASE_URL}/documents/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Error analizando documento');
  }

  return response.json();
}

/**
 * Obtener historial de análisis de un usuario
 */
export async function getUserAnalyses(
  userId: string = 'demo_user',
  limit: number = 10,
  offset: number = 0
): Promise<AnalysisListResponse> {
  const params = new URLSearchParams({
    user_id: userId,
    limit: limit.toString(),
    offset: offset.toString(),
  });

  const response = await fetch(`${API_BASE_URL}/documents/analyses?${params}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Error obteniendo análisis');
  }

  return response.json();
}

/**
 * Verificar estado del sistema
 */
export async function checkHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/system/health`);

  if (!response.ok) {
    throw new Error('Error verificando estado del sistema');
  }

  return response.json();
}

/**
 * Obtener información del sistema
 */
export async function getSystemInfo(): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/system/info`);

  if (!response.ok) {
    throw new Error('Error obteniendo información del sistema');
  }

  return response.json();
}
