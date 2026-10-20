import React, { useState } from 'react';
import { apiClient } from '../services/api';
import { RAGResponse } from '../types';
import { Send, ShieldCheck, AlertTriangle, BookOpen, CheckCircle } from 'lucide-react';

export const RAGAssistantPage: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<RAGResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    try {
      const res = await apiClient.post('/api/v1/rag/query', { question });
      setResponse(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h2 className="text-2xl font-bold text-slate-800">Low-Hallucination Grounded RAG</h2>
        <p className="text-slate-500 text-sm">Query your documents with hybrid semantic/BM25 retrieval, numerical verification, and citation traceability.</p>
      </div>

      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            type="text"
            placeholder="Ask about interest rates, annual fees, penalties, or contractual terms..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
          <button
            type="submit"
            disabled={loading || !question.trim()}
            className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-medium text-sm transition-colors flex items-center disabled:opacity-50"
          >
            <Send className="w-4 h-4 mr-2" />
            {loading ? "Searching & Verifying..." : "Ask Co-Pilot"}
          </button>
        </form>
      </div>

      {response && (
        <div className="space-y-4">
          {/* Main Answer Box */}
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <span className="text-xs font-semibold text-slate-500 uppercase">Verified Co-Pilot Answer</span>
              <div className="flex items-center space-x-2">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  response.verification_status === 'VERIFIED' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                }`}>
                  {response.verification_status === 'VERIFIED' ? (
                    <CheckCircle className="w-3.5 h-3.5 mr-1" />
                  ) : (
                    <AlertTriangle className="w-3.5 h-3.5 mr-1" />
                  )}
                  {response.verification_status}
                </span>
                <span className="text-xs font-medium bg-slate-100 text-slate-700 px-2 py-0.5 rounded">
                  Evidence Score: {(response.evidence_score * 100).toFixed(0)}%
                </span>
              </div>
            </div>

            <p className="text-slate-800 leading-relaxed text-sm whitespace-pre-wrap">{response.answer}</p>

            {/* Evidence breakdown badge */}
            <div className="pt-2 flex items-center space-x-4 text-xs text-slate-500 border-t border-slate-100">
              <span>Retrieval: {response.evidence_breakdown.retrieval}</span>
              <span>Claim Support: {response.evidence_breakdown.support}</span>
              <span>Consistency: {response.evidence_breakdown.consistency}</span>
              <span>Numerical Check: {response.numerical_check_passed ? "Passed" : "Flagged"}</span>
            </div>
          </div>

          {/* Citations Box */}
          {response.citations.length > 0 && (
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <h3 className="font-semibold text-slate-800 text-sm mb-3 flex items-center">
                <BookOpen className="w-4 h-4 mr-2 text-emerald-600" /> Grounded Source Citations
              </h3>
              <div className="space-y-3">
                {response.citations.map((c, i) => (
                  <div key={i} className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs space-y-1">
                    <div className="flex items-center justify-between font-semibold text-slate-700">
                      <span>{c.document_name}</span>
                      <span>Page {c.page_number} ({c.clause_id})</span>
                    </div>
                    <p className="text-slate-600 italic">"{c.excerpt}"</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
