'use client';

import { useState } from 'react';
import FileUpload from '@/components/FileUpload';
import AnalysisResults from '@/components/AnalysisResults';
import AnalysisHistory from '@/components/AnalysisHistory';
import SystemStatus from '@/components/SystemStatus';
import { type AnalysisResult } from '@/lib/api';

export default function Home() {
  const [currentResult, setCurrentResult] = useState<AnalysisResult | null>(null);
  const [userId, setUserId] = useState('demo_user');
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleAnalysisComplete = (result: AnalysisResult) => {
    setCurrentResult(result);
    setRefreshTrigger(prev => prev + 1); // Trigger refresh del historial
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                🤖 Document Analyzer
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                Análisis inteligente de documentos con IA
              </p>
            </div>
            
            {/* Selector de usuario */}
            <div className="flex items-center gap-3">
              <label className="text-sm font-medium text-gray-700">
                Usuario:
              </label>
              <input
                type="text"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="ID de usuario"
              />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Estado del Sistema */}
        <div className="mb-6">
          <SystemStatus />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Columna Izquierda: Upload y Resultados */}
          <div className="space-y-6">
            <FileUpload
              onAnalysisComplete={handleAnalysisComplete}
              userId={userId}
            />
            
            {currentResult && (
              <AnalysisResults result={currentResult} />
            )}
          </div>

          {/* Columna Derecha: Historial */}
          <div>
            <AnalysisHistory
              userId={userId}
              refreshTrigger={refreshTrigger}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between text-sm text-gray-600">
            <p>
              Powered by <strong>Ollama</strong> + <strong>Next.js</strong> + <strong>Supabase</strong>
            </p>
            <div className="flex gap-4">
              <a href="http://localhost:8000/api/v1/docs" target="_blank" rel="noopener noreferrer" className="hover:text-blue-600">
                📚 API Docs
              </a>
              <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="hover:text-blue-600">
                🔗 GitHub
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
