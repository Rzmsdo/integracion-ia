'use client';

import { useState, useEffect } from 'react';
import { getUserAnalyses, type SavedAnalysis } from '@/lib/api';

interface AnalysisHistoryProps {
  userId: string;
  refreshTrigger?: number;
}

export default function AnalysisHistory({ userId, refreshTrigger }: AnalysisHistoryProps) {
  const [analyses, setAnalyses] = useState<SavedAnalysis[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadAnalyses();
  }, [userId, refreshTrigger]);

  const loadAnalyses = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await getUserAnalyses(userId, 20);
      setAnalyses(response.analyses);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error cargando historial');
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('es', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  };

  const getAnalysisTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      comprehensive: 'Completo',
      summary: 'Resumen',
      key_points: 'Puntos Clave',
      sentiment: 'Sentimiento',
      general: 'General',
    };
    return labels[type] || type;
  };

  const getAnalysisTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      comprehensive: 'bg-blue-100 text-blue-800',
      summary: 'bg-green-100 text-green-800',
      key_points: 'bg-yellow-100 text-yellow-800',
      sentiment: 'bg-purple-100 text-purple-800',
      general: 'bg-gray-100 text-gray-800',
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">📚 Historial</h2>
        <div className="flex items-center justify-center py-12">
          <svg
            className="animate-spin h-8 w-8 text-blue-600"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">📚 Historial</h2>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-600">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-gray-800">📚 Historial</h2>
        <button
          onClick={loadAnalyses}
          className="text-sm text-blue-600 hover:text-blue-800 font-medium"
        >
          🔄 Actualizar
        </button>
      </div>

      {analyses.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📭</div>
          <p className="text-gray-600">No hay análisis guardados aún</p>
          <p className="text-sm text-gray-500 mt-2">
            Sube un documento para comenzar
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          <p className="text-sm text-gray-600 mb-4">
            {analyses.length} análisis encontrados
          </p>
          {analyses.map((analysis) => (
            <div
              key={analysis.id}
              className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 hover:shadow-md transition-all"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-gray-900 truncate mb-1">
                    📄 {analysis.document_name}
                  </h3>
                  <div className="flex flex-wrap gap-2 text-xs text-gray-600 mb-2">
                    <span className={`px-2 py-1 rounded-full ${getAnalysisTypeColor(analysis.analysis_type)}`}>
                      {getAnalysisTypeLabel(analysis.analysis_type)}
                    </span>
                    {analysis.metadata.model_used && (
                      <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded-full">
                        🤖 {analysis.metadata.model_used}
                      </span>
                    )}
                  </div>
                  <div className="flex flex-wrap gap-3 text-xs text-gray-500">
                    <span>🕒 {formatDate(analysis.created_at)}</span>
                    {analysis.metadata.file_size && (
                      <span>📊 {(analysis.metadata.file_size / 1024).toFixed(1)} KB</span>
                    )}
                    {analysis.metadata.word_count && (
                      <span>📝 {analysis.metadata.word_count} palabras</span>
                    )}
                    {analysis.metadata.file_type && (
                      <span>🏷️ {analysis.metadata.file_type}</span>
                    )}
                  </div>
                </div>
                <button
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium shrink-0"
                  onClick={() => {
                    // TODO: Implementar ver detalles
                    alert(`Ver detalles de: ${analysis.document_name}`);
                  }}
                >
                  Ver →
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
