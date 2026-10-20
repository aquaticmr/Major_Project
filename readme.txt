# FinoAddWise-X: A GenAI-Powered Financial Co-Pilot for Document Intelligence, Inclusive Advisory, and Fraud-Aware Planning

## 1. Your Role

Act as a senior AI/ML engineer, GenAI architect, Python backend engineer, MLOps engineer, security engineer, and full-stack developer.

Build a complete, runnable, end-to-end implementation of **FinoAddWise-X**, following the provided architecture diagram.

Do not merely create a prototype UI, architecture document, or code snippets. Implement a functional application with:

- React frontend and FastAPI backend.
- Clerk-based authentication and secure authorization.
- Locally trained machine-learning models.
- Persistent model artifacts using Pickle-compatible serialization.
- A complete retrieval-augmented generation (RAG) pipeline.
- Genuine RAGAS evaluation.
- Relational database persistence.
- Document processing and source-grounded financial assistance.
- URL fraud detection and financial trust scoring.
- Credit-card recommendations based on user profiles and card characteristics.
- Financial calculations and verification.
- User-specific alerts and automated actions.

Work directly in the existing project directory. Inspect the existing codebase before making changes. Create all required files, dependencies, database models, scripts, tests, configuration, and documentation.

Do not stop after generating a plan. Implement the application in phases, execute available tests, resolve errors, and provide commands to run the completed system.

Preserve existing functional code where possible. Do not overwrite working implementations unnecessarily.

## 2. Mandatory Engineering Principles

1. No hardcoded business answers, fabricated prediction results, fixed confidence scores, fake model metrics, or static API responses presented as live AI output.
2. All ML predictions must come from trained and persisted model artifacts.
3. All displayed financial values, confidence values, evaluation scores, and charts must be derived from actual runtime data.
4. Important features must have functioning backend endpoints and frontend integration.
5. Use environment variables for credentials, secrets, database connections, and configurable thresholds.
6. Support a local development mode that runs without paid APIs.
7. If an external LLM API is unavailable, provide a functioning local or deterministic fallback that clearly identifies its operating mode.
8. Never claim a model was trained when its training process did not run successfully.
9. Use synthetic data only for development when real datasets are unavailable. Clearly label synthetic data.
10. Never invent training accuracy, RAGAS scores, model confidence, fraud probabilities, or credit-card recommendations.
11. Do not use fake placeholder implementations such as `pass`, `TODO`, hardcoded JSON predictions, or unimplemented button handlers for required features.
12. Implement appropriate error handling, logging, input validation, security controls, and automated tests.
13. Avoid overengineering. Prefer modular, maintainable code that runs on an ordinary Windows laptop with CPU-only execution.
14. Keep the application usable when optional integrations such as Kafka, Redis, external LLMs, or hosted vector databases are unavailable.
15. Do not modify business logic merely to simplify implementation.
16. Clearly distinguish real public data, synthetic training data, heuristic calculations, model outputs, and LLM-generated interpretations.
17. Treat financial recommendations as informational assistance, not guaranteed financial outcomes or official lending decisions.

## 3. Technology Stack

### 3.1 Frontend

- React with Vite.
- TypeScript.
- Tailwind CSS.
- Recharts.
- Axios.
- React Router.
- Lucide icons.
- `@clerk/clerk-react` for authentication.

### 3.2 Backend

- Python 3.12.
- FastAPI.
- Uvicorn.
- Pydantic v2.
- SQLAlchemy 2.
- Alembic.
- PostgreSQL for production.
- SQLite as an optional local development database.
- Redis for optional caching and background tasks.

### 3.3 Machine Learning

- scikit-learn.
- pandas.
- NumPy.
- Pickle-compatible model persistence using `pickle` or joblib.
- XGBoost or HistGradientBoostingClassifier for credit-card recommendation modeling.
- RandomForestClassifier for URL fraud classification.
- LogisticRegression or another suitable classifier for alternative-data trust scoring.
- Train/test splitting.
- Preprocessing pipelines.
- Cross-validation where practical.
- Reproducible random seeds.
- Persisted model metadata and evaluation reports.

### 3.4 RAG and Document Intelligence

- LangChain.
- Sentence Transformers or FastEmbed for local embeddings.
- ChromaDB for persistent local vector storage.
- PyMuPDF for PDF text extraction.
- Tesseract OCR when installed.
- DOCX extraction using a suitable library.
- BM25 lexical retrieval.
- Dense semantic retrieval.
- Hybrid ranking.
- Optional cross-encoder reranking.
- RAGAS for genuine RAG evaluation.
- A locally available Hugging Face model or optional external LLM provider.

### 3.5 Security and Operations

- Clerk authentication.
- Cryptographically verified Clerk session JWTs in FastAPI.
- Role-based authorization.
- AES-256 authenticated encryption using a vetted cryptographic library for stored sensitive documents where required.
- Docker and Docker Compose.
- Pytest.
- Structured logging.
- GitHub Actions CI.
- Secure environment configuration.

