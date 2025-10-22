'use client';

import { useState, useEffect } from 'react';
import { checkHealth, type HealthResponse } from '@/lib/api';

export default function SystemStatus() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadHealth();
    const interval = setInterval(loadHealth, 30000); // Actualizar cada 30s
    return () => clearInterval(interval);
  }, []);

  const loadHealth = async () => {
    try {
      const response = await checkHealth();
      setHealth(response);
    } catch (err) {
      setHealth(null);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-4">
        <div className="animate-pulse flex space-x-4">
          <div className="flex-1 space-y-2">
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!health) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <div className="flex items-center gap-3">
          <span className="text-2xl">⚠️</span>
          <div>
            <p className="font-semibold text-red-800">Sistema Desconectado</p>
            <p className="text-sm text-red-600">No se puede conectar con el backend</p>
          </div>
        </div>
      </div>
    );
  }

  const isHealthy = health.status === 'healthy' && health.ollama_available;

  return (
    <div className={`rounded-lg shadow-lg p-4 ${isHealthy ? 'bg-green-50 border border-green-200' : 'bg-yellow-50 border border-yellow-200'}`}>
      <div className="flex items-center gap-3">
        <span className="text-2xl">{isHealthy ? '✅' : '⚠️'}</span>
        <div className="flex-1">
          <p className="font-semibold text-gray-800">Estado del Sistema</p>
          <div className="flex flex-wrap gap-3 text-sm mt-1">
            <StatusBadge
              label="Backend"
              active={health.status === 'healthy'}
            />
            <StatusBadge
              label="IA (Ollama)"
              active={health.ollama_available}
            />
            <StatusBadge
              label="Base de Datos"
              active={health.supabase_connected}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function StatusBadge({ label, active }: { label: string; active: boolean }) {
  return (
    <span className={`px-2 py-1 rounded text-xs font-medium ${
      active
        ? 'bg-green-100 text-green-800'
        : 'bg-gray-100 text-gray-600'
    }`}>
      {active ? '✓' : '○'} {label}
    </span>
  );
}
