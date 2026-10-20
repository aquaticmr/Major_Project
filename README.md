# FinoAddWise-X: A GenAI-Powered Financial Co-Pilot

A production-grade, low-hallucination GenAI financial advisory and threat-detection platform implementing grounded document intelligence, machine learning inference with Pickle persistence, Clerk authentication, and transparent evidence verification.

---

## 🏛 Implemented Architecture

As specified in the system architecture diagram:
- **Client & Edge Layer**: Modern React frontend with Vite, Tailwind CSS, Recharts, and `@clerk/clerk-react` authentication.
- **AI Orchestration & API Gateway**: FastAPI backend with cryptographically validated Clerk JWT session authentication and role-based permissions.
- **Document Intelligence Pipeline**: Multi-format extraction (PDF via PyMuPDF layout parser, DOCX, TXT), clause-level chunking, and ChromaDB persistent vector storage.
- **Low-Hallucination Grounded RAG Engine**: Hybrid retrieval combining dense semantic embeddings with BM25 lexical ranking:
  $$S_{\text{hybrid}}(q,c) = \alpha S_{\text{dense}}(q,c) + (1-\alpha)S_{\text{BM25}}(q,c)$$
  alongside numerical claims verification and evidence scoring:
  $$C_{\text{evidence}} = \alpha S_{\text{retrieval}} + \beta E_{\text{support}} + \gamma K_{\text{consistency}}$$
- **ML Microservices & Advisory**:
  - **Credit Card Recommender**: Trained `HistGradientBoostingClassifier` with fee/reward simulations.
  - **URL Fraud Threat Intel**: Trained `RandomForestClassifier` with lexical/structural entropy analysis.
  - **Trust Score Model**: Calibrated `LogisticRegression` combining consented alternative financial indicators.
- **Data & Storage Vault**: AES-256 Fernet document encryption, SQLAlchemy 2 ORM with SQLite (local) and PostgreSQL support.
- **RAGAS Benchmark Framework**: Repeatable evaluation pipeline computing Faithfulness, Answer Relevancy, Context Precision, and Recall.

---

## 🚀 Quickstart Guide (Windows PowerShell)

### 1. Backend Setup & Model Bootstrap

Open a PowerShell terminal:
```powershell
# Navigate to backend and create virtual environment
cd c:\Major-Project
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r backend\requirements.txt

# Bootstrap database, generate synthetic data, train ML models, and serialize .pkl artifacts
$env:PYTHONPATH = "c:\Major-Project"
python backend\scripts\bootstrap.py

# Run automated tests
pytest backend\tests -v

# Start FastAPI backend server
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

FastAPI Swagger Documentation will be available at: `http://localhost:8000/docs`

---

### 2. Frontend Setup (React + Clerk + Tailwind)

Ensure Node.js (v18+) is installed:
```powershell
cd c:\Major-Project\frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend application will be accessible at: `http://localhost:5173`

---

## 🔐 Clerk Authentication Configuration

1. Visit [Clerk Dashboard](https://dashboard.clerk.com) and create an application.
2. In frontend `.env`:
   ```dotenv
   VITE_CLERK_PUBLISHABLE_KEY=pk_test_...
   VITE_API_BASE_URL=http://localhost:8000
   ```
3. In backend `.env`:
   ```dotenv
   CLERK_ISSUER_URL=https://your-instance.clerk.accounts.dev
   CLERK_JWKS_URL=https://your-instance.clerk.accounts.dev/.well-known/jwks.json
   ```
4. Authenticated requests from React automatically attach `Authorization: Bearer <clerk_token>`, cryptographically validated by FastAPI.

---

## 📦 Machine Learning Artifacts

Trained artifacts and verifiable metadata are stored in:
- `backend/app/ml/artifacts/credit_card_model.pkl` & `credit_card_metadata.json`
- `backend/app/ml/artifacts/url_fraud_model.pkl` & `url_fraud_metadata.json`
- `backend/app/ml/artifacts/trust_score_model.pkl` & `trust_score_metadata.json`

---

## 🐳 Docker Deployment

To launch the full stack with PostgreSQL:
```bash
docker-compose up --build
```