Pin compatible dependency versions and document platform-specific installation requirements.

## 4. Required Project Structure

Create a maintainable repository similar to the following:

```text
finoaddwise-x/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── logging.py
│   │   ├── api/v1/
│   │   │   ├── auth.py
│   │   │   ├── documents.py
│   │   │   ├── rag.py
│   │   │   ├── advisory.py
│   │   │   ├── credit_cards.py
│   │   │   ├── fraud.py
│   │   │   ├── trust.py
│   │   │   ├── evaluation.py
│   │   │   └── alerts.py
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   ├── models.py
│   │   │   └── repositories.py
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── document_service.py
│   │   │   ├── retrieval_service.py
│   │   │   ├── verification_service.py
│   │   │   ├── advisory_service.py
│   │   │   ├── credit_card_service.py
│   │   │   ├── url_fraud_service.py
│   │   │   ├── trust_score_service.py
│   │   │   ├── encryption_service.py
│   │   │   └── notification_service.py
│   │   └── ml/
│   │       ├── training/
│   │       │   ├── train_credit_card.py
│   │       │   ├── train_url_fraud.py
│   │       │   └── train_trust_model.py
│   │       ├── inference/
│   │       └── artifacts/
│   ├── tests/
│   ├── scripts/
│   │   ├── bootstrap.py
│   │   └── generate_synthetic_data.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types/
│   │   └── App.tsx
│   ├── .env.example
│   └── package.json
├── data/
│   ├── raw/
│   ├── processed/
│   └── synthetic/
├── storage/
│   ├── documents/
│   ├── chroma/
│   └── model_registry/
├── docker-compose.yml
├── Dockerfile
├── .gitignore
└── README.md
```

Adjust the structure if necessary, but keep authentication, model training, inference, business logic, API routes, and frontend components separate.

Do not create duplicate or conflicting authentication implementations. Clerk must be the only authentication provider.

## 5. Local Machine-Learning Training and Pickle Persistence

This requirement is mandatory.

Implement actual training scripts that read datasets, fit preprocessing and classification pipelines, evaluate them, and persist their artifacts.

### 5.1 Credit-Card Recommendation Model

Train a model that recommends credit-card products based on a user's financial profile and the characteristics of available cards.

Use legitimate features such as:

- Monthly income.
- Monthly spending by category.
- Annual fee affordability.
- Preferred rewards category.
- Expected annual spending.
- Interest-bearing balance, when voluntarily supplied.
- Eligibility requirements.
- Rewards and fee structures of available cards.

Use an appropriate dataset when available. Otherwise, generate a clearly labeled synthetic training dataset with a documented feature-generation process.

This is a **product-ranking and recommendation model**, not a bank's credit underwriting model.

Build a preprocessing and model pipeline that includes:

- Missing-value handling.
- Categorical encoding.
- Numerical scaling where appropriate.
- Model training.
- Held-out test split.
- Cross-validation where practical.
- Precision, recall, F1, and a confusion matrix when classification is appropriate.
- Feature importance or interpretable explanations.
- Training metadata and dataset provenance.

Persist the trained pipeline to:

`backend/app/ml/artifacts/credit_card_model.pkl`

Save metadata to:

`backend/app/ml/artifacts/credit_card_metadata.json`

Metadata must contain the actual training timestamp, model type, dataset source, feature schema, training sample count, evaluation results, and artifact version.

Implement an inference service that loads the persisted pipeline and ranks available cards using model outputs combined with explicit fee, reward, eligibility, and affordability calculations.

The recommendation endpoint must not return a constant card or fixed prediction. Changing the user's profile or the card catalog must be capable of changing the ranking.

Include a local retraining command.

When the artifact is missing, return a clear model-not-trained error or execute an explicitly configured bootstrap training process. Never silently pretend that a model exists.

### 5.2 URL Fraud Classifier

Implement a locally trained URL classification model that predicts whether a URL is suspicious or potentially malicious.

Features may include:

- URL length.
- Hostname length.
- Number of subdomains.
- IP-address hostname indicator.
- HTTPS indicator.
- Suspicious character counts.
- URL entropy.
- Number of redirects, when actually measured.
- Domain age only when retrieved from a real supported source.

Use a labeled public dataset when available. Otherwise, create a labeled synthetic dataset using documented rules and identify it as synthetic.

Do not present synthetic-data performance as proof of real-world fraud-detection accuracy.

Train a scikit-learn pipeline, evaluate it on held-out data, and persist:

`backend/app/ml/artifacts/url_fraud_model.pkl`

Ensure the feature extractor used in training is exactly compatible with inference.

Implement:

