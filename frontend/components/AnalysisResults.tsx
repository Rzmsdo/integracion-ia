'use client';

import { type AnalysisResult } from '@/lib/api';

interface AnalysisResultsProps {
  result: AnalysisResult;
}

export default function AnalysisResults({ result }: AnalysisResultsProps) {
  if (!result.success) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-red-800 mb-2">❌ Error</h3>
        <p className="text-red-600">{result.error || result.detail}</p>
      </div>
    );
  }

  const { analysis, statistics, filename, file_size, file_type, analysis_id } = result;

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
      {/* Header */}
      <div className="border-b pb-4">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          ✅ Análisis Completado
        </h2>
        <div className="flex flex-wrap gap-4 text-sm text-gray-600">
          <span>📄 {filename}</span>
          <span>📊 {file_size ? `${(file_size / 1024).toFixed(2)} KB` : ''}</span>
          <span>🏷️ {file_type}</span>
          {analysis_id && (
            <span className="text-xs text-gray-400">ID: {analysis_id.substring(0, 8)}...</span>
          )}
        </div>
      </div>

      {/* Estadísticas */}
      {statistics && (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <StatCard
            icon="📝"
            label="Palabras"
            value={statistics.word_count}
          />
          <StatCard
            icon="🔤"
            label="Caracteres"
            value={statistics.character_count}
          />
          <StatCard
            icon="📋"
            label="Oraciones"
            value={statistics.sentence_count}
          />
          <StatCard
            icon="📑"
            label="Párrafos"
            value={statistics.paragraph_count}
          />
          <StatCard
            icon="📏"
            label="Prom. Palabra"
            value={statistics.average_word_length.toFixed(1)}
          />
          <StatCard
            icon="📐"
            label="Prom. Oración"
            value={statistics.average_sentence_length.toFixed(1)}
          />
        </div>
      )}

      {/* Tipo de Análisis */}
      {analysis && (
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full font-medium">
              {analysis.type}
            </span>
            {analysis.metadata?.model_used && (
              <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full font-medium">
                🤖 {analysis.metadata.model_used}
              </span>
            )}
          </div>

          {/* Resumen */}
          {analysis.summary && (
            <AnalysisSection
              title="📝 Resumen"
              content={analysis.summary}
              bgColor="bg-blue-50"
              borderColor="border-blue-200"
            />
          )}

          {/* Puntos Clave */}
          {analysis.key_points && (
            <AnalysisSection
              title="🎯 Puntos Clave"
              content={analysis.key_points}
              bgColor="bg-green-50"
              borderColor="border-green-200"
            />
          )}

          {/* Sentimiento */}
          {analysis.sentiment && (
            <AnalysisSection
              title="💭 Análisis de Sentimiento"
              content={analysis.sentiment}
              bgColor="bg-purple-50"
              borderColor="border-purple-200"
            />
          )}

          {/* Entidades */}
          {analysis.entities && (
            <div className="border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-800 mb-2">🏷️ Entidades</h3>
              <pre className="text-sm text-gray-700 overflow-x-auto">
                {JSON.stringify(analysis.entities, null, 2)}
              </pre>
            </div>
          )}

          {/* Preguntas */}
          {analysis.questions && (
            <div className="border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-800 mb-2">❓ Preguntas</h3>
              <pre className="text-sm text-gray-700 overflow-x-auto">
                {JSON.stringify(analysis.questions, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function StatCard({ icon, label, value }: { icon: string; label: string; value: number | string }) {
  return (
    <div className="bg-gray-50 rounded-lg p-4 text-center">
      <div className="text-2xl mb-1">{icon}</div>
      <div className="text-2xl font-bold text-gray-900">{value}</div>
      <div className="text-xs text-gray-600">{label}</div>
    </div>
  );
}

function AnalysisSection({
  title,
  content,
  bgColor,
  borderColor,
}: {
  title: string;
  content: string;
  bgColor: string;
  borderColor: string;
}) {
  return (
    <div className={`${bgColor} border ${borderColor} rounded-lg p-4`}>
      <h3 className="font-semibold text-gray-800 mb-3">{title}</h3>
      <div className="text-gray-700 whitespace-pre-wrap leading-relaxed">
        {content}
      </div>
    </div>
  );
}
