import React, { useState } from 'react';
import { apiClient } from '../services/api';
import { AdvisoryAnalysisResponse } from '../types';
import { Calculator, TrendingUp, DollarSign } from 'lucide-react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts';

export const AdvisoryPage: React.FC = () => {
  const [income, setIncome] = useState('7500');
  const [expenses, setExpenses] = useState('4200');
  const [dining, setDining] = useState('500');
  const [travel, setTravel] = useState('350');
  const [grocery, setGrocery] = useState('600');
  const [fuel, setFuel] = useState('150');
  const [other, setOther] = useState('400');
  const [principal, setPrincipal] = useState('50000');
  const [rate, setRate] = useState('7.5');
  const [term, setTerm] = useState('60');

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AdvisoryAnalysisResponse | null>(null);

  const handleCalculate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const payload = {
        profile: {
          monthly_income: parseFloat(income) || 0,
          monthly_expenses: parseFloat(expenses) || 0,
          dining_spend: parseFloat(dining) || 0,
          travel_spend: parseFloat(travel) || 0,
          grocery_spend: parseFloat(grocery) || 0,
          fuel_spend: parseFloat(fuel) || 0,
          other_spend: parseFloat(other) || 0,
          annual_fee_willingness: 250,
          preferred_reward_type: "travel",
          debt_amount: 1200
        },
        loan_principal: parseFloat(principal) || null,
        annual_interest_rate_pct: parseFloat(rate) || null,
        loan_term_months: parseInt(term) || null
      };

      const res = await apiClient.post('/api/v1/advisory/analyze', payload);
      setResult(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ec4899', '#8b5cf6', '#64748b'];
  const pieData = result
    ? Object.entries(result.budget_breakdown).map(([name, value]) => ({ name, value: Number(value) }))
    : [];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-800">Financial Advisory & Budget Planning</h2>
        <p className="text-slate-500 text-sm">Transparent Decimal calculations for monthly surplus, savings rate, debt-to-income, and loan amortization (EMI).</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form Inputs */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm lg:col-span-1 space-y-4">
          <h3 className="font-semibold text-slate-800 text-sm flex items-center">
            <Calculator className="w-4 h-4 mr-2 text-emerald-600" /> Financial Parameters
          </h3>
          <form onSubmit={handleCalculate} className="space-y-3">
            <div>
              <label className="text-xs font-semibold text-slate-600">Monthly Net Income ($)</label>
              <input
                type="number"
                value={income}
                onChange={(e) => setIncome(e.target.value)}
                className="w-full mt-1 px-3 py-2 border border-slate-300 rounded-lg text-sm"
              />
            </div>
            <div>
              <label className="text-xs font-semibold text-slate-600">Monthly Expenses ($)</label>
              <input
                type="number"
                value={expenses}
                onChange={(e) => setExpenses(e.target.value)}
                className="w-full mt-1 px-3 py-2 border border-slate-300 rounded-lg text-sm"
              />
            </div>

            <div className="grid grid-cols-2 gap-2 pt-2">
              <div>
                <label className="text-xs text-slate-500">Dining ($)</label>
                <input
                  type="number"
                  value={dining}
                  onChange={(e) => setDining(e.target.value)}
                  className="w-full mt-1 px-2 py-1.5 border border-slate-200 rounded text-xs"
                />
              </div>
              <div>
                <label className="text-xs text-slate-500">Travel ($)</label>
                <input
                  type="number"
                  value={travel}
                  onChange={(e) => setTravel(e.target.value)}
                  className="w-full mt-1 px-2 py-1.5 border border-slate-200 rounded text-xs"
                />
              </div>
            </div>

            <div className="border-t border-slate-100 pt-3">
              <p className="text-xs font-semibold text-slate-700 mb-2">Optional EMI Loan Simulator</p>
              <div className="grid grid-cols-3 gap-2">
                <div>
                  <label className="text-xs text-slate-500">Principal</label>
                  <input
                    type="number"
                    value={principal}
                    onChange={(e) => setPrincipal(e.target.value)}
                    className="w-full px-2 py-1 border border-slate-200 rounded text-xs"
                  />
                </div>
                <div>
                  <label className="text-xs text-slate-500">Rate (%)</label>
                  <input
                    type="number"
                    value={rate}
                    onChange={(e) => setRate(e.target.value)}
                    className="w-full px-2 py-1 border border-slate-200 rounded text-xs"
                  />
                </div>
                <div>
                  <label className="text-xs text-slate-500">Months</label>
                  <input
                    type="number"
                    value={term}
                    onChange={(e) => setTerm(e.target.value)}
                    className="w-full px-2 py-1 border border-slate-200 rounded text-xs"
                  />
                </div>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-sm font-medium transition-colors"
            >
              {loading ? "Calculating..." : "Compute Advisory Plan"}
            </button>
          </form>
        </div>

        {/* Results View */}
        <div className="lg:col-span-2 space-y-6">
          {result ? (
            <>
              <div className="grid grid-cols-3 gap-4">
                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                  <p className="text-xs text-slate-500">Monthly Surplus</p>
                  <p className="text-xl font-bold text-slate-900 mt-1">${result.monthly_surplus}</p>
                </div>
                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                  <p className="text-xs text-slate-500">Savings Rate</p>
                  <p className="text-xl font-bold text-emerald-600 mt-1">{result.savings_rate_pct}%</p>
                </div>
                <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                  <p className="text-xs text-slate-500">Calculated Loan EMI</p>
                  <p className="text-xl font-bold text-blue-600 mt-1">
                    {result.emi ? `$${result.emi}/mo` : "N/A"}
                  </p>
                </div>
              </div>

              {/* Budget Breakdown Chart */}
              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h4 className="font-semibold text-slate-800 text-sm mb-3">Discretionary & Savings Allocation</h4>
                <div className="h-56">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                        {pieData.map((_, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Advisory Recommendations */}
              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-2">
                <h4 className="font-semibold text-slate-800 text-sm">Actionable Advisory Insights</h4>
                <ul className="space-y-2">
                  {result.recommendations.map((rec, i) => (
                    <li key={i} className="text-xs text-slate-700 bg-slate-50 p-2.5 rounded border border-slate-200 flex items-start">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-1.5 mr-2 flex-shrink-0" />
                      {rec}
                    </li>
                  ))}
                </ul>
                <p className="text-[11px] text-slate-400 mt-3 italic">{result.disclaimer}</p>
              </div>
            </>
          ) : (
            <div className="bg-white p-12 rounded-xl border border-slate-200 shadow-sm text-center text-slate-400 text-sm">
              Enter your income and expenses to view advisory calculations and budget breakdown.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