- URL validation and normalization.
- Model probability or decision score.
- Configurable alert thresholds.
- Feature-based explanations.
- Handling of unsupported URLs.
- API and frontend integration.

Never visit a suspicious URL automatically. HTTPS alone does not establish that a URL is safe.

### 5.3 Alternative-Data Trust Score Model

Implement a demonstrative model that combines permitted, consented financial-behavior features.

Possible features:

- Payment regularity.
- Income stability.
- Debt-to-income ratio.
- Savings consistency.
- Account history length.
- Missing-data indicators.

Exclude protected characteristics and sensitive proxies from model inputs.

Train a real model using documented synthetic or public data and persist:

`backend/app/ml/artifacts/trust_score_model.pkl`

Return a calibrated probability only when calibration has actually been implemented and validated. Otherwise, identify the output as a raw model score.

Explain the factors influencing the score and the limitations of synthetic training data.

Do not claim that the model represents an official credit-bureau score or determines real lending eligibility.

### 5.4 Model Lifecycle

Implement a common model registry and lifecycle:

- Training.
- Validation.
- Versioning.
- Persistence.
- Loading.
- Prediction.
- Retraining.
- Artifact metadata.
- Model health checks.

Use Pickle-compatible persistence consistently.

Never load untrusted pickle files. Load only trusted application-generated artifacts.

Expose an API that reports whether each model is trained and available, its version, dataset provenance, and actual training metadata.

## 6. Document Intelligence Pipeline

Implement the complete document-processing lifecycle.

### 6.1 Upload and Processing

Support:

- PDF.
- TXT.
- DOCX where practical.
- Scanned PDF OCR when supported.

For every uploaded file:

1. Validate extension, MIME type, size, and content.
2. Generate an internal document identifier.
3. Store the file securely.
4. Extract text and page metadata.
5. Extract headings, tables, monetary values, dates, and clause boundaries where possible.
6. Normalize text while preserving source-page and section references.
7. Split content into clause-aware chunks.
8. Generate embeddings locally.
9. Store chunk embeddings and metadata in ChromaDB.
10. Persist document status and metadata in the relational database.
11. Make the document searchable through RAG.

Every extracted chunk must retain its document ID, page number, section or clause identifier, chunk identifier, and extraction method.

Do not expose private documents to external providers unless the user explicitly enables the provider and understands the data-sharing implications.

### 6.2 Layout-Aware Extraction

Create an extensible extraction interface supporting:

- Standard PDF text extraction.
- Table-aware extraction.
- OCR fallback.
- Optional LayoutLMv3 integration.

If LayoutLMv3 requires large downloads, additional hardware, or unavailable dependencies, fall back to a functioning extraction method and show the actual extraction method in the UI.

Never claim LayoutLMv3 was used when it was not.

## 7. RAG Retrieval and Answer Generation

Build a complete retrieval-augmented generation pipeline.

### 7.1 Retrieval

Implement:

- Local embedding generation.
- Persistent vector storage.
- BM25 lexical retrieval.
- Dense semantic retrieval.
- Hybrid ranking.
- Optional cross-encoder reranking.
- Source-aware chunk filtering.
- Document access control.

Use a configurable hybrid score:

\[
S_{\text{hybrid}}(q,c)=
\alpha S_{\text{dense}}(q,c)
+(1-\alpha)S_{\text{BM25}}(q,c)
\]

Normalize component scores appropriately before combining them. Alternatively, use reciprocal-rank fusion when the component scores cannot be meaningfully calibrated.

### 7.2 Grounded Answer Generation

For every user question:

1. Retrieve relevant document chunks.
2. Rank the retrieved chunks.
3. Construct a context containing source identifiers and page references.
4. Generate an answer using a configurable LLM provider.
5. Require the model to cite supporting sources.
6. Validate citations against retrieved chunk identifiers.
7. Detect unsupported numerical claims and missing evidence.
8. Return a source-linked answer.
9. Escalate low-evidence questions instead of inventing answers.

Return structured results containing:

- Answer text.
- Source document.
- Page number.
- Clause identifier.
- Supporting excerpts.
- Retrieval scores.
- Verification status.
- Evidence-strength category.
- Whether human review is required.

Do not label an arbitrary similarity score as a calibrated probability of answer correctness.

If no relevant source is found, explicitly state that the uploaded documents do not provide sufficient evidence.

## 8. RAGAS Evaluation

Integrate the actual RAGAS evaluation framework.

Implement an evaluation dataset containing:

- Questions.
- Reference answers.
- Relevant reference contexts.
- Retrieved contexts.
- Generated answers.

Support applicable metrics such as:

- Faithfulness.
- Answer relevancy.
- Context precision.
- Context recall.

Use the installed RAGAS version's actual supported API and metric definitions.

Create:

- A repeatable evaluation script.
- A persisted evaluation dataset.
- A JSON or CSV report.
- Evaluation timestamps.
- Dataset provenance.
- Metric-level results.
- Error handling when the selected LLM or embedding provider is unavailable.

