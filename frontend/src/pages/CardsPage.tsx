import React, { useState } from 'react';
import { apiClient } from '../services/api';
import { CardRecommendationResponse } from '../types';
import { CreditCard, Award, CheckCircle, Sparkles } from 'lucide-react';

export const CardsPage: React.FC = () => {
  const [income, setIncome] = useState('8500');
  const [dining, setDining] = useState('600');
  const [travel, setTravel] = useState('400');
  const [grocery, setGrocery] = useState('500');
  const [rewardType, setRewardType] = useState('travel');
  const [feeWillingness, setFeeWillingness] = useState('250');

  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<CardRecommendationResponse | null>(null);

  const handleRecommend = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await apiClient.post('/api/v1/credit-cards/recommend', {
        profile: {
          monthly_income: parseFloat(income) || 0,
          monthly_expenses: 4000,
          dining_spend: parseFloat(dining) || 0,
          travel_spend: parseFloat(travel) || 0,
          grocery_spend: parseFloat(grocery) || 0,
          fuel_spend: 150,
          other_spend: 300,
          annual_fee_willingness: parseFloat(feeWillingness) || 0,
          preferred_reward_type: rewardType,
          debt_amount: 500
        }
      });
      setRecommendations(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-800">ML Credit Card Recommender</h2>
        <p className="text-slate-500 text-sm">Ranks credit cards by combining trained HistGradientBoostingClassifier predictions with explicit fee and rewards modeling.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form Inputs */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
          <h3 className="font-semibold text-slate-800 text-sm flex items-center">
            <CreditCard className="w-4 h-4 mr-2 text-emerald-600" /> Spending Profile
          </h3>
          <form onSubmit={handleRecommend} className="space-y-3">
            <div>
              <label className="text-xs font-semibold text-slate-600">Monthly Income ($)</label>
              <input
                type="number"
                value={income}
                onChange={(e) => setIncome(e.target.value)}
                className="w-full mt-1 px-3 py-2 border border-slate-300 rounded-lg text-sm"
              />
            </div>
            <div>
              <label className="text-xs font-semibold text-slate-600">Monthly Dining Spend ($)</label>
              <input
                type="number"
                value={dining}
                onChange={(e) => setDining(e.target.value)}
                className="w-full mt-1 px-3 py-2 border border-slate-300 rounded-lg text-sm"
              />
            </div>
            <div>
              <label className="text-xs font-semibold text-slate-600">Monthly Travel Spend ($)</label>
              <input
                type="number"
                value={travel}
                onChange={(e) => setTravel(e.target.value)}
                className="w-full mt-1 px-3 py-2 border border-slate-300 rounded-lg text-sm"
              />
            </div>
            <div>
              <label className="text-xs font-semibold text-slate-600">Preferred Rewards Type</label>
              <select
                value={rewardType}
                onChange={(e) => setRewardType(e.target.value)}
                className="w-full mt-1 px-3 py-2 border border-slate-300 rounded-lg text-sm"
              >
                <option value="cashback">Cashback</option>
                <option value="travel">Travel & Flights</option>
                <option value="points">Flexible Points</option>
                <option value="lounge">Airport Lounge Access</option>
              </select>
            </div>
            <div>
              <label className="text-xs font-semibold text-slate-600">Annual Fee Willingness ($)</label>
              <input
                type="number"
                value={feeWillingness}
                onChange={(e) => setFeeWillingness(e.target.value)}
                className="w-full mt-1 px-3 py-2 border border-slate-300 rounded-lg text-sm"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-sm font-medium transition-colors flex items-center justify-center"
            >
              <Sparkles className="w-4 h-4 mr-2" />
              {loading ? "Ranking Models..." : "Rank Best Cards"}
            </button>
          </form>
        </div>

        {/* Card Catalog List */}
        <div className="lg:col-span-2 space-y-4">
          {recommendations ? (
            <>
              <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
                <span>Model Version: {recommendations.model_version}</span>
                <span>Sorted by Composite ML Score & Net Yield</span>
              </div>
              <div className="space-y-4">
                {recommendations.ranked_cards.map((card, idx) => (
                  <div key={card.card_id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative overflow-hidden">
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center space-x-2">
                          <span className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold flex items-center justify-center">
                            #{idx + 1}
                          </span>
                          <h4 className="font-bold text-slate-900 text-base">{card.card_name}</h4>
                          <span className="text-xs text-slate-500">by {card.issuer}</span>
                        </div>
                        <p className="text-xs text-emerald-600 font-semibold mt-1">
                          {card.eligibility_status}
                        </p>
                      </div>

                      <div className="text-right">
                        <p className="text-xs text-slate-400">Estimated Net Value</p>
                        <p className="text-xl font-bold text-slate-900">+${card.estimated_net_rewards}/yr</p>
                        <p className="text-xs text-slate-500">Annual Fee: ${card.annual_fee}</p>
                      </div>
                    </div>

                    <div className="mt-4 pt-3 border-t border-slate-100 flex flex-wrap gap-2">
                      {card.key_perks.map((perk, i) => (
                        <span key={i} className="inline-flex items-center px-2 py-1 rounded bg-slate-100 text-slate-700 text-xs font-medium">
                          <CheckCircle className="w-3 h-3 mr-1 text-emerald-600" />
                          {perk}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
              <p className="text-[11px] text-slate-400 mt-2 italic">{recommendations.disclaimer}</p>
            </>
          ) : (
            <div className="bg-white p-12 rounded-xl border border-slate-200 shadow-sm text-center text-slate-400 text-sm">
              Adjust your profile and click "Rank Best Cards" to generate ML recommendations.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
