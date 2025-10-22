'use client';

import { useState, useRef } from 'react';
import { analyzeDocument, type AnalysisResult } from '@/lib/api';

interface FileUploadProps {
  onAnalysisComplete: (result: AnalysisResult) => void;
  userId: string;
}

export default function FileUpload({ onAnalysisComplete, userId }: FileUploadProps) {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [analysisType, setAnalysisType] = useState('comprehensive');
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const analysisTypes = [
    { value: 'comprehensive', label: 'Análisis Completo', description: 'Resumen, puntos clave y sentimiento' },
    { value: 'summary', label: 'Resumen', description: 'Solo un resumen del documento' },
    { value: 'key_points', label: 'Puntos Clave', description: 'Extrae los puntos principales' },
    { value: 'sentiment', label: 'Sentimiento', description: 'Analiza el tono del texto' },
    { value: 'general', label: 'General', description: 'Análisis general del contenido' },
  ];

  const allowedExtensions = ['.pdf', '.txt', '.docx', '.md', '.doc'];
  const maxFileSize = 10 * 1024 * 1024; // 10MB

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (file: File) => {
    setError(null);

    // Validar extensión
    const extension = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!allowedExtensions.includes(extension)) {
      setError(`Formato no soportado. Usa: ${allowedExtensions.join(', ')}`);
      return;
    }

    // Validar tamaño
    if (file.size > maxFileSize) {
      setError('El archivo es demasiado grande. Máximo 10MB.');
      return;
    }

    setSelectedFile(file);
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Por favor selecciona un archivo');
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    try {
      const result = await analyzeDocument(selectedFile, analysisType, userId);
      onAnalysisComplete(result);
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al analizar el documento');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">
        📄 Subir Documento
      </h2>

      {/* Zona de arrastre */}
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept={allowedExtensions.join(',')}
          onChange={handleFileInputChange}
          className="hidden"
          id="file-upload"
        />
        
        <label
          htmlFor="file-upload"
          className="cursor-pointer flex flex-col items-center"
        >
          <svg
            className="w-16 h-16 text-gray-400 mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
          
          {selectedFile ? (
            <div className="space-y-2">
              <p className="text-lg font-medium text-gray-900">{selectedFile.name}</p>
              <p className="text-sm text-gray-500">
                {(selectedFile.size / 1024).toFixed(2)} KB
              </p>
              <button
                type="button"
                onClick={(e) => {
                  e.preventDefault();
                  setSelectedFile(null);
                  if (fileInputRef.current) fileInputRef.current.value = '';
                }}
                className="text-sm text-red-600 hover:text-red-800"
              >
                Eliminar
              </button>
            </div>
          ) : (
            <>
              <p className="text-lg font-medium text-gray-700 mb-2">
                Arrastra un archivo aquí o haz clic para seleccionar
              </p>
              <p className="text-sm text-gray-500">
                PDF, DOCX, TXT, MD (máx. 10MB)
              </p>
            </>
          )}
        </label>
      </div>

      {/* Selector de tipo de análisis */}
      <div className="mt-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Tipo de Análisis
        </label>
        <select
          value={analysisType}
          onChange={(e) => setAnalysisType(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          disabled={isAnalyzing}
        >
          {analysisTypes.map((type) => (
            <option key={type.value} value={type.value}>
              {type.label} - {type.description}
            </option>
          ))}
        </select>
      </div>

      {/* Error */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Botón de análisis */}
      <button
        onClick={handleAnalyze}
        disabled={!selectedFile || isAnalyzing}
        className={`mt-6 w-full py-3 px-6 rounded-lg font-medium text-white transition-colors ${
          !selectedFile || isAnalyzing
            ? 'bg-gray-300 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700 active:bg-blue-800'
        }`}
      >
        {isAnalyzing ? (
          <span className="flex items-center justify-center">
            <svg
              className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
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
            Analizando...
          </span>
        ) : (
          '🚀 Analizar Documento'
        )}
      </button>
    </div>
  );
}