Allow deterministic local checks for basic tests, but clearly distinguish these from genuine RAGAS evaluations.

If RAGAS requires an LLM judge, configure that judge explicitly. Use a local judge when feasible or an authorized external provider.

Never claim evaluation was performed if it failed. Persist evaluation runs in the database and expose an API endpoint to view historical results.

## 9. Numerical and Clause-Level Verification

Implement a separate verification service that checks generated answers against retrieved source material.

### Numerical Verification

- Extract monetary amounts, percentages, dates, durations, and EMI values.
- Compare answer values with relevant source values.
- Normalize currencies and numeric formats.
- Detect missing units, conflicting values, and unsupported calculations.
- Mark ambiguous matches for review.

### Clause Verification

- Associate claims with supporting source clauses.
- Check whether the source supports each claim.
- Identify missing citations and conflicting clauses.
- Distinguish direct evidence from model interpretation.

Use Python `Decimal` where monetary precision matters.

Do not claim that basic string or number comparison fully verifies legal meaning. Treat complex legal interpretation as requiring appropriate review.

## 10. Evidence-Quality Formula

Implement a transparent evidence-quality score to prioritize answer review.

Use the configurable formula:

\[
C_{\text{evidence}} =
\alpha S_{\text{retrieval}}
+\beta E_{\text{support}}
+\gamma K_{\text{consistency}}
\]

Where:

- \(S_{\text{retrieval}}\) is a normalized retrieval evidence score.
- \(E_{\text{support}}\) is the supported-claim ratio calculated by the verification layer.
- \(K_{\text{consistency}}\) is an answer consistency score.
- \(\alpha+\beta+\gamma=1\).
- Every component is normalized to \([0,1]\).

Default configurable weights:

- \(\alpha=0.40\)
- \(\beta=0.35\)
- \(\gamma=0.25\)

These are initial engineering defaults, not empirically validated weights.

Example:

\[
C_{\text{evidence}} =
0.40S_{\text{retrieval}}
+0.35E_{\text{support}}
+0.25K_{\text{consistency}}
\]

If the answer has no verifiable claims, required inputs are missing, or verification fails, return an insufficient-evidence status. Do not silently substitute perfect scores.

Call this an **evidence-quality score**, not a calibrated probability of factual correctness.

## 11. Financial Calculations and Advisory

Implement a financial advisory service that provides transparent calculations based on user-supplied data and verified document content.

Support appropriate calculations such as:

- Monthly budget breakdown.
- Income versus expenses.
- Savings rate.
- Debt-to-income ratio.
- Credit-card annual fee versus estimated rewards.
- Estimated net reward after fees.
- EMI calculations when principal, interest rate, and term are supplied.
- Savings and repayment scenarios.
- Financial goal progress.

Requirements:

1. Use `Decimal` for currency calculations.
2. Validate units, periods, interest-rate formats, and required inputs.
3. Never invent missing income, expenses, interest rates, fees, or card terms.
4. Clearly label assumptions and estimates.
5. Distinguish actual financial data from synthetic demonstration data.
6. Explain calculation formulas and intermediate values.
7. Use retrieved documents for claims about financial products or contractual terms.
8. Mark incomplete calculations as unavailable instead of returning fabricated values.
9. Do not represent informational recommendations as guaranteed savings or financial advice tailored by a licensed professional.

Create functioning backend endpoints and frontend visualizations based on actual runtime calculations.

## 12. Clerk Authentication Architecture (Mandatory)

Use **Clerk as the sole authentication provider** for FinoAddWise-X. Replace any existing custom authentication implementation with Clerk while keeping the rest of the application architecture and business logic unchanged.

Do not implement local password authentication, custom registration, locally issued login JWTs, or an alternative authentication provider.

### 12.1 Frontend Authentication

Use:

- `@clerk/clerk-react`.
- `ClerkProvider`.
- Clerk `SignIn` and `SignUp` components.
- `SignedIn` and `SignedOut`.
- `useAuth()` and `useUser()`.
- `UserButton` for account management and sign-out.

Create these routes:

- `/sign-in`
- `/sign-up`
- `/dashboard` — protected route.

Configure the frontend using:

`VITE_CLERK_PUBLISHABLE_KEY`

Wrap the React application in `ClerkProvider`. Redirect unauthenticated users to sign-in and authenticated users to the dashboard as appropriate.

Use Clerk for registration, sign-in, sign-out, session management, and account management.

Never expose the Clerk secret key in frontend code or client-side environment variables.

Use the current API supported by the installed Clerk React SDK. Do not mix obsolete Clerk APIs with the current SDK.

### 12.2 FastAPI Authentication and JWT Verification

Implement a reusable FastAPI dependency named `get_current_user` that authenticates protected requests using Clerk session tokens.

