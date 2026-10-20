import React, { useState } from 'react';
import { apiClient } from '../services/api';
import { TrustScoreResponse } from '../types';
import { Award, ShieldCheck, CheckCircle } from 'lucide-react';

export const TrustPage: React.FC = () => {
  const [regularity, setRegularity] = useState('98');
  const [stability, setStability] = useState('36');
  const [dti, setDti] = useState('22');
  const [savingsConsistency, setSavingsConsistency] = useState('0.85');
  const [accountAge, setAccountAge] = useState('6.5');

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<TrustScoreResponse | null>(null);

  const handleScore = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await apiClient.post('/api/v1/trust/score', {
        payment_regularity_pct: parseFloat(regularity) || 0,
        income_stability_months: parseInt(stability) || 0,
        monthly_dti_pct: parseFloat(dti) || 0,
        savings_consistency_score: parseFloat(savingsConsistency) || 0,
        account_age_years: parseFloat(accountAge) || 0
      });
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
        <h2 className="text-2xl font-bold text-slate-800">Alternative-Data Trust Score</h2>
        <p className="text-slate-500 text-sm">Empowering financial inclusion by deriving behavioral creditworthiness from consented alternative data points.</p>
      </div>

      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <form onSubmit={handleScore} className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-semibold text-slate-600">On-Time Payment Regularity (%)</label>
            <input
              type="number"
              value={regularity}
              onChange={(e) => setRegularity(e.target.value)}
              className="w-full mt-1 px-3 py-2 border border-slate-300 rounded-lg text-sm"
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-slate-600">Income Stability (Months Continuous)</label>
            <input
              type="number"
              value={stability}
              onChange={(e) => setStability(e.target.value)}
              className="w-full mt-1 px-3 py-2 border border-slate-300 rounded-lg text-sm"
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-slate-600">Debt-to-Income Ratio (%)</label>
            <input
              type="number"
              value={dti}
              onChange={(e) => setDti(e.target.value)}
              className="w-full mt-1 px-3 py-2 border border-slate-300 rounded-lg text-sm"
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-slate-600">Savings Consistency Score (0.0 - 1.0)</label>
            <input
              type="number"
              step="0.05"
              value={savingsConsistency}
              onChange={(e) => setSavingsConsistency(e.target.value)}
              className="w-full mt-1 px-3 py-2 border border-slate-300 rounded-lg text-sm"
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-slate-600">Banking Account Age (Years)</label>
            <input
              type="number"
              step="0.5"
              value={accountAge}
              onChange={(e) => setAccountAge(e.target.value)}
              className="w-full mt-1 px-3 py-2 border border-slate-300 rounded-lg text-sm"
            />
          </div>
          <div className="flex items-end">
            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-medium text-sm transition-colors"
            >
              {loading ? "Evaluating Logistic Regression..." : "Evaluate Trust Score"}
            </button>
          </div>
        </form>
      </div>

      {result && (
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <p className="text-xs text-slate-500 font-semibold uppercase">Calibrated Trust Rating</p>
              <p className="text-4xl font-extrabold text-slate-900 mt-1">{result.trust_score} <span className="text-sm text-slate-400 font-normal">/ 850</span></p>
            </div>
            <div>
              <span className="inline-flex items-center px-4 py-1.5 rounded-full text-sm font-bold bg-emerald-100 text-emerald-800">
                <ShieldCheck className="w-4 h-4 mr-1.5" />
                {result.risk_category} TIER
              </span>
            </div>
          </div>

          <div>
            <h4 className="text-xs font-semibold text-slate-700 mb-2">Contributing Factors</h4>
            <div className="space-y-2">
              {result.contributing_factors.map((f, i) => (
                <div key={i} className="p-2.5 bg-slate-50 border border-slate-200 rounded text-xs text-slate-700 flex items-center">
                  <CheckCircle className="w-3.5 h-3.5 text-emerald-600 mr-2 flex-shrink-0" />
                  {f}
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
