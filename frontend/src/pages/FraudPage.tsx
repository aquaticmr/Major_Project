import React, { useState } from 'react';
import { apiClient } from '../services/api';
import { URLFraudResponse } from '../types';
import { ShieldAlert, AlertTriangle, CheckCircle, Search } from 'lucide-react';

export const FraudPage: React.FC = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<URLFraudResponse | null>(null);

  const handleScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;

    setLoading(true);
    try {
      const res = await apiClient.post('/api/v1/fraud/analyze-url', { url });
      setResult(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h2 className="text-2xl font-bold text-slate-800">URL Threat Intel & Fraud Classifier</h2>
        <p className="text-slate-500 text-sm">Analyze financial portals and suspicious links using the locally trained Random Forest threat classifier.</p>
      </div>

      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <form onSubmit={handleScan} className="flex gap-3">
          <input
            type="text"
            placeholder="Paste URL to inspect (e.g., http://chase-bank-verify-account.xyz/auth)..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
          <button
            type="submit"
            disabled={loading || !url.trim()}
            className="px-6 py-2.5 bg-slate-900 hover:bg-slate-800 text-white rounded-lg font-medium text-sm transition-colors flex items-center disabled:opacity-50"
          >
            <Search className="w-4 h-4 mr-2" />
            {loading ? "Analyzing Features..." : "Analyze Link"}
          </button>
        </form>
      </div>

      {result && (
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <span className="text-xs font-semibold text-slate-500 uppercase">Assessment Result</span>
              <p className="font-mono text-xs text-slate-700 truncate max-w-lg mt-0.5">{result.url}</p>
            </div>
            <div className="flex items-center space-x-2">
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold ${
                result.risk_level === 'HIGH' ? 'bg-red-100 text-red-700' : (result.risk_level === 'MEDIUM' ? 'bg-amber-100 text-amber-700' : 'bg-emerald-100 text-emerald-700')
              }`}>
                {result.risk_level === 'HIGH' ? (
                  <ShieldAlert className="w-3.5 h-3.5 mr-1" />
                ) : (
                  <CheckCircle className="w-3.5 h-3.5 mr-1" />
                )}
                {result.risk_level} RISK
              </span>
              <span className="text-xs bg-slate-100 text-slate-800 px-2 py-1 rounded font-medium">
                Risk Probability: {(result.risk_score * 100).toFixed(1)}%
              </span>
            </div>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-slate-700 mb-2">Explanatory Threat Indicators</h4>
            <div className="space-y-2">
              {result.explanation_factors.map((factor, i) => (
                <div key={i} className="p-2.5 bg-slate-50 border border-slate-200 rounded text-xs text-slate-700 flex items-center">
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-400 mr-2" />
                  {factor}
                </div>
              ))}
            </div>
          </div>

          <p className="text-[11px] text-slate-400 mt-2 italic">{result.disclaimer}</p>
        </div>
      )}
    </div>
  );
};