For every protected request:

1. Extract the bearer token from the `Authorization` header.
2. Verify the JWT signature against Clerk's trusted JWKS endpoint.
3. Validate the permitted signing algorithm, issuer, expiration, and configured audience or authorized-party claims where applicable.
4. Extract the verified Clerk user ID from the `sub` claim.
5. Reject missing, invalid, expired, or incorrectly issued tokens with HTTP 401.
6. Resolve the verified Clerk identity to a local database user.
7. Perform resource ownership and authorization checks separately.

Use a maintained JWT/JWKS verification library with caching and key-rotation support.

Never trust decoded JWT claims without signature verification. Never accept a user ID supplied by the frontend as proof of identity.

Configure the backend using:

- `CLERK_ISSUER_URL`
- `CLERK_JWKS_URL`
- `CLERK_SECRET_KEY`, only when trusted server-side Clerk API operations are required.

Derive or validate issuer and JWKS configuration through trusted Clerk settings. Never allow a request to specify an arbitrary JWKS endpoint.

### 12.3 Frontend-to-Backend API Integration

Create a shared Axios client for FastAPI requests.

Use Clerk's current session API to obtain a valid session token when making protected requests. Attach it as:

`Authorization: Bearer <Clerk session token>`

Implement appropriate handling for:

- HTTP 401 responses.
- Expired or missing sessions.
- Authentication failures.
- Network errors.

Avoid redirect loops and do not manually persist session tokens in `localStorage`.

All protected API endpoints must use the shared authentication dependency. Public endpoints, including health checks, may remain unauthenticated.

### 12.4 Database User Mapping

Clerk is the source of truth for authentication and user identity.

Maintain a local `users` table containing:

- Internal database user ID.
- Unique `clerk_user_id`.
- Optional email.
- Optional display name.
- Creation timestamp.
- Update timestamp.

Do not store user passwords or issue custom login JWTs.

Synchronize local user records using verified Clerk identity claims or trusted server-side Clerk API responses. Handle missing optional profile fields correctly.

Associate documents, RAG sessions, financial profiles, recommendations, notifications, reminders, and other private records with the authenticated user's internal database ID.

Enforce ownership in database queries and backend service methods. Never rely exclusively on frontend access restrictions.

### 12.5 Optional Clerk Webhooks

Implement Clerk webhooks for user creation, profile updates, and account deletion if useful for the existing architecture.

If implemented:

- Verify webhook signatures.
- Process events idempotently.
- Handle duplicate and out-of-order events safely.
- Follow the data-retention policy.

Support lazy user synchronization so the application works without webhooks.

### 12.6 Authorization and Security

Implement:

- Per-user document and RAG-session isolation.
- Server-side ownership checks for private resources.
- Role-based access control for administrative operations.
- Restricted model retraining and global configuration endpoints.
- Rate limiting for expensive operations.
- Audit logging for security-sensitive operations.
- Secure environment-configured CORS.
- Redaction of tokens and sensitive information from logs.

Authentication identifies the user; authorization determines what that user can access.

Never treat frontend route protection as a replacement for backend authorization. Never allow a user to access another user's documents or financial data by changing a request identifier.

### 12.7 Authentication Testing

Add automated tests for:

- Missing bearer tokens.
- Invalid JWT signatures.
- Expired tokens.
- Incorrect issuer.
- Invalid audience or authorized-party claims, where applicable.
- Valid Clerk session tokens.
- JWKS caching and key rotation.
- Local user synchronization and duplicate-user prevention.
- Unauthorized administrative operations.
- Cross-user document and RAG-session access.
- Public health endpoints.
- Protected FastAPI endpoints.

Mock Clerk JWKS responses and tokens in automated tests so the test suite does not require a live Clerk account.

Verify that invalid tokens cannot create authenticated local users or access protected resources.

### 12.8 Clerk Configuration and Documentation

Update the existing `.env.example`, frontend `.env.example`, and README with Clerk configuration and setup instructions.

Document how to:

1. Create a Clerk application.
2. Configure sign-in and sign-up.
3. Obtain the publishable key.
4. Configure the trusted backend issuer and JWKS URL.
5. Configure the optional server-side secret key.
6. Start the frontend and backend.
7. Test registration, sign-in, sign-out, session expiration, and protected API requests.

Keep development and production settings separate. Never commit actual credentials, tokens, or secrets.

### 12.9 Authentication Acceptance Criteria

- Clerk handles registration, sign-in, sign-out, and session management.
- React obtains Clerk session tokens and attaches them to protected API requests.
- FastAPI verifies tokens cryptographically.
- Invalid and expired tokens are rejected.
- Local users map to verified Clerk identities.
- Each user can access only their own private records.
- Administrative endpoints enforce server-side permissions.
- No custom password-based authentication or locally issued login JWTs remain.
- Authentication tests pass without requiring a live Clerk account.
- Existing ML pipelines, `.pkl` artifacts, RAG, RAGAS, financial formulas, document processing, fraud detection, recommendations, and automated actions remain unchanged.

