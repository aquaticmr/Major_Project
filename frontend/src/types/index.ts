export interface UserProfile {
  id: string;
  clerk_user_id: string;
  email: string | null;
  display_name: string | null;
  role: string;
  created_at: string;
}

export interface DocumentItem {
  id: string;
  filename: string;
  file_type: string;
  file_size: number;
  page_count: number;
  status: string;
  extraction_method: string;
  chunk_count: number;
  created_at: string;
}

export interface Citation {
  document_id: string;
  document_name: string;
  page_number: number;
  clause_id: string | null;
  excerpt: string;
}

export interface RAGResponse {
  session_id: string;
  answer: string;
  citations: Citation[];
  evidence_score: number;
  verification_status: string;
  numerical_check_passed: boolean;
  requires_human_review: boolean;
  evidence_breakdown: {
    retrieval: number;
    support: number;
    consistency: number;
  };
}

export interface RankedCard {
  card_id: string;
  card_name: string;
  issuer: string;
  annual_fee: number;
  estimated_annual_rewards: number;
  estimated_net_rewards: number;
  model_score: number;
  eligibility_status: string;
  key_perks: string[];
}

export interface CardRecommendationResponse {
  ranked_cards: RankedCard[];
  model_version: string;
  disclaimer: string;
}

export interface AdvisoryAnalysisResponse {
  monthly_surplus: number;
  savings_rate_pct: number;
  debt_to_income_ratio: number;
  emi: number | null;
  budget_breakdown: Record<string, number>;
  recommendations: string[];
  disclaimer: string;
}

export interface URLFraudResponse {
  url: string;
  risk_score: number;
  is_malicious: boolean;
  risk_level: string;
  explanation_factors: string[];
  model_version: string;
  disclaimer: string;
}

export interface TrustScoreResponse {
  trust_score: number;
  risk_category: string;
  calibrated: boolean;
  contributing_factors: string[];
  model_version: string;
  disclaimer: string;
}

export interface ModelMetadata {
  model_name: string;
  is_trained: boolean;
  version: string | null;
  trained_at: string | null;
  algorithm: string | null;
  sample_count: number | null;
  metrics: Record<string, any> | null;
  provenance: string | null;
}

export interface AlertNotification {
  id: string;
  title: string;
  message: string;
  alert_type: string;
  is_read: boolean;
  created_at: string;
}
