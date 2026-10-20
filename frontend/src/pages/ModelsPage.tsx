import React, { useEffect, useState } from 'react';
import { apiClient } from '../services/api';
import { ModelMetadata } from '../types';
import { Cpu, CheckCircle2, XCircle, Database } from 'lucide-react';

export const ModelsPage: React.FC = () => {
  const [models, setModels] = useState<ModelMetadata[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await apiClient.get('/api/v1/models/status');
        setModels(res.data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchStatus();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-800">ML Model Registry & Telemetry</h2>
        <p className="text-slate-500 text-sm">Real-time status of locally trained, serialized (.pkl) machine learning pipelines.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {models.map((m) => (
          <div key={m.model_name} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="p-2 bg-slate-100 rounded-lg text-slate-700">
                  <Cpu className="w-5 h-5" />
                </div>
                <h3 className="font-semibold text-slate-900 text-sm">{m.model_name}</h3>
              </div>
              {m.is_trained ? (
                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-emerald-100 text-emerald-800">
                  <CheckCircle2 className="w-3.5 h-3.5 mr-1" /> Ready
                </span>
              ) : (
                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-red-100 text-red-800">
                  <XCircle className="w-3.5 h-3.5 mr-1" /> Not Trained
                </span>
              )}
            </div>

            <div className="text-xs space-y-1.5 text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-100">
              <p><span className="font-medium text-slate-700">Algorithm:</span> {m.algorithm || "N/A"}</p>
              <p><span className="font-medium text-slate-700">Version:</span> {m.version || "N/A"}</p>
              <p><span className="font-medium text-slate-700">Samples:</span> {m.sample_count || "N/A"}</p>
              <p><span className="font-medium text-slate-700">Trained At:</span> {m.trained_at ? new Date(m.trained_at).toLocaleDateString() : "N/A"}</p>
            </div>

            <p className="text-[11px] text-slate-400">
              <span className="font-semibold text-slate-500">Provenance:</span> {m.provenance || "Synthetic benchmark"}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};