## 13. URL Fraud Detection and Alerts

Build a complete fraud-monitoring feature around the locally trained URL classifier.

Include:

- URL submission and validation.
- Model-based risk assessment.
- Configurable risk thresholds.
- Explanation of suspicious URL features.
- User-specific assessment history.
- Alerts for high-risk results.
- Dashboard charts derived from actual assessment records.
- Clear warnings about false positives and false negatives.

Do not automatically navigate to submitted URLs.

Do not label every suspicious URL as confirmed fraud. Distinguish model predictions from confirmed incidents.

Store each assessment with the authenticated user's internal database ID.

## 14. Persistent Database and Data Isolation

Create SQLAlchemy models and migrations for relevant entities, including:

- Users.
- Documents.
- Document processing jobs.
- RAG sessions.
- RAG messages or query history.
- Financial profiles.
- Card catalog entries.
- Card recommendation results.
- Fraud assessments.
- Trust score assessments.
- RAGAS evaluation runs.
- Alerts and notifications.
- Audit events.

Adjust the schema to avoid unnecessary duplication.

Requirements:

1. Use Alembic migrations.
2. Add suitable indexes and unique constraints.
3. Enforce foreign-key relationships.
4. Scope private queries to the authenticated user.
5. Keep model artifacts and user records separate.
6. Store sensitive document data securely.
7. Provide safe local SQLite defaults and PostgreSQL production configuration.
8. Never expose one user's private records to another user.
9. Ensure deleting or deactivating a user follows an explicit retention policy.
10. Persist important state rather than relying on in-memory dictionaries.

## 15. API Requirements

Organize endpoints under `/api/v1`.

Implement endpoints appropriate to the application, including:

- `GET /health` — public health check.
- `GET /api/v1/auth/me` — authenticated user profile.
- `GET /api/v1/models/status` — model availability and training metadata.
- `POST /api/v1/documents/upload` — upload and process a document.
- `GET /api/v1/documents` — list the current user's documents.
- `GET /api/v1/documents/{document_id}` — retrieve an owned document.
- `DELETE /api/v1/documents/{document_id}` — delete an owned document.
- `POST /api/v1/rag/query` — query accessible documents.
- `GET /api/v1/rag/sessions` — list the current user's sessions.
- `POST /api/v1/advisory/analyze` — calculate financial insights.
- `POST /api/v1/credit-cards/recommend` — rank eligible card options.
- `POST /api/v1/fraud/analyze-url` — classify a submitted URL.
- `GET /api/v1/fraud/history` — retrieve the user's assessment history.
- `POST /api/v1/trust/score` — calculate a demonstrative trust score.
- `POST /api/v1/evaluation/run` — run an authorized evaluation job.
- `GET /api/v1/evaluation/history` — retrieve permitted evaluation results.
- `GET /api/v1/alerts` — list the current user's alerts.

Add endpoints for retraining and global administration only when necessary, and restrict them to authorized administrators.

Every protected endpoint must use `get_current_user` or an equivalent centralized dependency. Every resource-specific endpoint must enforce ownership in the backend.

Return proper HTTP status codes, structured Pydantic responses, and useful validation errors.

Do not expose raw stack traces, secret configuration, private file paths, or another user's information in API errors.

## 16. Frontend Application and Dashboard

Build a polished, responsive financial co-pilot interface.

Use a clean financial-product design with accessible typography, consistent spacing, responsive navigation, useful empty states, loading indicators, and informative error messages.

Implement the following pages or equivalent modules:

### 16.1 Authentication

- Clerk-powered sign-in.
- Clerk-powered sign-up.
- Protected dashboard.
- Clerk account menu.
- Sign-out.

### 16.2 Dashboard

Show actual runtime data for:

- Document count and processing status.
- Recent RAG queries.
- Financial profile summaries.
- Card recommendations.
- Fraud assessment history.
- Trust score history.
- Model training and availability status.
- RAGAS evaluation history.
- User alerts.

Never fabricate chart data or display hardcoded prediction results.

### 16.3 Document Intelligence

Implement:

- Document upload.
- Upload validation and progress.
- Processing status.
- Extracted text preview where appropriate.
- Source pages and clause references.
- Processing errors and retry options where supported.
- Document deletion.

### 16.4 RAG Assistant

Implement:

- Question submission.
- Source-grounded answers.
- Source citations.
- Page and clause references.
- Retrieval evidence.
- Verification status.
- Insufficient-evidence responses.
- Query history.

Clearly identify whether generation uses an external LLM, local model, or deterministic fallback.

### 16.5 Financial Advisory

Display:

- Income and expenses.
- Savings calculations.
- Debt-to-income calculations.
- Financial goal progress.
- Estimated card rewards after fees.
- EMI calculations when sufficient inputs are available.
- Assumptions and calculation explanations.

### 16.6 Credit-Card Recommendations

Display:

- Ranked cards.
- Relevant fee and reward terms.
- Estimated annual net rewards.
- Eligibility limitations.
- Model-generated ranking outputs.
- Explanation of ranking factors.
- Actual artifact availability and training metadata.

Do not present the result as guaranteed approval or guaranteed financial savings.

### 16.7 Fraud and Trust

Display:

- URL assessment form.
- Actual model result and risk score.
- Feature-based explanation.
- Assessment history.
- Trust model outputs and their limitations.
- Alerts generated from actual application events.

### 16.8 Evaluation and Model Health

Display:

- Model training status.
- Model artifact versions.
- Dataset provenance.
- Actual training metrics.
- Actual RAGAS evaluation runs.
- Evaluation failures.
- Timestamps and relevant metadata.

Never substitute sample metrics for unavailable results.

## 17. Model Training and Bootstrap Workflow

Create a bootstrap script that prepares the local application.

It should:

1. Load and validate environment configuration.
2. Initialize database tables or run documented migrations.
3. Prepare required storage directories.
4. Generate synthetic datasets only when explicitly configured and no suitable dataset exists.
5. Train each configured model.
6. Save artifacts and metadata only after successful training and evaluation.
7. Initialize required local embedding and vector-store components when available.
8. Report optional integrations that are unavailable.
9. Verify that model artifacts can be loaded for inference.
10. Exit with a meaningful error when a mandatory step fails.

Do not train models on every API request or silently retrain them during inference.

Support separate commands for:

- Database migration.
- Synthetic-data generation.
- Individual model training.
- Training all models.
- Model health checks.
- RAGAS evaluation.
- Test execution.
- Application startup.

Document Windows PowerShell commands as well as Docker-based startup.

## 18. Environment Configuration

Create `.env.example` files with safe placeholders.

Backend configuration should include relevant settings such as:

```dotenv
APP_ENV=development
DATABASE_URL=sqlite:///./finoaddwise.db

CLERK_ISSUER_URL=
CLERK_JWKS_URL=
CLERK_SECRET_KEY=

CORS_ORIGINS=http://localhost:5173

MODEL_ARTIFACT_DIR=app/ml/artifacts
DOCUMENT_STORAGE_DIR=../../storage/documents
CHROMA_PERSIST_DIR=../../storage/chroma

LLM_PROVIDER=local
LLM_API_KEY=
LLM_MODEL_NAME=

EMBEDDING_PROVIDER=fastembed
RAG_HYBRID_ALPHA=0.5

EVIDENCE_ALPHA=0.40
EVIDENCE_BETA=0.35
EVIDENCE_GAMMA=0.25

URL_FRAUD_THRESHOLD=0.70
ENABLE_SYNTHETIC_TRAINING_DATA=true
```

Treat these values as example defaults, not proof that integrations are configured. Validate required values at startup.

Frontend configuration:

```dotenv
VITE_CLERK_PUBLISHABLE_KEY=
VITE_API_BASE_URL=http://localhost:8000
```

Never commit actual secrets.

Ensure backend configuration uses `pydantic-settings` or an equivalent validated configuration mechanism. Do not access frontend-only environment variables from the backend.

## 19. Docker and Local Development

Provide a Docker Compose setup for the services that are actually required.

Support:

- FastAPI backend.
- React frontend.
- PostgreSQL.
- Optional Redis.

Do not make Redis, Kafka, or an external LLM mandatory for local startup unless a specific feature genuinely requires them.

Include:

- Health checks.
- Persistent database volumes.
- Appropriate service dependencies.
- Environment configuration.
- Safe storage mounts.
- Development-friendly error reporting.

Document a CPU-only Windows setup. Explain any requirements for Tesseract OCR, local language models, Docker, and model downloads.

## 20. Testing and Quality Assurance

Write automated tests for the following areas.

### Authentication and authorization

- Valid Clerk identity.
- Missing token.
- Invalid signature.
- Expired token.
- Incorrect issuer.
- User synchronization.
- Role authorization.
- Cross-user resource isolation.
- Public health endpoints.

### Machine learning

- Training scripts run successfully on supported datasets.
- Artifacts are saved.
- Artifacts load successfully.
- Missing artifacts are handled correctly.
- Feature schemas match inference.
- Predictions change when relevant inputs change.
- Metadata reflects actual training runs.
- Synthetic-data provenance is preserved.

### RAG and documents

- PDF and TXT processing.
- Supported DOCX processing.
- Invalid uploads.
- Chunk metadata.
- Retrieval and citation validation.
- User-specific document access.
- Insufficient-evidence handling.
- Verification of numerical claims.
- RAGAS evaluation failure handling.

### Financial calculations

- Decimal-based calculations.
- Missing inputs.
- Invalid rates and durations.
- Card-fee calculations.
- Reward calculations.
- EMI calculations.
- Clear handling of unsupported assumptions.

### Fraud and trust

- URL validation.
- Consistent feature extraction.
- Artifact loading.
- Prediction responses.
- Configurable alert thresholds.
- Explanation generation.
- Synthetic-data limitations.

### API and frontend

- API schema validation.
- Protected endpoints.
- Loading and error states.
- Dashboard integration.
- API authentication headers.
- Model status rendering.
- No hardcoded live prediction values.

Use deterministic test fixtures. Do not require a paid LLM or live Clerk account for the standard automated test suite.

Report actual test results. Do not claim tests passed unless they were executed successfully.

## 21. Implementation Sequence

Implement the application in the following order.

**Phase 1 — Inspect and establish the foundation**

- Inspect the current repository.
- Identify existing working components.
- Set up dependencies, configuration, database, logging, and project structure.
- Configure Clerk authentication and the shared API client.

**Phase 2 — Persistence and security**

- Implement database models and migrations.
- Implement verified Clerk session authentication.
- Implement user mapping and resource ownership.
- Add authorization and security tests.

**Phase 3 — Machine learning**

- Implement synthetic-data generation where needed.
- Implement all three training pipelines.
- Persist model artifacts and metadata.
- Implement inference services and model status endpoints.
- Execute training and validate artifact loading.

**Phase 4 — Document intelligence and RAG**

- Implement uploads, extraction, OCR fallback, chunking, embeddings, and persistent storage.
- Implement dense and BM25 retrieval.
- Implement hybrid ranking and grounded answers.
- Implement citation validation and numerical verification.

**Phase 5 — RAGAS and financial advisory**

- Implement genuine RAGAS evaluation.
- Persist evaluation runs.
- Implement financial formulas.
- Implement card ranking and reward calculations.
- Implement trust score and URL fraud services.

**Phase 6 — Frontend integration**

- Implement authentication pages.
- Implement protected dashboard routes.
- Connect all required frontend modules to functioning APIs.
- Implement charts using actual backend responses.

**Phase 7 — Integration, testing, and documentation**

- Execute migrations and bootstrap.
- Train configured models.
- Run backend tests.
- Run frontend checks and build.
- Run integration tests where possible.
- Fix discovered errors.
- Verify security and user isolation.
- Document actual limitations and startup instructions.

Do not stop after completing a phase. Continue until the required application is implemented or a specific external limitation prevents completion.

## 22. Final Acceptance Criteria

The project is complete only when the following are satisfied:

1. The React application starts successfully.
2. The FastAPI application starts successfully.
3. Clerk registration, sign-in, sign-out, and session management work.
4. FastAPI cryptographically validates Clerk session tokens.
5. Protected resources are isolated by authenticated user.
6. Database migrations work.
7. The credit-card model can be trained and saved to `.pkl`.
8. The URL fraud model can be trained and saved to `.pkl`.
9. The trust score model can be trained and saved to `.pkl`.
10. Training metadata contains real run information.
11. Inference loads persisted artifacts.
12. Missing model artifacts are handled explicitly.
13. Document upload, extraction, chunking, and storage work for supported formats.
14. RAG retrieves document evidence and returns validated source references.
15. Numerical and clause-level verification runs.
16. Genuine RAGAS evaluation can execute with its configured evaluation dependencies.
17. Financial calculations use validated inputs and appropriate numerical precision.
18. Card recommendations use model outputs and explicit fee/reward calculations.
19. Fraud assessments use the trained URL model.
20. User-specific alerts and history persist correctly.
21. Dashboard charts use actual backend data.
22. Automated tests cover the major functional and security requirements.
23. README and environment examples explain installation, configuration, training, and startup.
24. No required feature is represented by a fake prediction, fabricated metric, static result, or placeholder handler.
25. Existing business logic and non-authentication functionality remain intact.

## 23. Final Delivery Instructions

After implementation, provide:

- A summary of files created or modified.
- The actual implemented architecture.
- Exact Windows PowerShell commands to install dependencies and start the system.
- Clerk dashboard configuration steps.
- Database migration commands.
- Model training commands.
- Locations of generated `.pkl` artifacts and metadata.
- RAGAS evaluation commands.
- Test commands and actual pass/fail results.
- Any integrations requiring additional configuration.
- Any features that remain incomplete and the precise reason.

Clearly distinguish implemented and tested features from features that could not be verified.

**Final instruction:** Build the actual working application, not merely the appearance of one. Use Clerk exclusively for authentication. Keep all machine-learning training, Pickle persistence, RAG, RAGAS, document intelligence, fraud detection, financial calculations, recommendations, database behavior, and automation functional and unchanged by the authentication integration.